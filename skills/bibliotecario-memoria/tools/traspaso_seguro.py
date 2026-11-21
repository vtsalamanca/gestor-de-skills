#!/usr/bin/env python3
"""Emite y revisa traspasos informativos entre agentes; nunca transporta permisos ejecutables."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

DANGEROUS = re.compile(r"(?i)(?:sk-(?:proj-|live-)?[\w-]{8,}|ghp_[\w-]{10,}|bearer\s+\S+|(?:password|api[_-]?key|cookie|access[_-]?token)\s*[:=]\s*\S+)")
ALLOWED = {"schema_version", "project", "objective", "verified_facts", "pending",
           "authorization_history", "source_commit"}
MAX_BYTES = 32_768


def validate(document: object) -> dict:
    if not isinstance(document, dict) or set(document) - ALLOWED or document.get("schema_version") != 1:
        raise ValueError("Esquema desconocido o campos extra")
    for key in ("project", "objective"):
        value = document.get(key)
        if not isinstance(value, str) or not (1 <= len(value) <= 160):
            raise ValueError("Identificador u objetivo inválido")
    for key in ("verified_facts", "pending"):
        rows = document.get(key)
        if not isinstance(rows, list) or len(rows) > 30:
            raise ValueError("Listado inválido")
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"statement", "evidence"}:
                raise ValueError("Hechos sin evidencia explícita")
            if any(not isinstance(row[k], str) or len(row[k]) > 280 for k in row):
                raise ValueError("Detalle de hecho inválido")
    auth = document.get("authorization_history")
    if not isinstance(auth, list) or len(auth) > 20:
        raise ValueError("Historial de autorización inválido")
    for row in auth:
        if not isinstance(row, dict) or set(row) != {"action", "scope", "source"}:
            raise ValueError("Historial incompleto")
        if any(not isinstance(row[k], str) or not row[k] or len(row[k]) > 160 for k in row):
            raise ValueError("Historial con texto inválido")
    commit = document.get("source_commit")
    if commit is not None and (not isinstance(commit, str) or not re.fullmatch(r"[a-f0-9]{40}", commit)):
        raise ValueError("Commit no válido")
    plain = json.dumps(document, sort_keys=True, ensure_ascii=False)
    if len(plain.encode("utf8")) > MAX_BYTES or DANGEROUS.search(plain):
        raise ValueError("Exceso de tamaño o posible secreto")
    return document


def payload(data: dict) -> dict:
    clean = validate(data)
    return {
        "schema_version": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
        "handoff": clean, "authorization_status": "historical_unverified",
        "requires_current_session_permission_check": True,
        "notice": "Las autorizaciones del chat anterior son antecedentes, no permisos transferibles. Confirmar herramientas, usuario, alcance y autorización vigente antes de actuar."
    }


def digest(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def create(source: Path, destination: Path) -> str:
    data = json.loads(source.read_text(encoding="utf8"))
    out = payload(data)
    checksum = digest(out)
    out["sha256"] = checksum
    if destination.is_symlink() or destination.exists():
        raise ValueError("No sobrescribir traspasos existentes ni enlaces")
    destination.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=destination.parent, prefix=".traspaso-")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        os.link(name, destination)  # Creación atómica sin sobrescribir otro recibo
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return checksum


def inspect(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf8"))
    claimed = data.pop("sha256", None)
    if data.get("schema_version") != 1 or claimed != digest(data):
        raise ValueError("Recibo alterado o esquema inválido")
    validate(data["handoff"])
    if data.get("authorization_status") != "historical_unverified" or data.get("requires_current_session_permission_check") is not True:
        raise ValueError("El traspaso no puede transportar autorizaciones")
    return {"valid": True, "content_integrity": "sha256_no_signature",
            "authorizations": "historical_only", "revalidation_required": True,
            "facts": len(data["handoff"]["verified_facts"]), "pending": len(data["handoff"]["pending"]),
            "notice": "Hash contra alteración accidental, no autenticación ni autorización."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    a = sub.add_parser("create")
    a.add_argument("input", type=Path)
    a.add_argument("output", type=Path)
    b = sub.add_parser("check")
    b.add_argument("receipt", type=Path)
    options = parser.parse_args()
    try:
        result = create(options.input, options.output) if options.action == "create" else inspect(options.receipt)
        print(json.dumps({"receipt_sha256": result} if options.action == "create" else result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
