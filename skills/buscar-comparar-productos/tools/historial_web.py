"""Consultas de históricos ajenos, sin seguimiento ni almacenamiento propio."""
import html,re
from urllib.parse import urlsplit,quote
import requests

def _enlaces_base(oferta):
    url=oferta.get("url") or ""
    shop=oferta.get("tienda")
    if shop=="Amazon":
        m=re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})",url)
        if m:return [{"fuente":"Keepa","url":"https://keepa.com/#!product/9-"+m.group(1),"tipo":"grafico_externo_sin_consulta"}]
    if shop=="PcComponentes":
        ident=str(oferta.get("id_producto") or "").strip()
        if re.fullmatch(r"[0-9]{4,16}",ident):
            return [{"fuente":"PCComTracker","url":"https://pccomtracker.com/producto/ref-"+ident,"tipo":"historico_externo_sin_consulta"}]
    name=oferta.get("nombre_ficha") or oferta.get("nombre") or ""
    return [{"fuente":"idealo","url":"https://www.idealo.es/resultados.html?q="+quote(name[:110]),"tipo":"buscar_coincidencia_exacta"}]

def _eu(text):
    try:return float(text.replace(".","").replace(",","."))
    except ValueError:return None

def comprobar_pccom(oferta,session=None,timeout=5):
    links=enlaces(oferta)
    result={"estado":"NO_VERIFICADO","enlaces":links,
      "nota":"Fuente de terceros, no prueba del mínimo legal de 30 días"}
    if oferta.get("tienda")!="PcComponentes" or links[0]["fuente"]!="PCComTracker":
        return result
    url=links[0]["url"]
    try:
        response=(session or requests).get(url,timeout=timeout)
        if response.status_code!=200 or len(response.content)>300000:
            result["estado"]="FUENTE_NO_DISPONIBLE";return result
        text=response.text
        canon=re.search(r'<link rel="canonical" href="(https://pccomtracker\.com/producto/[^"]+)"',text)
        ident=str(oferta.get("id_producto"))
        if not canon or not canon.group(1).endswith("-"+ident):
            result["estado"]="IDENTIDAD_NO_CONFIRMADA";return result
        desc=re.search(r'<meta name="description" content="([^"]+)"',text)
        if not desc:
            result["estado"]="SIN_RESUMEN_HISTORICO";return result
        d=html.unescape(desc.group(1))
        minimum=re.search(r"mínimo del año\s+([\d.]+,\d{2})\s*€",d,re.I)
        if not minimum:
            result["estado"]="HISTORICO_NO_EXTRAIBLE";return result
        result.update(estado="MINIMO_ANUAL_EXTERNAMENTE_PUBLICADO",
            minimo_anual_eur=_eu(minimum.group(1)),
            fuente_url=canon.group(1),
            evidencia="metadatos públicos del comparador; puede estar desactualizado")
        current=oferta.get("precio_eur")
        hoy=re.search(r"Hoy\s+([\d.]+,\d{2})\s*€",d,re.I)
        if hoy and current is not None and abs(_eu(hoy.group(1))-float(current))>max(1,float(current)*0.01):
            result["advertencia_frescura"]="COTIZACION_EXTERNA_DIFIERE_DE_LA_TIENDA"
        if current is not None and float(current)>result["minimo_anual_eur"]*1.01:
            result["aviso"]="YA_EXISTIO_UN_PRECIO_ANUAL_INFERIOR"
        return result
    except requests.RequestException:
        result["estado"]="ERROR_CONSULTA_EXTERNA"
        return result

def incorporar(ofertas,verificar=False,max_comprobaciones=2):
    used=0
    for offer in ofertas:
        if verificar and used<max_comprobaciones and offer.get("tienda")=="PcComponentes" and offer.get("precio_eur") is not None:
            offer["historico_web"]=comprobar_pccom(offer)
            used+=1
        else:
            offer["historico_web"]={"estado":"ENLACES_EXTERNOS_SIN_CONSULTAR","enlaces":enlaces(offer)}
    return {"modalidad":"EXTERNA_SIN_BD","solicitudes_externas_maximas":max_comprobaciones if verificar else 0,
            "consultas_efectuadas":used}

def enlaces(oferta):
    """Enlaces gratuitos de consulta; no ejecuta búsquedas ni guarda precios."""
    from datetime import datetime, timedelta, timezone
    base=_enlaces_base(oferta)
    nombre=oferta.get("nombre_ficha") or oferta.get("nombre") or ""
    url=oferta.get("url_ficha_final") or oferta.get("url") or ""
    if nombre.strip():
        corte=(datetime.now(timezone.utc)-timedelta(days=30)).date()
        q=" ".join(nombre.replace('"',"").split()[:9])+" precio before:"+str(corte)
        base.append({"fuente":"Google: publicaciones antiguas",
            "url":"https://www.google.com/search?q="+quote(q),
            "tipo":"busqueda_fechada_no_prueba_de_precio"})
    p=urlsplit(url)
    if p.scheme=="https" and p.hostname and not p.username and not p.password:
        base.append({"fuente":"Wayback Machine",
            "url":"https://web.archive.org/web/*/"+p._replace(query="",fragment="").geturl(),
            "tipo":"copias_anteriores_si_existen"})
    return base
