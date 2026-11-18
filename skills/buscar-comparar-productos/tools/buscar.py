#!/usr/bin/env python3
"""Búsqueda real de portátiles desde Debian, con fuentes verificables y sin compras.
Python stdlib + requests (instalado); nunca usa credenciales ni servicios de pago.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html import unescape
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlencode
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept-Language": "es-ES,es;q=0.9",
}
HOSTS = {"www.amazon.es": "Amazon", "www.elcorteingles.es": "El Corte Inglés",
         "www.pccomponentes.com": "PcComponentes", "www.mediamarkt.es": "MediaMarkt",
         "www.fnac.es": "Fnac"}
BLOCK_MARKERS = ("just a moment...", "checking your browser", "captcha", "access denied")
GPU_RE = re.compile(r"\bRTX[\s™®]*(4060|5050|5060)\b", re.I)

def plain(value):
    return unescape(re.sub(r"<[^>]*>", " ", value or "")).strip()

def normalize(s):
    return re.sub(r"\s+", " ", unescape(s or "")).strip()

def money(raw):
    """Convierte formato europeo de euros a Decimal, sin redondear precios desconocidos."""
    value = re.sub(r"[^0-9,.]", "", normalize(raw))
    if not value:
        return None
    if "," in value:
        value = value.replace(".", "").replace(",", ".")
    elif value.count(".") > 1 or re.fullmatch(r"\d{1,3}\.\d{3}", value):
        value = value.replace(".", "")
    try:
        return Decimal(value)
    except InvalidOperation:
        return None

def as_number(title, field):
    t = normalize(title)
    if field == "ram":
        pats = [r"(?<!\d)(\d{1,3})\s*GB\s*(?:de\s+)?RAM\b",
                r"\bRAM\s*(?:de\s*)?(\d{1,3})\s*GB\b"]
    else:
        pats = [r"(?<!\d)(\d+(?:[,.]\d+)?)\s*(TB|GB)\s*(?:de\s*)?(?:SSD|NVME)\b",
                r"\b(?:SSD|NVME)\s*(?:de\s*)?(\d+(?:[,.]\d+)?)\s*(TB|GB)\b"]
    for p in pats:
        m = re.search(p, t, re.I)
        if m:
            if field == "ram":
                return int(m.group(1))
            n = float(m.group(1).replace(",", "."))
            return int(n * (1024 if m.group(2).upper() == "TB" else 1))
    if field == "ram":
        # Las fichas españolas suelen escribir "16GB, 512GB SSD" sin la palabra RAM.
        # Nunca inferir RAM del bloque de VRAM adyacente a "RTX 5050 8GB".
        for m in re.finditer(r"(?<!\d)(\d{1,3})\s*GB\b", t, re.I):
            before=t[max(0,m.start()-16):m.start()]
            after=t[m.end():m.end()+18]
            if re.search(r"\bRTX\s*\d{4}\s*$",before,re.I) or re.search(r"^\s*(?:SSD|NVME|GDDR|VRAM)\b",after,re.I):
                continue
            value=int(m.group(1))
            if 8<=value<=128:
                return value
    return None

def features(title):
    title = normalize(title)
    gpu = GPU_RE.search(title)
    hz = re.search(r"(?<!\d)(\d{2,3})\s*Hz\b", title, re.I)
    keyboard = bool(re.search(r"(QWERTY\s*espa[nñ]ol|teclado\s*(?:ES|espa[nñ]ol))", title, re.I))
    return {
        "gpu": "RTX " + gpu.group(1) if gpu else None,
        "ram_gb": as_number(title, "ram"),
        "ssd_gb": as_number(title, "ssd"),
        "hz": int(hz.group(1)) if hz else None,
        "teclado_es_explicito": keyboard,
    }

def card(src, name, url, require_gpu=True, **extras):
    if urlsplit(url).hostname not in HOSTS:
        return None
    if require_gpu and not GPU_RE.search(name):
        return None
    return {"tienda": src, "nombre": normalize(name), "url": url, **features(name), **extras}

def parse_amazon_results(html, require_gpu=True):
    matches = list(re.finditer(r'<div\b(?=[^>]*data-asin="([A-Z0-9]{10})")(?=[^>]*data-component-type="s-search-result")[^>]*>', html, re.I))
    out = []
    seen = set()
    for i, m in enumerate(matches):
        asin = m.group(1)
        if asin in seen:
            continue
        seg = html[m.start():matches[i+1].start() if i+1 < len(matches) else m.start()+35000]
        h = re.search(r"<h2\b[^>]*aria-label=\"([^\"]+)\"", seg, re.I|re.S)
        if h:
            name = unescape(h.group(1))
        else:
            h = re.search(r"<h2\b[^>]*>(.*?)</h2>", seg, re.I|re.S)
            if not h:
                continue
            name = normalize(plain(h.group(1)))
        if not name:
            continue
        sponsored = bool(re.search(r"^Anuncio patrocinado:", name, re.I))
        name = re.sub(r"^Anuncio patrocinado:\s*", "", name, flags=re.I)
        # Precio del índice solo ayuda a decidir qué ficha visitar: nunca confirma la oferta.
        tail = seg[h.end():h.end()+16000]
        pm = re.search(r'class="a-offscreen"[^>]*>\s*([0-9.,]+\s*€)', tail, re.I)
        idxprice = money(pm.group(1)) if pm else None
        item = card("Amazon", name, "https://www.amazon.es/dp/" + asin,
                    fuente_descubrimiento="busqueda_merchant", id_producto=asin,
                    require_gpu=require_gpu, patrocinado=sponsored,
                    precio_indice_eur=float(idxprice) if idxprice is not None else None)
        if item:
            seen.add(asin)
            out.append(item)
    return out

def parse_eci_results(html, require_gpu=True):
    out = []
    for segment in re.findall(r"<article\b[^>]*>.*?</article>", html, re.I|re.S):
        m = re.search(r'class="product_preview-title[^"]*"[^>]*title="([^"]+)"[^>]*href="([^"]+)"', segment, re.I|re.S)
        if not m:
            continue
        url = urljoin("https://www.elcorteingles.es", unescape(m.group(2)))
        item = card("El Corte Inglés", m.group(1), url, require_gpu=require_gpu, fuente_descubrimiento="busqueda_merchant")
        if item:
            out.append(item)
    return out

def parse_media_results(html, require_gpu=True):
    """MediaMarkt: el listado usa schema.org ItemList en HTML público."""
    out = []
    for m in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.I|re.S):
        try:
            obj=json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if not isinstance(obj,dict) or obj.get("@type")!="ItemList":
            continue
        for entry in obj.get("itemListElement", []):
            p=entry.get("item",{})
            if not isinstance(p,dict) or p.get("@type")!="Product":
                continue
            offer=p.get("offers",{})
            if isinstance(offer,list):
                offer=offer[0] if offer else {}
            price=money(str(offer.get("price",""))) if offer.get("priceCurrency")=="EUR" else None
            row=card("MediaMarkt",p.get("name",""),p.get("url",""),
                     require_gpu=require_gpu, fuente_descubrimiento="schema_itemlist",
                     precio_indice_eur=float(price) if price is not None else None)
            if row: out.append(row)
    return out

def media_detail(html):
    """MediaMarkt: la ficha usa JSON-LD BuyAction.object.Product, no Product raíz."""
    product=None
    for m in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',html,re.I|re.S):
        try:
            obj=json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if not isinstance(obj,dict):
            continue
        candidate=obj.get("object") if obj.get("@type")=="BuyAction" else obj
        if isinstance(candidate,dict) and candidate.get("@type")=="Product":
            product=candidate
            break
    if not product:
        return {"nombre_ficha":None,"precio_eur":None,"stock":None,"error_detalle":"MEDIA_SIN_PRODUCTO"}
    offer=product.get("offers",{})
    if isinstance(offer,list):
        offer=offer[0] if offer else {}
    price=money(str(offer.get("price",""))) if offer.get("priceCurrency")=="EUR" else None
    availability=offer.get("availability","")
    if not isinstance(availability,str):
        availability=""
    details=offer.get("shippingDetails",{})
    if isinstance(details,list):details=details[0] if details else {}
    if not isinstance(details,dict):details={}
    shipping=details.get("shippingRate",{})
    if not isinstance(shipping,dict):shipping={}
    raw_rate=shipping.get("value")
    free_generic=(raw_rate==0 or raw_rate=="0" or
                  re.search(r'IVA incl\. Con env[ií]o gratis',html,re.I) is not None)
    # Especificaciones del producto de la ficha, no del buscador ni de un anuncio.
    # Solo usar un dato si todas las apariciones del campo coinciden: los SSR pueden
    # contener recomendaciones y referencias a otros artículos en la caché GraphQL.
    hz_values={int(x) for x in re.findall(
        r'"name":"Frecuencia de actualización","type":null,"unit":"Hz","value":"(\d{2,3})"',html)}
    kb_values=set(re.findall(
        r'"name":"Tipo de teclado","type":null,"unit":null,"value":"([^"]{1,160})"',html))
    country_values=set(re.findall(
        r'"name":"Distribución del teclado \(por país\)","type":null,"unit":null,"value":"([A-Z]{2})"',html))
    hz_verified=next(iter(hz_values)) if len(hz_values)==1 else None
    kb_verified=(len(kb_values)==1 and any(re.search(r'espa[nñ]ol',x,re.I) for x in kb_values)
                 or country_values=={"ES"})
    return {"nombre_ficha":normalize(product.get("name","")),
            "especificaciones_ficha":{"hz":hz_verified,"teclado_es_explicito":bool(kb_verified)},
            "fuente_especificaciones":"caracteristicas_media_ssr_si_univocas",
            "precio_eur":float(price) if price is not None else None,
            "stock":True if "InStock" in availability else (False if "OutOfStock" in availability else None),
            "stock_texto":availability,
            "condicion":offer.get("itemCondition"),
            "envio_general_gratis_indicio":bool(free_generic),
            "envio_a_destino_verificado":False,
            "garantia_verificada":False}

def classify_empty_result(shop, html):
    """Un HTML accesible sin productos extraídos no acredita búsqueda vacía."""
    hint={"Amazon":'data-component-type="s-search-result"',
          "El Corte Inglés":'class="product_preview-title',
          "MediaMarkt":'"@type":"ItemList"'}[shop]
    if hint in html:
        return "EXTRACCION_FALLIDA_CON_TARJETAS"
    if re.search(r'no se han encontrado resultados|no hay resultados|0 resultados',html,re.I):
        return "SIN_RESULTADOS_DECLARADOS"
    return "RESPUESTA_SIN_CATALOGO_VERIFICABLE"

def get(session, url, timeout=13):
    allowed = urlsplit(url).hostname
    if allowed not in HOSTS:
        return None, "DOMINIO_NO_AUTORIZADO"
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True)
    except requests.RequestException as e:
        return None, "RED:" + type(e).__name__
    if urlsplit(response.url).hostname not in HOSTS:
        return None, "REDIRECCION_NO_AUTORIZADA"
    if response.status_code != 200:
        return None, "HTTP_" + str(response.status_code)
    if any(x in response.text[:10000].lower() for x in BLOCK_MARKERS):
        return None, "PROTECCION_WEB"
    return response, None

def amazon_detail(html):
    name = re.search(r'<meta\s+name="title"\s+content="([^"]+)"', html, re.I)
    if not name:
        name = re.search(r"<title>(.*?)</title>", html, re.S|re.I)
    name = normalize(name.group(1).split(" : Amazon.es")[0]) if name else None
    price_segment = re.search(r'class="[^"]*apex-pricetopay-value[^"]*"[^>]*>(.{0,650})', html, re.I|re.S)
    pm = re.search(r'class="a-offscreen"[^>]*>\s*([^<]+)', price_segment.group(1), re.I) if price_segment else None
    price = money(pm.group(1)) if pm else None
    availability = re.search(r'id="availability"[^>]*>(.{0,1000})', html, re.I|re.S)
    atext = normalize(plain(availability.group(1)))[:160] if availability else ""
    in_stock = bool(re.search(r"\bEn stock\b", atext, re.I))
    sold_out = bool(re.search(r"no disponible|agotado|sin existencias", atext, re.I))
    delivery = re.search(r'data-csa-c-delivery-price="([^"]+)"', html, re.I)
    return {"nombre_ficha": name, "precio_eur": float(price) if price is not None else None,
            "stock": True if in_stock else (False if sold_out else None),
            "stock_texto": atext, "envio_general_gratis_indicio": bool(delivery and delivery.group(1).upper()=="GRATIS"),
            "envio_a_destino_verificado": False, "garantia_verificada": False}

def eci_detail(html):
    match = re.search(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.I|re.S)
    product = None
    for m in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.I|re.S):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        objs = obj if isinstance(obj, list) else [obj]
        for p in objs:
            if isinstance(p, dict) and (p.get("@type") == "Product" or "Product" in p.get("@type", [])):
                product = p
                break
        if product:
            break
    if not product:
        return {"nombre_ficha": None, "precio_eur": None, "stock": None, "error_detalle": "JSON_LD_SIN_PRODUCTO"}
    offers = product.get("offers", {})
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    price = money(str(offers.get("price", ""))) if offers.get("priceCurrency")=="EUR" else None
    stock = offers.get("availability", "")
    return {"nombre_ficha": normalize(product.get("name", "")),
            "precio_eur": float(price) if price is not None else None,
            "stock": True if "InStock" in stock else (False if "OutOfStock" in stock else None),
            "stock_texto": stock, "envio_general_gratis_indicio": False,
            "envio_a_destino_verificado": False, "garantia_verificada": False}

def assess(item, budget, min_ram=16, min_ssd=512, min_hz=144, require_keyboard=True, profile="portatil-gaming", product_query="", must=()):
    title = item.get("nombre_ficha") or item.get("nombre", "")
    values = features(title)
    direct = item.get("especificaciones_ficha", {})
    for field in ("hz","teclado_es_explicito"):
        verified=direct.get(field)
        if verified is not None and verified is not False:
            if values[field] not in (None, False, verified):
                # La ficha contradice el nombre: tratar como desconocido.
                values[field]=None if field=="hz" else False
                item["conflicto_especificaciones"]=field
            else:
                values[field]=verified
    item.update(values)
    reasons = []
    unknown = []
    if profile == "portatil-gaming":
        if not values["gpu"]: reasons.append("GPU_INCOMPATIBLE")
        if values["ram_gb"] is None: unknown.append("RAM")
        elif values["ram_gb"] < min_ram: reasons.append("RAM_INSUFICIENTE")
        if values["ssd_gb"] is None: unknown.append("SSD")
        elif values["ssd_gb"] < min_ssd: reasons.append("SSD_INSUFICIENTE")
        if values["hz"] is None: unknown.append("HZ")
        elif values["hz"] < min_hz: reasons.append("HZ_INSUFICIENTES")
        if require_keyboard and not values["teclado_es_explicito"]: unknown.append("TECLADO_ES")
    else:
        text = normalize(title).lower()
        terms = [w.lower() for w in re.findall(r"[a-záéíóúüñ0-9]+",product_query,re.I)
                 if len(w)>3 and w.lower() not in {"para","gaming","con","de","color","negro"}]
        if terms and sum(t in text for t in terms)*2<len(terms):
            reasons.append("NO_COINCIDE_BUSQUEDA")
        for required in must:
            if required.lower() not in text: unknown.append("REQUISITO_NO_VERIFICADO:"+required)
    if item.get("stock") is False: reasons.append("AGOTADO")
    elif item.get("stock") is None: unknown.append("STOCK")
    price = item.get("precio_eur")
    if price is None: unknown.append("PRECIO")
    elif price > budget: reasons.append("FUERA_DE_PRESUPUESTO")
    if not item.get("envio_a_destino_verificado"): unknown.append("ENVIO_DESTINO_Y_COSTE_TOTAL")
    if not item.get("garantia_verificada"): unknown.append("GARANTIA")
    item["incumplimientos"] = reasons
    item["pendientes"] = unknown
    item["estado"] = "DESCARTADO" if reasons else ("COMPRABLE_VERIFICADO" if not unknown else "CANDIDATO_PENDIENTE")
    return item

def pccomponentes_por_acceso_webs(queries, args):
    """Fallback real 403 → Firefox ESR en X11, utilizando la skill compartida acceso_webs.
    Una sola pestaña de navegador y páginas renderizadas; nada de cookies externas.
    """
    import sys
    from urllib.parse import quote
    shared=Path(__file__).resolve().parents[2]/"acceso_webs"/"tools"
    if str(shared) not in sys.path:
        sys.path.insert(0,str(shared))
    from navegador_visual import FirefoxVisual, AccesoVisualError
    from pccomponentes_adapter import search_cards, detail as detail_pc

    rows=[]
    candidates=[]
    checked=[]
    try:
        with FirefoxVisual(allowed_hosts=("www.pccomponentes.com","pccomponentes.com")) as browser:
            for query in queries:
                url="https://www.pccomponentes.com/search/?query="+quote(query)
                row={"tienda":"PcComponentes","consulta":query,"url":url,"resultado":"PENDIENTE"}
                try:
                    page=browser.read(url,expected=lambda t: 'data-product-list="Search results /' in t or
                                       re.search(r'no hay resultados|0 artículos',t,re.I) is not None)
                    items=search_cards(page["html"])
                    new=[]
                    for item in items:
                        raw=money(item.get("price_text") or "")
                        c=card("PcComponentes",item["name"],item["url"],
                               require_gpu=args.perfil=="portatil-gaming",
                               fuente_descubrimiento="firefox_esr_x11_html_renderizado",
                               id_producto=item.get("product_id"),
                               vendedor=item.get("seller"),
                               condicion_listado=item.get("condition"),
                               precio_indice_eur=float(raw) if raw is not None else None)
                        if c:new.append(c)
                    candidates.extend(new)
                    row.update(resultado="EXTRACCION_GUI_VERIFICADA" if new else "SIN_ARTICULOS_COMPATIBLES",
                               encontrados=len(new),metodo=page["metodo"])
                except AccesoVisualError as e:
                    row.update(resultado="BLOQUEADO_VISUAL_"+e.code,encontrados=0)
                rows.append(row)
            # Cupo proporcional: una ficha por GPU, después ofertas de menor precio.
            # Evitar decenas de navegaciones y no usar precios de índice como actuales.
            chosen=[]
            if args.perfil=="portatil-gaming":
                for g in args.gpus:
                    options=[x for x in candidates if x["gpu"]=="RTX "+g]
                    if options:
                        options.sort(key=lambda x:x.get("precio_indice_eur") or 999999)
                        if options[0]["url"] not in {z["url"] for z in chosen}:
                            chosen.append(options[0])
            rest=sorted(candidates,key=lambda x:x.get("precio_indice_eur") or 999999)
            for it in rest:
                if len(chosen)>=min(args.max_fichas_por_tienda,5):break
                if it["url"] not in {z["url"] for z in chosen}:chosen.append(it)
            for it in chosen:
                clone=it.copy()
                clone["consultado_utc"]=datetime.now(timezone.utc).isoformat(timespec="seconds")
                try:
                    page=browser.read(it["url"],expected=lambda t:'pdp-price-current-integer' in t)
                    clone.update(detail_pc(page["html"]))
                    clone["metodo_detalle"]=page["metodo"]
                    clone["url_ficha_final"]=page["url"]
                    if clone["nombre_ficha"] and it.get("id_producto") and not it["url"].endswith(urlsplit(page["url"]).path.split("/")[-1]):
                        clone["error_detalle"]="IDENTIDAD_URL_NO_COINCIDE"
                        clone["precio_eur"]=None
                    # Ningún atributo de recomendaciones o accesorios acredita stock del artículo.
                except AccesoVisualError as e:
                    clone.update(error_detalle="BLOQUEADO_VISUAL_"+e.code,
                                 nombre_ficha=None,precio_eur=None,stock=None,
                                 envio_a_destino_verificado=False,garantia_verificada=False)
                checked.append(assess(clone,args.presupuesto,min_hz=args.min_hz,
                                     require_keyboard=args.teclado_es,profile=args.perfil,
                                     product_query=args.producto,must=args.debe_contener))
    except AccesoVisualError as e:
        if not rows:
            rows=[{"tienda":"PcComponentes","consulta":q,
                   "resultado":"BLOQUEADO_VISUAL_"+e.code,"encontrados":0} for q in queries]
    return rows,candidates,checked

def elegir_modalidad_publica(senal, visual_disponible):
    """Consulta el catálogo genérico de acceso_webs, no reglas ad hoc por comercio."""
    import sys
    compartido=Path(__file__).resolve().parents[2]/"acceso_webs"/"tools"
    if str(compartido) not in sys.path:sys.path.insert(0,str(compartido))
    from selector_metodos import recomendar
    return recomendar(senal,{"navegador_visual":bool(visual_disponible)})

def pccomponentes_por_http(session, url, response, args):
    """Solo si el HTTP público contiene productos reales; costes menores que Firefox."""
    from pccomponentes_adapter import search_cards, detail as detail_pc
    items=search_cards(response.text)
    parsed=[]
    for item in items:
        price=money(item.get("price_text") or "")
        c=card("PcComponentes",item["name"],item["url"],
               require_gpu=args.perfil=="portatil-gaming",
               fuente_descubrimiento="http_publico_html",
               vendedor=item.get("seller"),id_producto=item.get("product_id"),
               condicion_listado=item.get("condition"),
               precio_indice_eur=float(price) if price is not None else None)
        if c:parsed.append(c)
    by_url={r["url"]:r for r in parsed}
    chosen=sorted(by_url.values(),key=lambda v:v.get("precio_indice_eur") or 999999)[:min(args.max_fichas_por_tienda,5)]
    verified=[]
    for item in chosen:
        r=item.copy()
        r["consultado_utc"]=datetime.now(timezone.utc).isoformat(timespec="seconds")
        page,err=get(session,item["url"])
        if page and "pdp-price-current-integer" in page.text:
            r.update(detail_pc(page.text))
            r["metodo_detalle"]="http_publico_html"
        else:
            r.update(nombre_ficha=None,precio_eur=None,stock=None,
                     error_detalle=err or "SIN_PRECIO_PDP",
                     envio_a_destino_verificado=False,garantia_verificada=False)
        verified.append(assess(r,args.presupuesto,min_hz=args.min_hz,
                             require_keyboard=args.teclado_es,profile=args.perfil,
                             product_query=args.producto,must=args.debe_contener))
    row={"tienda":"PcComponentes","consulta":args.producto if args.perfil=="general" else "portatil rtx 5050",
         "url":url,"resultado":"HTTP_PUBLICO_EXTRAIDO","encontrados":len(by_url),
         "metodo":"M20_HTTP_PUBLICO"}
    return [row],list(by_url.values()),verified

def run(args, transport=None):
    session = transport or requests.Session()
    session.headers.update(HEADERS)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    raw = []
    searches = []
    queries = [f"portatil gaming rtx {gpu}" for gpu in args.gpus] if args.perfil=="portatil-gaming" else [args.producto]
    for shop in ("Amazon","El Corte Inglés","MediaMarkt"):
        for query in queries:
            url = ("https://www.amazon.es/s?" + urlencode({"k":query}) if shop=="Amazon" else
                   "https://www.elcorteingles.es/search/?" + urlencode({"s":query}) if shop=="El Corte Inglés" else
                   "https://www.mediamarkt.es/es/search.html?" + urlencode({"query":query}))
            response, err = get(session, url)
            row = {"tienda":shop,"consulta":query,"url":url,"resultado":"OK" if response else err}
            if response:
                found = (parse_amazon_results(response.text,require_gpu=args.perfil=="portatil-gaming") if shop=="Amazon"
                         else parse_eci_results(response.text,require_gpu=args.perfil=="portatil-gaming") if shop=="El Corte Inglés"
                         else parse_media_results(response.text,require_gpu=args.perfil=="portatil-gaming"))
                row["encontrados"] = len(found)
                if not found:
                    # HTTP 200 no significa que un catálogo se haya extraído.
                    row["resultado"] = classify_empty_result(shop,response.text)
                raw.extend(found)
            searches.append(row)
    # PcComponentes: primero HTTP directo; ante 403 no repetir peticiones.
    # De manera predeterminada, se activa la recuperación visual documentada en acceso_webs.
    pc_verified=[]
    from urllib.parse import quote
    probe = args.producto if args.perfil=="general" else "portatil rtx 5050"
    pc_url="https://www.pccomponentes.com/search/?query="+quote(probe)
    pc_response,pc_err=get(session,pc_url,timeout=9)
    from pccomponentes_adapter import search_cards
    http_extraible=bool(pc_response and search_cards(pc_response.text))
    senal=("HTTP_200_CON_DATOS" if http_extraible else
           "HTTP_403_DESAFIO" if pc_err=="HTTP_403" else
           "HTTP_200_SIN_DATOS" if pc_response else
           "TRANSPORTE_FALLIDO")
    plan=elegir_modalidad_publica(senal,args.visual_fallback)
    if plan["metodo"]=="M20_HTTP_PUBLICO" and http_extraible:
        pc_rows,pc_items,pc_verified=pccomponentes_por_http(session,pc_url,pc_response,args)
        searches.extend(pc_rows)
        raw.extend(pc_items)
    elif plan["metodo"]=="M50_NAVEGADOR_VISUAL":
        pc_rows,pc_items,pc_verified=pccomponentes_por_acceso_webs(queries,args)
        for row in pc_rows:row["metodo_seleccionado"]="M50_NAVEGADOR_VISUAL"
        searches.extend(pc_rows)
        raw.extend(pc_items)
    else:
        searches.append({"tienda":"PcComponentes","consulta":probe,"url":pc_url,
                         "resultado":pc_err or "EXTRACCION_NO_DEMOSTRADA",
                         "metodo_seleccionado":plan.get("metodo"),
                         "detalle_seleccion":plan["estado"]})
    fnac_url="https://www.fnac.es/SearchResult/ResultList.aspx?Search="+quote(probe)
    fnac_response,fnac_err=get(session,fnac_url,timeout=9)
    searches.append({"tienda":"Fnac","consulta":probe,"url":fnac_url,
                     "resultado":"RESPONDE_SIN_ADAPTADOR" if fnac_response else fnac_err})
    unique={}
    for item in raw:
        unique.setdefault(item["url"], item)
    found=list(unique.values())
    # Cuotas de descubrimiento por GPU y tienda: evita explorar solo RTX 5060 caras.
    selected=[]
    for shop in ("Amazon","El Corte Inglés","MediaMarkt"):
        pool=[x for x in found if x["tienda"]==shop]
        quota=args.max_fichas_por_tienda
        selected_shop=[]
        for j,gpu in enumerate(args.gpus if args.perfil=="portatil-gaming" else ["general"]):
            group=[x for x in pool if x["gpu"]=="RTX "+gpu] if args.perfil=="portatil-gaming" else pool
            group.sort(key=lambda x:(x.get("precio_indice_eur") is None,
                                     x.get("precio_indice_eur") is not None and x["precio_indice_eur"]>args.presupuesto,
                                     x.get("precio_indice_eur") or 999999))
            remaining=quota-len(selected_shop)
            groups=len(args.gpus) if args.perfil=="portatil-gaming" else 1
            slots=max(1,quota//groups) if j<groups-1 else remaining
            selected_shop.extend(x for x in group[:max(0,min(slots,remaining))] if x["url"] not in {z["url"] for z in selected_shop})
        if len(selected_shop)<quota:
            selected_shop.extend(x for x in pool if x["url"] not in {z["url"] for z in selected_shop})
        selected.extend(selected_shop[:quota])
    def detail(item):
        clone=item.copy()
        response,err=get(session,clone["url"])
        clone["consultado_utc"]=datetime.now(timezone.utc).isoformat(timespec="seconds")
        clone["fecha_http"]=response.headers.get("Date") if response else None
        if err:
            clone.update({"error_detalle":err,"precio_eur":None,"stock":None,
                          "envio_a_destino_verificado":False,"garantia_verificada":False})
        else:
            clone.update(amazon_detail(response.text) if clone["tienda"]=="Amazon" else
                         eci_detail(response.text) if clone["tienda"]=="El Corte Inglés" else media_detail(response.text))
            # La fecha de respuesta HTTP es una comprobación mínima, nunca prueba de frescura de todo el catálogo.
            # Si el servidor entrega explícitamente una respuesta antigua, no certificar precio ni stock.
            from email.utils import parsedate_to_datetime
            try:
                age = (datetime.now(timezone.utc)-parsedate_to_datetime(response.headers["Date"])).total_seconds()
            except (KeyError, ValueError, TypeError):
                age = None
            clone["antiguedad_http_segundos"] = int(age) if age is not None else None
            if age is not None and age > 86400:
                clone["error_detalle"]="RESPUESTA_HTTP_ANTIGUA"
                clone["precio_eur"]=None
                clone["stock"]=None
            name=clone.get("nombre_ficha","")
            if name and ((args.perfil=="portatil-gaming" and not GPU_RE.search(name)) or
                         (clone.get("id_producto") and clone["id_producto"] not in response.url)):
                clone["error_detalle"]="IDENTIDAD_DUDOSA"
                clone["stock"]=None
        return assess(clone,args.presupuesto,min_hz=args.min_hz,require_keyboard=args.teclado_es,
                      profile=args.perfil,product_query=args.producto,must=args.debe_contener)
    checked=list(pc_verified)
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending=[pool.submit(detail, x) for x in selected]
        for future in as_completed(pending):
            checked.append(future.result())
    checked.sort(key=lambda x:(x["estado"]=="DESCARTADO",len(x["pendientes"]),x.get("precio_eur") if x.get("precio_eur") is not None else 100000.0))
    from historial_web import incorporar
    historial=incorporar(checked,verificar=getattr(args,"consultar_historico_web",False),max_comprobaciones=2)
    summary={
        "fecha_utc":now,"entorno":"Debian labgestor", "presupuesto_total_eur":args.presupuesto,
        "destino":args.destino,"perfil":args.perfil,"producto":args.producto,"consultas":queries,
        "candidatos_en_listados":len(found),"fichas_directas_comprobadas":len(checked),
        "comprables_verificados":sum(x["estado"]=="COMPRABLE_VERIFICADO" for x in checked),
        "candidatos_pendientes":sum(x["estado"]=="CANDIDATO_PENDIENTE" for x in checked),
        "descartados":sum(x["estado"]=="DESCARTADO" for x in checked),
        "limitaciones":"No se simula carrito/checkout ni se deduce envío al destino; disponibilidad y precios sujetos a cambios.",
        "cobertura_tiendas":searches,"ofertas":checked,"historico":historial,
    }
    return summary

def md(report):
    def cell(value):
        return normalize(str(value)).replace("|", r"\|").replace("[", r"\[").replace("]", r"\]")
    out=["# Búsqueda automática desde Debian",
         "",f"Consulta UTC: {report['fecha_utc']} · Presupuesto total: {report['presupuesto_total_eur']:.2f} € · Destino: {report['destino']}",
         "",f"Listados: {report['candidatos_en_listados']} · Fichas leídas: {report['fichas_directas_comprobadas']} · Comprables íntegramente verificados: {report['comprables_verificados']}",
         "","## Cobertura real",
         "| Tienda | Consulta | Resultado | Productos |","|---|---|---|---:|"]
    for x in report["cobertura_tiendas"]:
        out.append(f"| {x['tienda']} | {x['consulta']} | {x['resultado']} | {x.get('encontrados','—')} |")
    out+=["","## Comparación de fichas"]
    if report.get("perfil","portatil-gaming")=="general":
        out+=["| Artículo | Tienda | Precio observado | Stock | Estado |","|---|---|---:|---|---|"]
        for x in report["ofertas"]:
            out.append(f"| [{cell(x['nombre_ficha'] or x['nombre'])}]({x['url']}) | {x['tienda']} | {str(x.get('precio_eur'))+' €' if x.get('precio_eur') is not None else 'Sin verificar'} | {x.get('stock')} | {x['estado']} |")
    else:
        out+=["| Artículo | Tienda | Precio | GPU | RAM | SSD | Hz | Estado |","|---|---:|---|---:|---:|---:|---|"]
        for x in report["ofertas"]:
            out.append(f"| [{cell(x['nombre_ficha'] or x['nombre'])}]({x['url']}) | {x['tienda']} | {str(x.get('precio_eur'))+' €' if x.get('precio_eur') is not None else 'Sin verificar'} | {x.get('gpu') or '?'} | {x.get('ram_gb') or '?'} | {x.get('ssd_gb') or '?'} | {x.get('hz') or '?'} | {x['estado']} |")
    out+=["","## Histórico de precios"]
    for x in report["ofertas"]:
        h=x.get("historico_web",{})
        fuentes=" | ".join("[%s](%s)"%(f["fuente"],f["url"]) for f in h.get("enlaces",[]))
        out.append("- %s: %s; minimo_anual_externo=%s; fuente=%s; alertas=%s"%(x["nombre"][:45],h.get("estado"),h.get("minimo_anual_eur"),h.get("fuente_url"),h.get("aviso")))
        if fuentes:out.append("  Fuentes: "+fuentes)
    out+=["","## Incidencias por oferta"]
    for x in report["ofertas"]:
        out.append(f"- **{x['tienda']}: {x.get('id_producto') or x['url'].split('/')[-2][:28]}**: incumple {', '.join(x['incumplimientos']) or 'ningún criterio acreditado'}; pendiente {', '.join(x['pendientes']) or 'nada'}; error {x.get('error_detalle','ninguno')}")
    out+=["","> No hay precio final verificable para Toledo sin costes de envío confirmados. Una ficha accesible no implica autorización de compra.",""]
    return "\n".join(out)

def main(argv=None):
    p=argparse.ArgumentParser(description="Búsqueda autónoma de productos con comparación verificable, sin compra")
    p.add_argument("--perfil",choices=["portatil-gaming","general"],default="portatil-gaming")
    p.add_argument("--producto",default="portatil gaming",help="Necesario para perfil general")
    p.add_argument("--visual-fallback",action=argparse.BooleanOptionalAction,default=True,
                   help="Al recibir 403 en PcComponentes, usar acceso_webs/Firefox ESR gráfico")
    p.add_argument("--debe-contener",default="",help="Atributos separados por coma que deben comprobarse en la ficha")
    p.add_argument("--consultar-historico-web","--verificar-descuento",action="store_true",help="Solo finalistas; máximo 2 consultas HTTP a un histórico externo")
    p.add_argument("--presupuesto",type=float,default=900)
    p.add_argument("--destino",default="Toledo, España")
    p.add_argument("--gpus",default="5060,5050,4060",help="GPU separadas por coma")
    p.add_argument("--min-hz",type=int,default=144)
    p.add_argument("--max-fichas-por-tienda",type=int,default=3)
    p.add_argument("--teclado-es",action=argparse.BooleanOptionalAction,default=True)
    p.add_argument("--salida",default=None)
    a=p.parse_args(argv)
    a.gpus=[x.strip() for x in a.gpus.split(",") if x.strip() in {"4060","5050","5060"}]
    a.debe_contener=[x.strip() for x in a.debe_contener.split(",") if x.strip()]
    if (a.perfil=="portatil-gaming" and not a.gpus) or (a.perfil=="general" and not a.producto.strip()) or not (0<a.presupuesto<100000) or not(1<=a.max_fichas_por_tienda<=15):
        p.error("Consulta, GPU, presupuesto o máximo de fichas inválidos")
    report=run(a)
    dest=Path(a.salida or Path(__file__).resolve().parent.parent/"reports"/datetime.now(timezone.utc).strftime("busqueda-%Y%m%d-%H%M%S"))
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.with_suffix(".json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dest.with_suffix(".md").write_text(md(report),encoding="utf-8")
    print(json.dumps({"resumen":{k:v for k,v in report.items() if k not in ("ofertas","cobertura_tiendas")},
                      "resultado_json":str(dest.with_suffix(".json")),
                      "resultado_md":str(dest.with_suffix(".md")),
                      "ofertas_relevantes":[{"nombre":x["nombre"][:95],"tienda":x["tienda"],"precio_eur":x.get("precio_eur"),"estado":x["estado"],"pendientes":x["pendientes"],"url":x["url"]} for x in report["ofertas"][:7]]},
                     ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
