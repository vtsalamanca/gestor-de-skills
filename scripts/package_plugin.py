#!/usr/bin/env python3
"""Build a deterministic Plugin Creator archive from an exact Git commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import uuid
import zipfile


OFFICIAL_REPOSITORY = "https://github.com/vtsalamanca/gestor-de-skills.git"
EXPECTED_SKILLS = {
    "auditar-skills",
    "crear-skills",
    "descubrir-skills",
    "ingenieria-fiable",
    "integrar-skills",
    "inventariar-skills",
    "organizaciondeltrabajo",
}
PACKAGE_ROOT_FILES = {"README.md", ".codex-plugin/plugin.json"}
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
SUSPICIOUS_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
SUSPICIOUS_NAMES = {".env", "credentials.json", "secrets.json"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKILL_NAME_RE = re.compile(r"^name:\s*([^\s#]+)\s*$", re.MULTILINE)


class PackageError(RuntimeError):
    """A clear, user-facing packaging failure."""


def run_git(arguments: list[str], cwd: Path | None = None) -> str:
    command = ["git", *arguments]
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as exc:
        raise PackageError("No se encontró Git en el sistema.") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "error desconocido").strip()
        raise PackageError(f"Falló {' '.join(command)}: {detail}") from exc
    return result.stdout.strip()


def remove_tree(path: Path) -> None:
    def make_writable(function, target, _error) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    if path.exists():
        shutil.rmtree(path, onexc=make_writable)


def export_commit(repository: str, commit: str, destination: Path) -> str:
    """Fetch only the requested commit and export its tracked bytes without .git."""
    local_repository = Path(repository).resolve()
    fetch_repository: Path | None = None
    if local_repository.is_dir():
        source = local_repository
        resolved = run_git(["rev-parse", f"{commit}^{{commit}}"], source)
    else:
        fetch_repository = destination.parent / f".fetch-{uuid.uuid4().hex[:8]}"
        run_git(["init", "--quiet", str(fetch_repository)])
        run_git(["-c", "http.sslBackend=openssl", "fetch", "--quiet", "--depth", "1", repository, commit], fetch_repository)
        resolved = run_git(["rev-parse", "FETCH_HEAD^{commit}"], fetch_repository)
        source = fetch_repository

    archive_path = destination.parent / f".snapshot-{uuid.uuid4().hex[:8]}.tar"
    try:
        run_git(["archive", "--format=tar", f"--output={archive_path}", resolved], source)
        destination.mkdir(parents=True)
        with tarfile.open(archive_path, "r") as archive:
            for member in archive.getmembers():
                path = PurePosixPath(member.name)
                if path.is_absolute() or ".." in path.parts:
                    raise PackageError(f"Ruta insegura en el commit: {member.name}")
            archive.extractall(destination, filter="data")
    finally:
        archive_path.unlink(missing_ok=True)
        if fetch_repository is not None:
            remove_tree(fetch_repository)
    return resolved


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PackageError(f"Falta el archivo obligatorio: {path.relative_to(path.parents[1])}") from exc
    except json.JSONDecodeError as exc:
        raise PackageError(f"JSON no válido en {path}: {exc}") from exc


def validate_snapshot(root: Path) -> tuple[str, list[Path]]:
    plugin = load_json(root / ".codex-plugin" / "plugin.json")
    marketplace = load_json(root / ".agents" / "plugins" / "marketplace.json")

    if plugin.get("name") != "gestor-de-skills":
        raise PackageError("El manifiesto no identifica el plugin gestor-de-skills.")
    version = plugin.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise PackageError("La versión del plugin no tiene formato X.Y.Z.")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise PackageError("El marketplace debe declarar exactamente un plugin.")
    entry = entries[0]
    if entry.get("name") != plugin["name"] or entry.get("version") != version:
        raise PackageError("Las versiones o nombres del manifiesto y marketplace no coinciden.")

    skills_root = root / "skills"
    actual_skills = {p.name for p in skills_root.iterdir() if p.is_dir()}
    if actual_skills != EXPECTED_SKILLS:
        missing = sorted(EXPECTED_SKILLS - actual_skills)
        extra = sorted(actual_skills - EXPECTED_SKILLS)
        raise PackageError(f"El conjunto de skills no es el esperado. Faltan={missing}; sobran={extra}.")

    files: list[Path] = []
    for relative in sorted(PACKAGE_ROOT_FILES):
        path = root / relative
        if not path.is_file():
            raise PackageError(f"Falta el archivo obligatorio: {relative}")
        files.append(path)

    for skill in sorted(EXPECTED_SKILLS):
        skill_file = skills_root / skill / "SKILL.md"
        if not skill_file.is_file():
            raise PackageError(f"Falta skills/{skill}/SKILL.md")
        match = SKILL_NAME_RE.search(skill_file.read_text(encoding="utf-8"))
        if not match or match.group(1) != skill:
            raise PackageError(f"El nombre declarado en skills/{skill}/SKILL.md no coincide con su ruta.")
        for path in sorted((skills_root / skill).rglob("*")):
            if path.is_symlink():
                raise PackageError(f"No se permiten enlaces simbólicos: {path.relative_to(root)}")
            if not path.is_file():
                continue
            if path.name in IGNORED_NAMES:
                continue
            lower_name = path.name.lower()
            if lower_name in SUSPICIOUS_NAMES or path.suffix.lower() in SUSPICIOUS_SUFFIXES:
                raise PackageError(f"Archivo potencialmente sensible rechazado: {path.relative_to(root)}")
            files.append(path)

    unique_files = sorted(set(files), key=lambda p: p.relative_to(root).as_posix())
    return version, unique_files


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_archive(snapshot: Path, output: Path, commit: str) -> dict:
    version, files = validate_snapshot(snapshot)
    output.parent.mkdir(parents=True, exist_ok=True)
    file_hashes: dict[str, str] = {}

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = PurePosixPath(path.relative_to(snapshot).as_posix()).as_posix()
            data = path.read_bytes()
            file_hashes[relative] = sha256_bytes(data)
            info = zipfile.ZipInfo(relative, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    zip_hash = sha256_bytes(output.read_bytes())
    report = {
        "schema_version": 1,
        "repository": OFFICIAL_REPOSITORY,
        "commit": commit,
        "package_version": version,
        "file_count": len(files),
        "files": file_hashes,
        "archive": {"name": output.name, "sha256": zip_hash},
    }
    report_path = output.with_suffix(output.suffix + ".sha256.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=OFFICIAL_REPOSITORY, help="URL Git o ruta local del repositorio")
    parser.add_argument("--commit", required=True, help="SHA completo e inmutable que se debe empaquetar")
    parser.add_argument("--output", type=Path, required=True, help="Ruta del ZIP de salida")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not re.fullmatch(r"[0-9a-fA-F]{40}", args.commit):
        print("ERROR: --commit debe ser un SHA Git completo de 40 caracteres.", file=sys.stderr)
        return 2
    try:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.parent / f".pkg-{uuid.uuid4().hex[:8]}"
        temporary.mkdir()
        try:
            snapshot = temporary / "repository"
            resolved = export_commit(args.repository, args.commit.lower(), snapshot)
            if resolved.lower() != args.commit.lower():
                raise PackageError(f"El commit resuelto {resolved} no coincide con el solicitado {args.commit}.")
            report = build_archive(snapshot, output, resolved)
        finally:
            remove_tree(temporary)
    except PackageError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Paquete {report['package_version']} creado desde {report['commit']}.")
    print(f"ZIP: {args.output.resolve()}")
    print(f"SHA-256: {report['archive']['sha256']}")
    print(f"Archivos: {report['file_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
