#!/usr/bin/env python3
"""Auditoría local de políticas de Codex y Goose sin leer secretos ni usar modelos."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import tomllib


def parse_goose_public(path: Path) -> dict:
    """Lee solo tres campos conocidos: jamás devuelve credenciales ni otros valores."""
    if not path.is_file():
        return {}
    result = {}
    for line in path.read_text(encoding="utf8").splitlines():
        if line.startswith(" ") or line.startswith("\t") or line.lstrip().startswith("#"):
            continue
        found = re.fullmatch(r"([A-Za-z_]+):\s*([^#]*)\s*(?:#.*)?", line)
        if found and found.group(1) in {"GOOSE_MODE", "active_provider", "GOOSE_TELEMETRY_ENABLED"}:
            result[found.group(1)] = found.group(2).strip().strip("'\"").lower()
    return result


def inspect(home: Path) -> dict:
    home = home.resolve()
    evidence = []
    codex = home / ".codex/config.toml"
    try:
        config = tomllib.loads(codex.read_text(encoding="utf8")) if codex.is_file() else {}
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        config = {}
        evidence.append({"component": "codex", "rule": "invalid-config", "severity": "warning"})
    mode = config.get("sandbox_mode")
    approval = config.get("approval_policy")
    network = config.get("sandbox_workspace_write", {}).get("network_access")
    if mode == "danger-full-access":
        evidence.append({"component": "codex", "rule": "unsandboxed", "severity": "critical"})
    if approval == "never":
        evidence.append({"component": "codex", "rule": "no-approvals", "severity": "critical"})
    if network is True:
        evidence.append({"component": "codex", "rule": "agent-network-enabled", "severity": "warning"})
    if mode is None or approval is None:
        evidence.append({"component": "codex", "rule": "implicit-defaults", "severity": "info"})
    goose = parse_goose_public(home / ".config/goose/config.yaml")
    goose_mode = goose.get("GOOSE_MODE")
    if goose_mode in (None, "auto"):
        evidence.append({"component": "goose", "rule": "autonomous-or-default-mode", "severity": "warning"})
    provider = goose.get("active_provider", "")
    remote = bool(provider) and not any(provider == x for x in ("ollama", "local", "llamacpp", "llama.cpp"))
    if remote:
        evidence.append({"component": "goose", "rule": "external-provider-configured", "severity": "warning"})
    if not provider:
        evidence.append({"component": "goose", "rule": "provider-unknown", "severity": "info"})
    return {
        "codex": {"sandbox": mode or "unspecified", "approval": approval or "unspecified",
                  "network": "enabled" if network is True else ("disabled" if network is False else "unspecified")},
        "goose": {"mode": goose_mode or "unspecified", "provider_category": "external" if remote else ("local" if provider else "unknown")},
        "findings": evidence,
        "budget": "No se ha ejecutado modelo, consulta API ni gasto. Los ficheros originales permanecen intactos.",
        "limitations": "Solo configuración declarada; no observa permisos efectivos MCP, modelo en ejecución, facturación ni agentes lanzados fuera de perfiles seguros."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    a = parser.parse_args()
    report = inspect(a.home)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
