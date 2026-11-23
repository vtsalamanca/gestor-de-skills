#!/usr/bin/env python3
"""Generate a private, offline L4 dashboard from the official case bank."""

import argparse
from html import escape
import json
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "skills/control-laboratorio"
sys.path.insert(0, str(LAB / "tools"))
from eval_skill_routing import load_cases, score

CHAT_REF = re.compile(r"https://chatgpt\.com/c/[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}")


def read_jsonl(path):
    if path is None:
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def chat_rows(cases, attempts, observations, version, trace_root):
    case_ids = {case["id"] for case in cases}
    conversations = {}
    owners = {}

    def register(case_id, ref):
        if case_id not in case_ids or not isinstance(ref, str) or not CHAT_REF.fullmatch(ref):
            raise ValueError("Caso o enlace privado de ChatGPT inválido")
        if owners.get(ref, case_id) != case_id or conversations.get(case_id, ref) != ref:
            raise ValueError("La conversación debe ser distinta para cada caso")
        owners[ref] = case_id
        conversations[case_id] = ref

    for attempt in attempts:
        if attempt["caso"] in conversations:
            raise ValueError("Ejecución duplicada")
        register(attempt["caso"], attempt["ref"])

    reviewed = {}
    for row in observations:
        if row.get("observation_kind") != "verified_tool_trace":
            raise ValueError("La entrada revisada requiere trazas; use --attempts para informes y pilotos")
        register(row["id"], row.get("conversation_ref"))
        if row["id"] in reviewed:
            raise ValueError("Traza duplicada")
        reviewed[row["id"]] = row

    # Validate every reviewed record, including ones from a different release.
    validated = score(cases, list(reviewed.values()), version, trace_root)
    mismatches = set(validated["version_mismatches"])
    target = [row for key, row in reviewed.items() if key not in mismatches]
    result = score(cases, target, version, trace_root) if mismatches else validated
    details = {row["id"]: row for row in result["case_details"]}
    return result, conversations, reviewed, mismatches, details


def render(cases, attempts, observations, version, trace_root):
    result, chats, reviewed, mismatches, details = chat_rows(cases, attempts, observations, version, trace_root)
    rows = []
    for case in cases:
        key = case["id"]
        detail = details.get(key)
        if detail:
            state, label = "measured", "Verificado"
        elif key in mismatches:
            state, label = "other", "Otra versión"
        elif key in chats:
            state, label = "pilot", "Sin traza revisada"
        else:
            state, label = "pending", "Pendiente"
        ref = f'<a href="{escape(chats[key])}">Abrir chat</a>' if key in chats else "—"
        expected = escape(", ".join(case["expected_skills"]) or "Ninguna")
        loaded = escape(reviewed[key]["plugin_version"]) if key in reviewed else "—"
        errors = []
        if detail:
            for field, caption in (("false_positive", "Inesperadas"), ("false_negative", "Omitidas")):
                if detail[field]:
                    errors.append(f"{caption} · {escape(', '.join(detail[field]))}")
        findings = "<br>".join(errors) or ("Coincide" if detail else "—")
        rows.append(f'<tr data-state="{state}"><th scope="row">{escape(case["prompt"])}</th>'
                    f'<td>{expected}</td><td><span class="{state}">{label}</span></td>'
                    f'<td>{loaded}</td><td>{findings}</td><td>{ref}</td></tr>')

    def metric(value):
        return "Sin datos" if value is None else f"{value:.1%}"

    total, verified = len(cases), result["observed"]
    complete = result["independent_l4_validated"]
    verdict = ("Medición completa · revisar desvíos" if result["FP"] or result["FN"] else
               "Medición completa · coincide con el banco") if complete else "Homologación pendiente"
    counts = f'{result["TP"]} aciertos · {result["FP"]} inesperadas · {result["FN"]} omitidas' if verified else "Sin lecturas verificadas"
    return f"""<!doctype html>
<html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer"><title>Panel de homologación L4</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f6f9;color:#182332;font:16px system-ui,sans-serif}}
main{{max-width:1180px;margin:auto;padding:clamp(1rem,4vw,3rem)}} h1{{margin:.2em 0;font-size:clamp(2rem,5vw,3.5rem);letter-spacing:-.055em}}
p{{line-height:1.55}} .summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:25px 0}}
.summary div{{background:white;border:1px solid #dce3eb;border-radius:14px;padding:14px 18px}} dt{{color:#425467}}dd{{margin:6px 0 0;font-size:1.45rem;font-weight:700}}
.table{{overflow:auto;background:white;border:1px solid #dce3eb;border-radius:14px;margin-top:12px}}
table{{width:100%;border-collapse:collapse;text-align:left}}th,td{{padding:12px;vertical-align:top;border-bottom:1px solid #dce3eb}}
thead{{background:#182332;color:white}} tbody th{{min-width:230px;font-weight:550}} a{{color:#154e9b;white-space:nowrap}}
select{{font:inherit;margin-left:.5rem;padding:.35rem .45rem}} span{{white-space:nowrap}} .measured{{color:#196744}}.other,.pilot{{color:#854800}}
</style>
<main><h1>Homologación L4</h1><p><strong>{verdict}</strong> · Versión objetivo {escape(version)}</p>
<dl class="summary"><div><dt>Ejecutados</dt><dd>{len(chats)} / {total}</dd></div>
<div><dt>Verificados en la versión</dt><dd>{verified} / {total}</dd></div>
<div><dt>Precisión</dt><dd>{metric(result['precision'])}</dd></div><div><dt>Recuperación</dt><dd>{metric(result['recall'])}</dd></div></dl>
<p>{counts}. Para confirmar cada lectura, revisa la procedencia y la cobertura del turno en el registro original.</p>
<label>Mostrar <select id="state"><option value="">Todos los casos</option><option value="pending">Pendientes</option>
<option value="pilot">Sin traza revisada</option><option value="other">Otra versión</option><option value="measured">Verificados</option></select></label>
<div class="table" tabindex="0"><table><thead><tr><th>Petición</th><th>Habilidades esperadas</th><th>Evidencia</th>
<th>Versión</th><th>Resultado</th><th>Conversación</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></main>
<script>
const filter = document.querySelector('#state');
filter.addEventListener('change', () => {{
  for (const row of document.querySelectorAll('tbody tr')) {{
    row.hidden = filter.value !== '' && row.dataset.state !== filter.value;
  }}
}});
</script></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=LAB / "references/eval_cases.jsonl")
    parser.add_argument("--attempts", type=Path, help="JSONL de pilotos con los campos caso y ref")
    parser.add_argument("--reviewed-observations", type=Path,
                        help="JSONL del evaluador. Usar solo tras cotejar fuente original y cobertura completa del turno")
    parser.add_argument("--trace-root", type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        document = render(load_cases(args.cases), read_jsonl(args.attempts),
                          read_jsonl(args.reviewed_observations), args.version, args.trace_root)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output.parent, delete=False) as output:
        output.write(document)
    Path(output.name).replace(args.output)


if __name__ == "__main__":
    main()
