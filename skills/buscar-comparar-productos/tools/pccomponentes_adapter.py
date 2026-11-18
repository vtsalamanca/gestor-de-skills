"""Adaptador de páginas de PcComponentes renderizadas en Firefox convencional.
Solo interpreta HTML que entrega acceso_webs/navegador_visual; NO consulta Cloudflare.
"""
from html.parser import HTMLParser
from html import unescape
import re
from urllib.parse import urlsplit

class CardsParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows=[]
        self.seen=set()
    def handle_starttag(self,tag,attrs):
        if tag!="a":return
        a=dict(attrs)
        u=a.get("href","")
        if urlsplit(u).hostname not in {"www.pccomponentes.com","pccomponentes.com"}:return
        if not str(a.get("data-product-list","")).startswith("Search results /"):return
        name=a.get("data-product-name") or a.get("title")
        if not name or u in self.seen:return
        self.seen.add(u)
        self.rows.append({"name":unescape(name),"url":u,
                          "price_text":a.get("data-product-price"),
                          "seller":a.get("data-product-seller"),
                          "condition":a.get("data-product-condition"),
                          "product_id":a.get("data-product-id")})
def search_cards(html):
    parser=CardsParser()
    parser.feed(html)
    return parser.rows

def detail(html):
    # Precio del PDP, nunca de recomendaciones, PVPR, packs ni enlaces relacionados.
    h=re.search(r"<h1\b[^>]*>(.*?)</h1>",html,re.I|re.S)
    title=unescape(re.sub(r"<[^>]+>"," ",h.group(1))).strip() if h else None
    title=re.sub(r"\s+"," ",title or "")
    m=re.search(r'id="pdp-price-current-integer"[^>]*>\s*([\d.]+)',html,re.I)
    if not m:
        return {"nombre_ficha":title or None,"precio_eur":None,"stock":None,
                "error_detalle":"PRECIO_FICHA_NO_DETECTADO",
                "envio_a_destino_verificado":False,"garantia_verificada":False}
    raw=m.group(1).replace(".","")
    window=html[m.end():m.end()+260]
    dec=re.search(r'id="pdp-price-current-decimals"[^>]*>(.*?)</span>\s*</span>',window,re.I|re.S)
    cents=None
    if dec:
        plain=re.sub(r"<[^>]+>","",dec.group(1))
        z=re.search(r"([0-9]{2})\s*(?:€|$)",unescape(plain))
        if z:cents=z.group(1)
    price=float(raw)+(int(cents)/100 if cents else 0)
    return {"nombre_ficha":title or None, "precio_eur":price, "stock":None,
            "error_detalle":None if title else "IDENTIDAD_SIN_H1",
            "fuente_precio":"pdp-price-current-integer",
            "envio_a_destino_verificado":False,"garantia_verificada":False}
