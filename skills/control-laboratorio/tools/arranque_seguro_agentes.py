#!/usr/bin/env python3
"""Lanzador optativo: nunca usa proveedores de pago por uso en Goose.

NO sustituye los comandos originales ni puede garantizar qué modelo se factura
mediante la cuenta ChatGPT. Para nuevos usos, verificar plan/entitlements aparte.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

SECRET_ENV = {"OPENAI_API_KEY", "GROQ_API_KEY", "ANTHROPIC_API_KEY",
              "OPENROUTER_API_KEY", "AZURE_OPENAI_API_KEY", "GOOGLE_API_KEY",
              "CODEX_HOME", "CODEX_OSS_BASE_URL", "CODEX_OSS_PORT"}


def plan(agent: str, model: str | None, home: Path) -> dict:
    if agent == "goose":
        if not model or not all(c.isalnum() or c in "._:/-" for c in model) or len(model) > 90:
            raise ValueError("Goose local requiere --model exacto y no vacío")
        command = ["goose", "session", "--max-turns", "8", "--max-tool-repetitions", "2", "--model", model]
        env_overrides = {"GOOSE_PROVIDER": "ollama", "GOOSE_MODE": "approve",
                         "GOOSE_DISABLE_SESSION_NAMING": "1", "GOOSE_MAX_TOKENS": "2048",
                         "OLLAMA_HOST": "127.0.0.1:11434",
                         "OLLAMA_BASE_URL": "http://127.0.0.1:11434"}
        requirements = ["ollama CLI y servidor local disponibles", "modelo instalado localmente"]
    elif agent == "codex":
        if model:
            raise ValueError("No seleccionar proveedores/modelos por esta vía de Codex")
        config = home / ".codex/config.toml"
        try:
            settings = tomllib.loads(config.read_text(encoding="utf8")) if config.exists() else {}
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ValueError(f"Configuración Codex no interpretable: {type(exc).__name__}") from exc
        if settings.get("model_provider") not in (None, "openai"):
            raise ValueError("Proveedor personalizado Codex no verificado")
        try:
            auth = __import__("json").loads((home / ".codex/auth.json").read_text(encoding="utf8"))
        except (OSError, ValueError) as exc:
            raise ValueError("Falta autenticación ChatGPT comprobable") from exc
        if auth.get("auth_mode") != "chatgpt":
            raise ValueError("Codex no está autenticado mediante ChatGPT; API de pago no autorizada")
        command = ["codex", "--sandbox", "workspace-write", "--ask-for-approval",
                   "on-request", "-c", "sandbox_workspace_write.network_access=false"]
        env_overrides = {}
        requirements = ["cuenta ChatGPT revisada; ninguna API de pago autorizada",
                        "las peticiones a modelos consumen cuota de la cuenta"]
    else:
        raise ValueError("Agente desconocido")
    return {"agent": agent, "command": command, "env_overrides": env_overrides,
            "remove_environment": sorted(SECRET_ENV),
            "requirements": requirements, "external_api_use": "disabled-for-goose, no-api-keys-for-codex",
            "limits": "Perfil optativo: ejecutar codex/goose originales elude esta protección; no controla otros MCP."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=("goose", "codex"))
    parser.add_argument("--model")
    parser.add_argument("--execute", action="store_true", help="Solo desde un terminal interactivo del usuario")
    args = parser.parse_args(argv)
    try:
        spec = plan(args.agent, args.model, Path.home())
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    if not args.execute:
        import json
        print(json.dumps(spec, ensure_ascii=False, indent=2))
        return 0
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("BLOCKED: requiere terminal interactivo, no ejecución desatendida", file=sys.stderr)
        return 2
    if not shutil.which(spec["command"][0]):
        print("BLOCKED: falta el ejecutable requerido", file=sys.stderr)
        return 2
    if args.agent == "goose" and not shutil.which("ollama"):
        print("BLOCKED: falta Ollama local", file=sys.stderr)
        return 2
    env = {k: v for k, v in os.environ.items() if k not in SECRET_ENV}
    env.update(spec["env_overrides"])
    return subprocess.call(spec["command"], env=env)


if __name__ == "__main__":
    sys.exit(main())
