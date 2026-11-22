"""Lectura visual acotada de Amazon por AT-SPI, sin portapapeles ni credenciales.
No incluye compras ni grabaciones BrowserLearn. Solo Firefox propio del usuario.
"""
from __future__ import annotations
from datetime import datetime, timezone
import os
import re
import subprocess
import time
from urllib.parse import urlsplit, parse_qsl

ASIN = re.compile(r"/(?:gp/product|dp)/([A-Z0-9]{10})(?:[/?]|$)", re.I)
EURO = re.compile(r"(?<!\d)(\d{1,3}(?:\.\d{3})*,\d{2})\s*€")
BLOCK = re.compile(r"captcha|just a moment|verifica que eres humano|robot check", re.I)

def _euro(value):
    m = EURO.search(value or "")
    return float(m.group(1).replace(".", "").replace(",", ".")) if m else None

def match_product(requested, observed):
    """No confundir productos de otras diagonales o referencias."""
    a = re.findall(r"[a-z0-9]+", requested.lower())
    b = (observed or "").lower()
    size=re.search(r"(?<![a-z0-9])(?:43|50|55|65|75|85|98)(?![a-z0-9])",requested.lower())
    if size and not re.search(r"(?<![a-z0-9])"+size.group(0)+r"(?![a-z0-9])",b):
        return False
    codes = [x for x in a if re.search(r"\d", x) and len(x) >= 4]
    if codes:
        return all(x in re.findall(r"[a-z0-9]+", b) for x in codes)
    terms = [x for x in a if len(x) > 2 and x not in {"para","con","televisor","smart","pulgadas","mini","led"}]
    return bool(terms) and sum(x in b for x in terms) >= max(1, len(terms) - 1)

def search_candidate(text, title, url):
    """Un precio de listado nunca equivale a precio verificado de ficha."""
    if not match_product(title, text) or not ASIN.search(url or "") or urlsplit(url).hostname not in ("www.amazon.es","amazon.es"):
        return None
    m = re.search(r"(?:precio, p[aá]gina del producto|producto)\s+([\d.,]+\s*€)", text, re.I)
    price = _euro(m.group(1)) if m else None
    return {"url":"https://www.amazon.es/dp/"+ASIN.search(url).group(1).upper(), "nombre":title, "precio_indice_eur":price,
            "fuente_descubrimiento":"amazon_firefox_atspi",
            "id_producto":ASIN.search(url).group(1).upper()}

def offer_from_text(text, seller=None):
    """Solo un bloque de oferta del artículo exacto; no recomendaciones."""
    t = re.sub(r"\s+", " ", text or "")
    p = _euro(t)
    if p is None:
        return None
    return {"precio_eur":p, "vendedor":seller,
            "stock":None, "envio_a_destino_verificado":False,
            "garantia_verificada":False, "origen_precio":"opcion_compra_amazon_atspi"}

class VisualError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def _walk(root, limit=8500):
    stack=[root]
    count=0
    while stack and count<limit:
        node=stack.pop()
        count+=1
        yield node
        try:
            children=min(node.get_child_count(),180)
            stack.extend(node.get_child_at_index(i) for i in range(children-1,-1,-1))
        except Exception:
            continue

class AmazonVisual:
    """Abre una pestaña temporal; valida URL y PID antes de leer AT-SPI."""
    def __init__(self, timeout=35):
        import gi
        gi.require_version("Atspi","2.0")
        from gi.repository import Atspi
        self.atspi=Atspi
        self.timeout=timeout
        self.initial_tabs=None
        self.requested=None

    def _current(self):
        env=dict(os.environ)
        env.setdefault("DISPLAY",":0")
        env.setdefault("XAUTHORITY",os.path.expanduser("~/.Xauthority"))
        try:
            active=subprocess.check_output(["xprop","-root","_NET_ACTIVE_WINDOW"],env=env,timeout=3,text=True)
            wid=re.search(r"0x[0-9a-f]+",active)
            if not wid or wid.group(0)=="0x0":
                raise VisualError("SIN_VENTANA_ACTIVA")
            props=subprocess.check_output(["xprop","-id",wid.group(0),"WM_CLASS","_NET_WM_PID"],env=env,timeout=3,text=True)
            pid=re.search(r"_NET_WM_PID.*?=\s*(\d+)",props)
            if not pid or "firefox" not in props.lower():
                raise VisualError("VENTANA_NO_ES_FIREFOX")
            num=int(pid.group(1))
            if os.stat("/proc/"+str(num)).st_uid!=os.getuid():
                raise VisualError("FIREFOX_NO_AUTORIZADO")
            d=self.atspi.get_desktop(0)
            for i in range(d.get_child_count()):
                app=d.get_child_at_index(i)
                if app.get_name()=="Firefox" and app.get_process_id()==num:
                    return app.get_child_at_index(0)
        except VisualError:
            raise
        except Exception as e:
            raise VisualError("VENTANA_NO_VERIFICABLE") from e
        raise VisualError("FIREFOX_ATSPI_NO_DISPONIBLE")

    def _url(self, frame):
        for node in _walk(frame,1000):
            try:
                if node.get_role_name()=="combo box":
                    label=(node.get_name() or "").lower()
                    if "address" in label or "direcci" in label:
                        s=self.atspi.Text.get_text(node,0,-1).strip()
                        if not s.startswith("http"):
                            s="https://"+s
                        return s
            except Exception:
                pass
        raise VisualError("URL_ATSPI_NO_DISPONIBLE")

    def _document(self, frame):
        for node in _walk_frame(frame):
            try:
                if node.get_role_name()=="document web" and node.get_state_set().contains(self.atspi.StateType.SHOWING):
                    if BLOCK.search(node.get_name() or ""):
                        raise VisualError("DESAFIO_INTERACTIVO")
                    return node
            except VisualError:
                raise
            except Exception:
                pass
        raise VisualError("DOCUMENTO_NO_VISIBLE")

    def _checked_document(self):
        frame=self._current()
        if not self.requested or not self._same_url(self._url(frame),self.requested):
            raise VisualError("URL_CAMBIO_DURANTE_LECTURA")
        return self._document(frame)

    def _tabs(self, frame):
        for node in _walk(frame,300):
            try:
                if node.get_role_name()=="page tab list":
                    return node
            except Exception:
                pass
        return None

    def open(self, url):
        domain=urlsplit(url).hostname
        if domain not in ("www.amazon.es","amazon.es") or urlsplit(url).scheme!="https":
            raise VisualError("DOMINIO_NO_AUTORIZADO")
        self.requested=url
        try:
            frame=self._current()
            tabs=self._tabs(frame)
            self.initial_tabs=tabs.get_child_count() if tabs else None
        except VisualError:
            self.initial_tabs=None
        subprocess.Popen(["firefox-esr","--new-tab",url],stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True,
                         env={**os.environ,"DISPLAY":os.getenv("DISPLAY") or ":0",
                              "XAUTHORITY":os.getenv("XAUTHORITY") or os.path.expanduser("~/.Xauthority")})
        until=time.monotonic()+self.timeout
        last="NAVEGACION_NO_CONFIRMADA"
        while time.monotonic()<until:
            time.sleep(.7)
            try:
                frame=self._current()
                target=self._url(frame)
                if not self._same_url(target,url):
                    last="URL_DISTINTA"
                    continue
                doc=self._document(frame)
                if doc.get_child_count() > 0:
                    return frame,doc
            except VisualError as e:
                if e.code in ("DESAFIO_INTERACTIVO","DOMINIO_NO_AUTORIZADO"):
                    raise
                last=e.code
        raise VisualError(last)

    @staticmethod
    def _same_url(actual,requested):
        a,b=urlsplit(actual),urlsplit(requested)
        if a.hostname!=b.hostname or a.scheme!="https":
            return False
        x,y=ASIN.search(a.path),ASIN.search(b.path)
        if x or y:
            return bool(x and y and x.group(1).upper()==y.group(1).upper())
        return (a.path.rstrip("/")==b.path.rstrip("/") and
                sorted(parse_qsl(a.query))==sorted(parse_qsl(b.query)))

    def close_own_tab(self):
        try:
            frame=self._current()
            if not self._same_url(self._url(frame),self.requested):
                return False
            tabs=self._tabs(frame)
            if not tabs or self.initial_tabs is None or tabs.get_child_count()<=self.initial_tabs:
                return False
            for i in range(tabs.get_child_count()):
                tab=tabs.get_child_at_index(i)
                if tab.get_role_name()=="page tab" and tab.get_state_set().contains(self.atspi.StateType.SELECTED):
                    for j in range(tab.get_child_count()):
                        button=tab.get_child_at_index(j)
                        if button.get_name()=="Close tab":
                            return bool(button.do_action(0))
        except Exception:
            pass
        return False

    def search(self, query):
        from urllib.parse import urlencode
        _,doc=self.open("https://www.amazon.es/s?"+urlencode({"k":query}))
        # Esperar tarjetas reales: el documento puede existir antes del listado.
        for _ in range(12):
            if any(n.get_role_name()=="list item" and match_product(query,n.get_name() or "") for n in _walk(doc)):
                break
            time.sleep(.8)
            doc=self._checked_document()
        results=[]
        seen=set()
        for item in _walk(doc):
            try:
                if item.get_role_name()!="list item":
                    continue
                name=(item.get_name() or "")[:1250]
                if not match_product(query,name):
                    continue
                title=None
                url=None
                for ch in _walk(item,95):
                    if ch.get_role_name()=="heading":
                        title=ch.get_name() or ""
                    if ch.get_role_name()=="link":
                        h=ch.get_hyperlink()
                        if h:
                            candidate=h.get_uri(0)
                            if candidate and ASIN.search(urlsplit(candidate).path) and urlsplit(candidate).hostname in ("www.amazon.es","amazon.es"):
                                url=candidate
                    if title and url:
                        break
                c=search_candidate(name,title or name,url)
                if c and c["id_producto"] not in seen:
                    seen.add(c["id_producto"])
                    results.append(c)
            except Exception:
                continue
        return results

    def detail(self, url, title):
        _,doc=self.open(url)
        for _ in range(12):
            observed=doc.get_name() or ""
            if match_product(title,observed):break
            time.sleep(.8)
            doc=self._checked_document()
        else:raise VisualError("MODELO_NO_COINCIDE")
        result={"nombre_ficha":observed,"precio_eur":None,"stock":None,
                "envio_a_destino_verificado":False,"garantia_verificada":False,
                "metodo_detalle":"amazon_firefox_atspi","error_detalle":"SIN_OFERTA_PRINCIPAL"}
        for _ in range(12):
            buybox=_buybox_from_doc(doc,self.atspi,observed)
            if buybox:
                result.update(buybox)
                result["error_detalle"]=None
                return result
            time.sleep(.6)
            doc=self._checked_document()
        # Solo botón 'Ver todas las opciones de compra': no se añade a la cesta.
        for node in _walk(doc):
            try:
                if node.get_role_name()=="link" and (node.get_name() or "")=="Ver todas las opciones de compra":
                    if node.get_n_actions():
                        node.do_action(0)
                        time.sleep(.8)
                    break
            except Exception:
                pass
        # El cuadro lateral de opciones prevalece sobre precios de recomendaciones.
        doc=self._checked_document()
        for node in _walk(doc):
            try:
                if node.get_role_name()=="dialog":
                    lines=[(n.get_role_name(),(n.get_name() or "")[:300]) for n in _walk(node,400)]
                    joined=" ".join(v for _,v in lines)
                    if "opciones" not in joined.lower():
                        continue
                    price=None
                    seller=None
                    for i,(role,label) in enumerate(lines):
                        if price is None and role in ("static","text","link") and _euro(label) is not None:
                            price=_euro(label)
                        if label.strip().lower()=="vendedor" and i+1<len(lines):
                            seller=lines[i+1][1].strip()
                    if price is not None:
                        result.update(offer_from_text(f"{price:.2f}".replace(".",",")+" €",seller))
                        result["error_detalle"]=None
                        return result
            except Exception:
                pass
        buybox=_buybox_from_doc(doc,self.atspi,observed)
        if buybox:
            result.update(buybox)
            result["error_detalle"]=None
        return result


def _walk_frame(root):
    queue=[(root,0)]
    n=0
    while queue and n<500:
        node,depth=queue.pop(0)
        n+=1
        yield node
        if depth>=6 or node.get_role_name()=="document web":
            continue
        try:
            for i in range(min(node.get_child_count(),60)):
                queue.append((node.get_child_at_index(i),depth+1))
        except Exception:
            continue

def _buybox_from_doc(doc, atspi, title):
    """Precio de variante marcada y bloque vendedor en la ficha verificada."""
    size=re.search(r'(?<![a-z0-9])(43|50|55|65|75|85|98)\s*(?:pulgadas|["″])',
                   title.lower())
    if not size:
        return None
    price=None
    stock=None
    seller=None
    for node in _walk(doc,11000):
        try:
            role=node.get_role_name()
            name=(node.get_name() or "").strip()
            if role=="radio button" and node.get_state_set().contains(atspi.StateType.CHECKED):
                match=re.match(r'^\s*'+size.group(1)+r'["″]?\s+(.+)',name)
                if match:
                    price=_euro(match.group(1))
                    stock=True if "en stock" in name.lower() else None
            if role=="heading" and name=="Remitente / Vendedor":
                parent=node.get_parent()
                for i in range(parent.get_child_count()):
                    child=parent.get_child_at_index(i)
                    if child.get_role_name()=="section" and child.get_character_count():
                        value=atspi.Text.get_text(child,0,-1).strip()
                        if 1<=len(value)<=80 and "\n" not in value:
                            seller=value
        except Exception:
            continue
    if price is None:
        return None
    return {"precio_eur":price,"vendedor":seller,"stock":stock,
            "envio_a_destino_verificado":False,"garantia_verificada":False,
            "origen_precio":"amazon_variante_marcada_atspi"}
