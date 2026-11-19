#!/usr/bin/env python3
"""Genera un inventario veraz a partir de nombres MCP observados en un chat.

No consulta ChatGPT, no lanza herramientas y no intenta acceder al llavero.
La captura de funciones la aporta quien dispone del catálogo en su sesión.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,99}$")
MUTATION_RE = re.compile(
    r"(?:^set_|^write_|^create_|^edit_|^move_|^kill_|^start_|^stop_|"
    r"^force_|^interact_|^debian_lab_command|^debian_laboratorio_iniciar|"
    r"_(?:start|stop|gesture|focus|move|resize|type|create|edit|append|"
    r"authenticar|accion|iniciar|modulo_revisado|roundtrip|click_escape)$)"
)

def read_snapshot_tsv(raw: str) -> list[dict[str, str]]:
    """Valida que cada registro tenga un nombre único y descripción segura."""
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            raise ValueError(f"Línea {index}: se requieren exactamente dos columnas TSV")
        name, description = fields
        if not NAME_RE.fullmatch(name):
            raise ValueError(f"Línea {index}: nombre inválido")
        description = description.strip()
        if not description or len(description) > 220 or any(ord(c) < 32 for c in description):
            raise ValueError(f"Línea {index}: descripción inválida")
        if name in seen:
            raise ValueError(f"Línea {index}: herramienta duplicada: {name}")
        seen.add(name)
        items.append({"name": name, "description": description})
    if not items:
        raise ValueError("La captura está vacía")
    if len(items) > 500:
        raise ValueError("La captura tiene una cantidad inesperada de herramientas")
    return items


def group(name: str) -> str:
    if name.startswith("debian_gui_"):
        return "interfaz_grafica"
    if name.startswith("debian_host_") or name.startswith("debian_lab_"):
        return "equipo_y_autorizaciones"
    if name.startswith("debian_laboratorio_"):
        return "operaciones_locales"
    if name.startswith("debian_terminal_"):
        return "terminal_aislada"
    if name.startswith("debian_project_"):
        return "proyectos"
    if "process" in name or "session" in name or "terminate" in name:
        return "procesos"
    if any(word in name for word in ("file", "directory", "search", "config", "edit_block")):
        return "archivos_y_configuracion"
    return "otras"


def class_of_effect(name: str) -> str:
    """Conservadora: el nombre NO autoriza ni confirma que una función escriba."""
    return "accion_potencial" if MUTATION_RE.search(name) else "efecto_por_confirmar"


def parse_time(stamp: str) -> str:
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Marca de tiempo ISO 8601 inválida") from exc
    if dt.tzinfo is None:
        raise ValueError("La fecha debe incluir zona horaria")
    return dt.isoformat()


def read_evidence(path: Path | None, known: set[str]) -> dict[str, dict[str, str]]:
    """Pruebas declaradas separadas del mero hecho de exponer una función."""
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Formato de evidencias inválido")
    checks = data.get("checks")
    if not isinstance(checks, dict):
        raise ValueError("Faltan comprobaciones")
    out = {}
    for name, check in checks.items():
        if name not in known or not isinstance(check, dict):
            raise ValueError("Comprobación de herramienta inexistente o inválida")
        if check.get("result") not in ("verificada", "fallida", "parcial"):
            raise ValueError("Estado de prueba desconocido")
        when = parse_time(str(check.get("checked_at", "")))
        scope = check.get("scope")
        if not isinstance(scope, str) or not (3 <= len(scope) <= 160):
            raise ValueError("Alcance de prueba inválido")
        out[name] = {"result": check["result"], "checked_at": when, "scope": scope}
    return out


def build_snapshot(raw: str, captured_at: str, evidence: dict | None = None) -> dict:
    parsed = read_snapshot_tsv(raw)
    evid = evidence or {}
    known = {t["name"] for t in parsed}
    if set(evid) - known:
        raise ValueError("Evidencia de herramienta ausente de la captura")
    entries = []
    for item in parsed:
        name = item["name"]
        entries.append({
            **item,
            "group": group(name),
            "effect": class_of_effect(name),
            "visibility": "expuesta_en_chat_en_captura",
            "verification": evid.get(name, {"result": "sin_prueba"}),
        })
    return {
        "schema_version": 1,
        "connector": "Control Debian — Sustituto independiente",
        "capture_source": "catálogo de funciones realmente expuestas en una conversación",
        "captured_at": parse_time(captured_at),
        "input_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "total": len(entries),
        "classification": "Visibilidad no significa acceso ni ejecución. Verificaciones limitadas al alcance indicado.",
        "tools": entries,
    }


def differences(previous: dict | None, current: dict) -> dict[str, list[str]]:
    before = {x["name"]: x.get("description", x.get("declared_description", "")) for x in previous.get("tools", [])} if previous else {}
    after = {x["name"]: x["description"] for x in current["tools"]}
    return {
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "description_changed": sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),
    }


def markdown(snapshot: dict, diff: dict[str, list[str]]) -> str:
    esc = lambda s: str(s).replace("|", r"\|").replace("\n", " ")
    out = [
        "# Inventario individual de herramientas MCP — Control Debian",
        "",
        f"**Observación:** {snapshot['captured_at']}. **Funciones expuestas:** {snapshot['total']}.",
        f"**SHA-256 TSV origen:** `{snapshot['input_sha256']}`.",
        "",
        "Este inventario refleja el **catálogo visible en una conversación concreta**, no "
        "un test de funcionamiento de todas las herramientas ni el catálogo de otras sesiones.",
        "Las comprobaciones están asociadas a su alcance y fecha; una herramienta "
        "sin prueba no se considera operativa.",
        "",
        "## Cambios frente a la captura anterior",
        f"- Altas: {', '.join(diff['added']) or 'ninguna'}",
        f"- Bajas: {', '.join(diff['removed']) or 'ninguna'}",
        f"- Descripciones modificadas: {', '.join(diff['description_changed']) or 'ninguna'}",
        "",
    ]
    for category in dict.fromkeys(x["group"] for x in snapshot["tools"]):
        rows = [x for x in snapshot["tools"] if x["group"] == category]
        out.extend([
            f"## {category.replace('_', ' ').title()} ({len(rows)})",
            "",
            "| Herramienta | Función declarada | Efecto por revisar | Prueba real |",
            "|---|---|---|---|",
        ])
        for x in rows:
            v = x["verification"]
            test = "No probada en esta captura"
            if v["result"] != "sin_prueba":
                test = f"{v['result']} ({v['scope']}; {v['checked_at']})"
            out.append(f"| `{x['name']}` | {esc(x['description'])} | "
                       f"{esc(x['effect'])} | {esc(test)} |")
        out.append("")
    out.extend([
        "## Regla de consulta",
        "En cada chat, comprobar que la función figura en el catálogo realmente disponible y "
        "revisar su contrato. Después consultar este inventario como evidencia histórica "
        "y, para operaciones importantes, ejecutar una prueba autorizada y registrar el resultado.",
        "Ni el archivo ni su fecha habilitan permisos, credenciales o servicios.",
        "",
    ])
    return "\n".join(out)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".inventario-", dir=path.parent, text=True)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="TSV observado: nombre<TAB>descripción")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--captured-at", required=True, help="fecha/hora ISO8601 con zona")
    parser.add_argument("--expected-count", type=int, help="recuento observado en el chat")
    parser.add_argument("--evidence", type=Path, help="JSON separado de pruebas reales")
    parser.add_argument("--write", action="store_true", help="autoriza sobrescritura atómica")
    parser.add_argument("--allow-removals", action="store_true", help="acepta bajas tras inspección")
    args = parser.parse_args(argv)
    raw = args.input.read_text(encoding="utf-8")
    parsed = read_snapshot_tsv(raw)
    if args.expected_count is not None and len(parsed) != args.expected_count:
        raise ValueError(f"Captura incompleta: esperadas {args.expected_count}, leídas {len(parsed)}")
    evidence = read_evidence(args.evidence, {x["name"] for x in parsed})
    current = build_snapshot(raw, args.captured_at, evidence)
    target = args.output_dir / "inventario-mcp.json"
    previous = json.loads(target.read_text(encoding="utf-8")) if target.exists() else None
    diff = differences(previous, current)
    if args.write and diff["removed"] and not args.allow_removals:
        raise ValueError(f"Se detectaron bajas: {len(diff['removed'])}; revisar antes de --allow-removals")
    if args.write:
        atomic_write(target, json.dumps(current, ensure_ascii=False, indent=2) + "\n")
        atomic_write(args.output_dir / "inventario-mcp.md", markdown(current, diff))
    print(json.dumps({
        "status": "written" if args.write else "dry-run",
        "tools": current["total"],
        "verified_checks": len(evidence),
        "changes": {key: len(value) for key, value in diff.items()},
        "input_sha256": current["input_sha256"],
        "output_dir": str(args.output_dir) if args.write else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
