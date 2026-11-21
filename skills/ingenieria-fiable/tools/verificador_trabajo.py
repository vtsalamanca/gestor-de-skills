#!/usr/bin/env python3
"""Verificador estático propio para cambios de agentes; nunca ejecuta archivos analizados."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import sys


def finding(path, line, level, rule):
    return {"file": str(path), "line": line, "severity": level, "rule": rule}


def placeholder(node):
    return (
        isinstance(node, ast.Pass)
        or isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis
        or isinstance(node, ast.Raise) and (
            isinstance(node.exc, ast.Name) and node.exc.id == "NotImplementedError"
            or isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name) and node.exc.func.id == "NotImplementedError"
        )
    )


def is_docstring(node):
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def is_abstract(node):
    for decorator in getattr(node, "decorator_list", ()):
        name = decorator.id if isinstance(decorator, ast.Name) else decorator.attr if isinstance(decorator, ast.Attribute) else ""
        if name in ("abstractmethod", "overload"):
            return True
    return False


def verifies(node):
    for inner in ast.walk(node):
        if isinstance(inner, ast.Assert):
            return True
        if isinstance(inner, ast.Call):
            func = inner.func
            if isinstance(func, ast.Attribute) and (func.attr.startswith("assert") or func.attr in ("raises", "warns", "fail")):
                return True
    return False


def scan_python(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    except (SyntaxError, UnicodeError, OSError) as exc:
        return [finding(path, getattr(exc, "lineno", 1) or 1, "critical", "parse-or-read-error")]
    issues = []
    is_test = path.name.startswith("test_") or path.name.endswith("_test.py")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body[1:] if node.body and is_docstring(node.body[0]) else node.body
            if (not body or all(placeholder(item) for item in body)) and not is_abstract(node):
                issues.append(finding(path, node.lineno, "critical", "function-stub"))
            if is_test and node.name.startswith("test_") and not verifies(node):
                issues.append(finding(path, node.lineno, "warning", "hollow-test"))
        elif isinstance(node, ast.ExceptHandler):
            if node.body and all(placeholder(item) for item in node.body):
                issues.append(finding(path, node.lineno, "warning", "swallowed-exception"))
        elif isinstance(node, ast.Call):
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else ""
            owner = fn.value.id if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) else ""
            if name == "breakpoint" or isinstance(fn, ast.Attribute) and fn.attr == "set_trace" and owner in ("pdb", "ipdb", "pytest"):
                issues.append(finding(path, node.lineno, "warning", "debugger"))
    return issues


def scan_js(path):
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (UnicodeError, OSError):
        return [finding(path, 1, "critical", "read-error")]
    issues = []
    for lineno, line in enumerate(lines, 1):
        if re.search(r"\bdebugger\s*;", line):
            issues.append(finding(path, lineno, "warning", "debugger"))
        if re.search(r"\b(?:it|test|describe)\.only\s*\(", line):
            issues.append(finding(path, lineno, "warning", "test-only"))
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--base", help="Git revision to compare with HEAD; scan only changed source files")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on", choices=("critical", "warning"), default="critical")
    args = parser.parse_args(argv)
    if not args.paths and not args.base:
        parser.error("indicar archivos o --base")
    paths = list(args.paths)
    if args.base:
        try:
            result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR", args.base, "HEAD", "--"], capture_output=True, text=True, check=True)
            paths += [Path(name) for name in result.stdout.splitlines()]
        except (subprocess.CalledProcessError, OSError) as exc:
            print(f"git diff failed: {exc}", file=sys.stderr)
            return 2
    issues = []
    scanned = 0
    for path in sorted(set(paths)):
        if not path.exists() and args.base:
            continue
        if path.suffix.lower() == ".py":
            issues.extend(scan_python(path))
        elif path.suffix.lower() in (".js", ".jsx", ".ts", ".tsx"):
            issues.extend(scan_js(path))
        else:
            continue
        scanned += 1
    issues.sort(key=lambda x: (x["file"], x["line"], x["rule"]))
    summary = {"scanned": scanned, "critical": sum(x["severity"] == "critical" for x in issues), "warning": sum(x["severity"] == "warning" for x in issues), "findings": issues}
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        for issue in issues:
            print(f'{issue["severity"].upper()}: {issue["file"]}:{issue["line"]} [{issue["rule"]}]')
        print(f'Analizados: {scanned}; críticos: {summary["critical"]}; avisos: {summary["warning"]}')
    return int(bool(summary["critical"] or args.fail_on == "warning" and summary["warning"]))


if __name__ == "__main__":
    sys.exit(main())
