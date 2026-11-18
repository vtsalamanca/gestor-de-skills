#!/usr/bin/env python3
"""Selector genérico de modalidades; no navega, no se autentica ni evade controles."""
import argparse, json
from pathlib import Path
CATALOGO=Path(__file__).resolve().parents[1]/"references"/"modalidades.json"
def catalogo():
    data=json.loads(CATALOGO.read_text(encoding="utf-8"))
    m=data["modalidades"]
    ids=[x["id"] for x in m]
    if len(ids)!=len(set(ids)) or [x["orden"] for x in m]!=sorted(x["orden"] for x in m):
        raise ValueError("Catálogo duplicado o fuera de orden")
    required={"id","orden","nombre","coste","requisitos","confirma",
              "siguiente","senales","capacidad_requerida"}
    for row in m:
        if not required.issubset(row) or not isinstance(row["senales"],list) or not row["senales"]:
            raise ValueError("Modalidad incompleta: falta contrato de activación/verificación")
        if row["siguiente"] is not None and row["siguiente"] not in ids:
            raise ValueError("Modalidad apunta a alternativa inexistente")
    return data
def recomendar(senal, disponibles=None, datos=None):
    """Selecciona por reglas del catálogo; nuevos Mxx se reconocen sin añadir ifs.
    Una propuesta no supone acceso real, permiso automático ni navegación.
    """
    c=disponibles or {}
    tabla=datos or catalogo()
    if senal in tabla["detener"] or c.get("coste_no_autorizado"):
        return {"estado":"DETENER","senal":senal,"metodo":None}
    if senal in ("HTTP_401","SESION_CADUCADA"):
        return {"estado":"AUTENTICACION_REQUERIDA","metodo":None,"capa":"A10_AUTENTICACION"}
    for entry in tabla["modalidades"]:
        signs=entry.get("senales",[])
        cap=entry.get("capacidad_requerida")
        if "*" not in signs and senal not in signs:
            continue
        if cap and not c.get(cap):
            continue
        return {"estado":"PROPUESTA_SIN_VERIFICAR","senal":senal,
                "metodo":entry["id"],"requisitos":entry["requisitos"],
                "alternativa":entry["siguiente"]}
    return {"estado":"SIN_MODALIDAD","senal":senal,"metodo":None}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("senal")
    p.add_argument("--navegador-visual",action="store_true")
    p.add_argument("--navegador-dom",action="store_true")
    p.add_argument("--fuente-oficial",action="store_true")
    p.add_argument("--cache-vigente",action="store_true")
    p.add_argument("--inspeccion-autorizada",action="store_true")
    a=p.parse_args()
    print(json.dumps(recomendar(a.senal,vars(a)),ensure_ascii=False,indent=2))
