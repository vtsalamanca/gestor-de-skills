#!/usr/bin/env python3
"""Auditoría estática propia de portabilidad de skills ChatGPT/Codex/Linux/Windows.

Es una inspección heurística; nunca ejecuta los ficheros inspeccionados ni usa red.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

PATTERNS = (
    ("home-hardcoded", re.compile(r"/home/[A-Za-z0-9_.-]+/"), "ruta Linux de usuario fija"),
    ("windows-user-hardcoded", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\s]+", re.I), "ruta Windows de perfil fija"),
    ("shell-pipe-execution", re.compile(r"\b(?:curl|wget)\b[^\n|]{0,150}\|\s*(?:sh|bash)\b"), "instalación remota ejecutada en shell"),
    ("paid-api-auto", re.compile(r"(?i)(?:automatically|automáticamente).{0,90}(?:paid api|api de pago|pay-per-use)"), "API facturable mencionada como automática"),
)
LINK = re.compile(r"\]\(((?:references|tools)/[^)#\s]+)(?:#[^)]*)?\)")
REQUIRED_SKILLS = {"organizaciondeltrabajo", "ingenieria-fiable", "acceso_webs",
    "buscar-comparar-productos", "bibliotecario-memoria", "descubrir-skills",
    "auditar-skills", "crear-skills", "integrar-skills", "inventariar-skills",
    "control-laboratorio"}


def check(root: Path, paths: list[Path] | None = None) -> dict:
    root = root.resolve(strict=True)
    findings = []
    manifest = root / ".codex-plugin/plugin.json"
    marketplace = root / ".agents/plugins/marketplace.json"
    try:
        version = json.loads(manifest.read_text(encoding="utf8"))["version"]
        other = json.loads(marketplace.read_text(encoding="utf8"))["plugins"][0]["version"]
        if version != other:
            findings.append({"file": "(manifests)", "line": 0, "rule": "version-mismatch", "severity": "error"})
    except (OSError, KeyError, IndexError, ValueError, TypeError):
        findings.append({"file": "(manifests)", "line": 0, "rule": "invalid-manifest", "severity": "error"})
        version = None
    folder = root / "skills"
    actual = {p.name for p in folder.iterdir() if p.is_dir()} if folder.exists() else set()
    if actual != REQUIRED_SKILLS:
        findings.append({"file": "skills", "line": 0, "rule": "skill-set-mismatch", "severity": "error"})
    if paths is None:
        paths = sorted(folder.rglob("*.md")) + sorted(folder.rglob("*.py"))
    scanned = 0
    for source in paths:
        p = (root / source).resolve()
        if not p.is_relative_to(root) or not p.is_file() or source.is_symlink():
            raise ValueError("Solo archivos regulares dentro del repositorio")
        relative = p.relative_to(root).as_posix()
        if p.suffix not in {".md", ".py", ".json"}:
            continue
        scanned += 1
        try:
            text = p.read_text(encoding="utf8")
        except (UnicodeError, OSError):
            findings.append({"file": relative, "line": 0, "rule": "read-error", "severity": "error"})
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for rule, rx, _ in PATTERNS:
                if rx.search(line):
                    findings.append({"file": relative, "line": n, "rule": rule, "severity": "warning"})
            if p.name == "SKILL.md" or p.suffix == ".md":
                for match in LINK.finditer(line):
                    target = (p.parent / match.group(1)).resolve()
                    if not target.is_relative_to(root) or not target.is_file():
                        findings.append({"file": relative, "line": n, "rule": "broken-link", "severity": "error"})
    return {"version": version, "scanned": scanned, "errors": sum(x["severity"] == "error" for x in findings),
            "warnings": sum(x["severity"] == "warning" for x in findings), "findings": findings,
            "limits": "Heurístico: no garantiza ejecutabilidad ni compatibilidad real en ChatGPT, Codex o Windows."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--fail-warnings", action="store_true")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.root, args.paths or None)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result["errors"] > 0 or (args.fail_warnings and result["warnings"] > 0))


if __name__ == "__main__":
    sys.exit(main())
