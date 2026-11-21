#!/usr/bin/env python3
"""Evidencia local de reparación: ejecuta pruebas explícitas y vincula sus resultados a archivos exactos.

No usa shell ni red por sí mismo ni conserva salida textual; el test explícito puede tener efectos externos.
No autentica pruebas ni demuestra su calidad funcional.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

MAX_FILE_BYTES = 20 * 1024 * 1024
FORBIDDEN = {".env", ".ssh", "id_rsa", "id_ed25519", "auth.json", "credentials.json"}
LABEL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,39}$")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for part in iter(lambda: handle.read(65536), b""):
            digest.update(part)
    return digest.hexdigest()


def resolve_files(root: Path, names: list[str]) -> dict[str, str]:
    if not names:
        raise ValueError("Indica al menos un archivo --watch.")
    found: dict[str, str] = {}
    for raw in names:
        candidate = Path(raw)
        if candidate.is_absolute() or ".." in candidate.parts or (root / candidate).is_symlink():
            raise ValueError("Ruta no permitida: archivo externo, ascendente o enlace simbólico")
        if any(part.lower() in FORBIDDEN or part == ".git" for part in candidate.parts):
            raise ValueError("Archivo sensible o metadatos Git no permitidos")
        resolved = (root / candidate).resolve(strict=True)
        if not resolved.is_relative_to(root) or not resolved.is_file() or resolved.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("El archivo no es regular, es externo o demasiado grande")
        name = resolved.relative_to(root).as_posix()
        found[name] = file_hash(resolved)
    return dict(sorted(found.items()))


def store(path: Path, payload: dict) -> None:
    if path.is_symlink():
        raise ValueError("El recibo no puede ser un enlace simbólico")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".prueba-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Recibo inexistente o con formato incompatible")
    return data


def evaluate(root: Path, receipt: dict) -> dict:
    issues: list[str] = []
    root_sha = hashlib.sha256(str(root.resolve()).encode()).hexdigest()
    if receipt.get("project_path_sha256") != root_sha:
        issues.append("El recibo pertenece a otro directorio de proyecto")
    before = receipt.get("before")
    after = receipt.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        issues.append("Falta evidencia de una fase before/after")
    if isinstance(before, dict) and isinstance(after, dict):
        if before.get("command_sha256") != after.get("command_sha256"):
            issues.append("Las pruebas before y after no son equivalentes")
        if before.get("exit_code") in (0, "timeout", "error") or not isinstance(before.get("exit_code"), int):
            issues.append("El fallo original no quedó reproducido")
        if after.get("exit_code") != 0:
            issues.append("La prueba posterior no terminó satisfactoriamente")
        if before.get("files_before") != before.get("files_after") or after.get("files_before") != after.get("files_after"):
            issues.append("Una prueba modificó uno o varios archivos vigilados")
        if before.get("requirements") != after.get("requirements") or set(before.get("watched", {})) != set(after.get("watched", {})):
            issues.append("Cambió el alcance de prueba entre fases")
        watched = after.get("watched")
        if not isinstance(watched, dict) or not watched:
            issues.append("Sin huellas de archivos probados")
        else:
            try:
                current = resolve_files(root, list(watched))
                if current != watched:
                    issues.append("Archivos modificados después de las pruebas (evidencia obsoleta)")
            except (ValueError, OSError) as exc:
                issues.append(f"No se pueden volver a verificar archivos: {exc}")
    return {
        "verdict": "consistent_record" if not issues else "incomplete_or_stale",
        "issues": issues,
        "warning": "La coherencia del recibo no acredita que la prueba sea relevante, honesta o suficiente; no prueba despliegues.",
        "requirements": receipt.get("requirements", []),
    }


def record(args: argparse.Namespace) -> int:
    root = args.root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("--root debe ser un directorio")
    if args.timeout <= 0 or args.timeout > 600:
        raise ValueError("Tiempo máximo no permitido (1-600 s)")
    req = sorted(set(args.requirement))
    if not req or any(not LABEL_RE.fullmatch(item) for item in req):
        raise ValueError("Indica etiquetas --requirement válidas")
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command or any(not part or "\x00" in part for part in command):
        raise ValueError("Indica un comando de prueba explícito después de --")
    before = resolve_files(root, args.watch)
    cmd_hash = hashlib.sha256(json.dumps(command, ensure_ascii=False).encode()).hexdigest()
    if args.phase == "before":
        if args.evidence.exists():
            raise ValueError("El recibo ya existe: no sobrescribir una evidencia anterior")
        receipt = {"schema_version": 1, "project_path_sha256": hashlib.sha256(str(root).encode()).hexdigest(), "requirements": req, "before": None, "after": None}
    else:
        receipt = read(args.evidence)
        if receipt.get("project_path_sha256") != hashlib.sha256(str(root).encode()).hexdigest():
            raise ValueError("Recibo asociado a otro proyecto")
        if not isinstance(receipt.get("before"), dict) or receipt.get("after") is not None:
            raise ValueError("La fase after requiere un before existente y no usado")
        if req != receipt.get("requirements") or cmd_hash != receipt["before"].get("command_sha256"):
            raise ValueError("Etiquetas y comando deben ser iguales a la fase original")
        if list(before) != list(receipt["before"].get("watched", {})):
            raise ValueError("La lista de archivos vigilados cambió")
    try:
        with tempfile.TemporaryFile() as captured:
            child = subprocess.Popen(command, cwd=root, stdout=captured, stderr=subprocess.STDOUT,
                                     start_new_session=(os.name == "posix"))
            try:
                code: int | str = child.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                try:
                    if os.name == "posix":
                        os.killpg(child.pid, signal.SIGKILL)
                    else:
                        child.kill()
                except ProcessLookupError:
                    code = "timeout"  # El proceso ya terminó durante la interrupción.
                child.wait()
                code = "timeout"
            captured.seek(0)
            digest = hashlib.sha256()
            for chunk in iter(lambda: captured.read(65536), b""):
                digest.update(chunk)
            output_digest = digest.hexdigest()
    except OSError:
        code = "error"
        output_digest = None
    after = resolve_files(root, args.watch)
    receipt[args.phase] = {
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "command_sha256": cmd_hash, "requirements": req,
        "watched": before, "files_before": before, "files_after": after,
        "exit_code": code, "output_sha256": output_digest, "timeout_seconds": args.timeout,
    }
    store(args.evidence, receipt)
    summary = evaluate(root, receipt)
    summary.update({"phase": args.phase, "test_exit_code": code})
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if args.phase == "before" or code == 0 else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    p = modes.add_parser("record", help="Ejecutar test real y guardar recibo privado")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--phase", choices=("before", "after"), required=True)
    p.add_argument("--requirement", action="append", default=[])
    p.add_argument("--watch", action="append", required=True)
    p.add_argument("--timeout", type=int, default=90)
    p.add_argument("command", nargs=argparse.REMAINDER)
    c = modes.add_parser("check", help="Verificar huellas y coherencia del recibo")
    c.add_argument("--root", type=Path, required=True)
    c.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.mode == "record":
            return record(args)
        verdict = evaluate(args.root.resolve(strict=True), read(args.evidence))
        print(json.dumps(verdict, ensure_ascii=False))
        return 0 if verdict["verdict"] == "consistent_record" else 1
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
