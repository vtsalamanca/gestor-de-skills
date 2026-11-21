#!/usr/bin/env python3
"""Auditoría conservadora del peso de nombres/descripciones MCP sobre un inventario previo.

No conecta servidores, no lee historiales de ChatGPT ni ejecuta herramientas MCP.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys


def validate_snapshot(data: object) -> list[dict]:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Inventario incompatible: se requiere schema_version=1")
    tools = data.get("tools")
    if not isinstance(tools, list) or not tools or len(tools) > 500:
        raise ValueError("Inventario de herramientas vacío o excesivo")
    names = set()
    for row in tools:
        if not isinstance(row, dict):
            raise ValueError("Registro de herramienta inválido")
        name, description, group = row.get("name"), row.get("description"), row.get("group")
        if not isinstance(name, str) or not name or not isinstance(description, str) or not isinstance(group, str) or not group:
            raise ValueError("Herramienta sin nombre, descripción o grupo")
        if name in names:
            raise ValueError("Herramienta duplicada")
        names.add(name)
    if data.get("total") != len(tools):
        raise ValueError("Recuento de inventario incongruente")
    return tools


def validate_usage(data: object, names: set[str]) -> tuple[dict[str, int], bool, str]:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Observaciones incompatibles")
    if not isinstance(data.get("complete"), bool):
        raise ValueError("Falta la indicación explícita de cobertura completa/incompleta")
    scope = data.get("scope")
    if not isinstance(scope, str) or not (4 <= len(scope) <= 120):
        raise ValueError("Ámbito de observación no válido")
    counts = data.get("counts")
    if not isinstance(counts, dict) or set(counts) - names:
        raise ValueError("Recuentos inválidos o nombres no inventariados")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 or value > 1000000 for value in counts.values()):
        raise ValueError("Los recuentos deben ser enteros no negativos")
    return counts, data["complete"], scope


def analyze(snapshot: dict, usage: dict | None = None) -> dict:
    rows = validate_snapshot(snapshot)
    names = {row["name"] for row in rows}
    counts: dict[str, int] = {}
    complete = False
    scope = None
    if usage is not None:
        counts, complete, scope = validate_usage(usage, names)
    groups: dict[str, dict] = defaultdict(lambda: {"tools": 0, "name_description_proxy_tokens": 0, "observed_calls": 0, "usage_known_tools": 0})
    details = []
    for row in rows:
        # Únicamente proxy de texto observado; los esquemas JSON no están en el inventario.
        proxy = (len(row["name"]) + len(row["description"]) + 3) // 4
        count = counts.get(row["name"])
        if count is None and complete:
            count = 0
        group = groups[row["group"]]
        group["tools"] += 1
        group["name_description_proxy_tokens"] += proxy
        if count is not None:
            group["observed_calls"] += count
            group["usage_known_tools"] += 1
        details.append({
            "name": row["name"], "group": row["group"],
            "name_description_proxy_tokens": proxy, "observed_calls": count,
            "observation": ("not_observed_in_scope" if count == 0 and complete else
                            "observed" if count is not None and count > 0 else "unknown"),
        })
    details.sort(key=lambda t: (-t["name_description_proxy_tokens"], t["name"]))
    total_proxy = sum(x["name_description_proxy_tokens"] for x in details)
    return {
        "source": {"captured_at": snapshot.get("captured_at"), "input_sha256": snapshot.get("input_sha256")},
        "scope": {"connector": snapshot.get("connector"), "usage_scope": scope, "usage_complete": complete},
        "summary": {"tools": len(rows), "name_description_proxy_tokens": total_proxy,
                    "tool_schema_tokens": None, "whole_context_tokens": None},
        "groups": dict(sorted(groups.items(), key=lambda pair: -pair[1]["name_description_proxy_tokens"])),
        "tools": details,
        "warnings": [
            "La cifra es solo un indicador longitud/4 de nombres y descripciones. No incluye esquemas JSON ni refleja tokens reales de contexto.",
            "Sin observación completa de la sesión, el uso desconocido NO significa herramienta no utilizada.",
            "Incluso una herramienta no observada puede ser crítica para recuperación, autenticación o seguridad.",
            "No desconectar herramientas ni cambiar el MCP automáticamente; validar dependencia y relevancia antes.",
        ],
    }


def render_markdown(report: dict, limit: int = 10) -> str:
    out = ["# Eficiencia MCP — diagnóstico no destructivo", ""]
    out.append(f"Fuente: {report['scope']['connector'] or 'desconocida'}; {report['summary']['tools']} herramientas.")
    out.append(f"Proxy nombres+descripciones: ~{report['summary']['name_description_proxy_tokens']} unidades (NO tokens reales del esquema o contexto).")
    out.append(f"Cobertura de observación: {'completa para el ámbito indicado' if report['scope']['usage_complete'] else 'incompleta o desconocida'}; ámbito: {report['scope']['usage_scope'] or 'sin observaciones'}.")
    out.extend(["", "## Grupos", "| Grupo | Herramientas | Proxy textual | Llamadas observadas |", "|---|---:|---:|---:|"])
    for group, values in report["groups"].items():
        calls = str(values["observed_calls"]) if values["usage_known_tools"] == values["tools"] else ("al menos " + str(values["observed_calls"]) if values["usage_known_tools"] else "sin datos")
        out.append(f"| {group} | {values['tools']} | {values['name_description_proxy_tokens']} | {calls} |")
    out.extend(["", "## Nombres/descripciones más extensos", "| Herramienta | Grupo | Proxy textual | Uso observado |", "|---|---|---:|---|"])
    for tool in report["tools"][:limit]:
        out.append(f"| {tool['name']} | {tool['group']} | {tool['name_description_proxy_tokens']} | {tool['observation']} |")
    out.extend(["", "## Límites"] + [f"- {warning}" for warning in report["warnings"]])
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path, help="inventario-mcp.json ya observado")
    parser.add_argument("--usage", type=Path, help="JSON opcional de observaciones explícitas (sin secretos)")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 100:
        parser.error("--limit debe estar entre 1 y 100")
    try:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        usage = json.loads(args.usage.read_text(encoding="utf-8")) if args.usage else None
        result = analyze(inventory, usage)
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(result, args.limit), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
