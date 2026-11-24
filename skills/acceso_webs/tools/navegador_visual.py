#!/usr/bin/env python3
"""Acceso visual X11 autorizado: Firefox convencional y HTML visible copiado.
No modifica cookies, perfiles, permisos ni protecciones del sitio.
Uso interno: únicamente URLs públicas autorizadas, no cuenta, carrito ni pagos.
"""
from __future__ import annotations
import ctypes
import fcntl
import os
import re
import shutil
import subprocess
import time
from urllib.parse import urlsplit

class AccesoVisualError(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def _command(argv, timeout=5):
    return subprocess.run(argv, capture_output=True, timeout=timeout, check=False)

def _text(argv, timeout=5):
    p=_command(argv,timeout)
    if p.returncode: raise AccesoVisualError("COMANDO_X11_FALLIDO")
    return p.stdout.decode("utf-8","replace")

def _host(url, allowed):
    u=urlsplit(url)
    if u.scheme!="https" or u.username or u.password or u.fragment or u.hostname not in allowed or u.port not in (None,443):
        raise AccesoVisualError("URL_NO_PERMITIDA")
    return u.hostname

class XKeys:
    def __init__(self):
        self.x=ctypes.CDLL("libX11.so.6")
        self.t=ctypes.CDLL("libXtst.so.6")
        self.x.XOpenDisplay.restype=ctypes.c_void_p
        self.d=self.x.XOpenDisplay(None)
        if not self.d:raise AccesoVisualError("DISPLAY_X11_NO_DISPONIBLE")
        self.x.XStringToKeysym.argtypes=[ctypes.c_char_p]
        self.x.XStringToKeysym.restype=ctypes.c_ulong
        self.x.XKeysymToKeycode.argtypes=[ctypes.c_void_p,ctypes.c_ulong]
        self.x.XKeysymToKeycode.restype=ctypes.c_uint
        self.t.XTestFakeKeyEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong]
        self.t.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong]
        self.t.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong]
        self.x.XFlush.argtypes=[ctypes.c_void_p]
        self.x.XCloseDisplay.argtypes=[ctypes.c_void_p]
    def close(self):self.x.XCloseDisplay(self.d)
    def key(self,s,down):
        code=self.x.XKeysymToKeycode(self.d,self.x.XStringToKeysym(s.encode()))
        if not code:raise AccesoVisualError("TECLA_NO_DISPONIBLE")
        self.t.XTestFakeKeyEvent(self.d,code,int(down),0);self.x.XFlush(self.d)
        time.sleep(.035)
    def hot(self,s):
        self.key("Control_L",True)
        try:self.key(s,True);self.key(s,False)
        finally:self.key("Control_L",False)
    def click(self,x,y):
        self.t.XTestFakeMotionEvent(self.d,-1,x,y,0);self.x.XFlush(self.d);time.sleep(.06)
        self.t.XTestFakeButtonEvent(self.d,1,1,0)
        self.t.XTestFakeButtonEvent(self.d,1,0,0)
        self.x.XFlush(self.d);time.sleep(.09)

def _destino_confirmado(actual, solicitado, permitidos):
    """Coincidencia genérica de HTTPS + origen + ruta + consulta, no por marca."""
    from urllib.parse import parse_qsl
    a=urlsplit(actual);b=urlsplit(solicitado)
    return (a.scheme=="https" and b.scheme=="https" and
            a.hostname in permitidos and a.hostname==b.hostname and
            a.path.rstrip("/")==b.path.rstrip("/") and
            sorted(parse_qsl(a.query,keep_blank_values=True)) ==
            sorted(parse_qsl(b.query,keep_blank_values=True)))

class FirefoxVisual:
    """Una sola pestaña de Firefox ESR de la sesión gráfica del usuario."""
    def __init__(self, allowed_hosts, max_html=3000000):
        # Cada consumidor especifica sus dominios; el motor no tiene un sitio preferido.
        if not allowed_hosts or not all(isinstance(h,str) and h and "/" not in h for h in allowed_hosts):
            raise AccesoVisualError("DOMINIOS_PERMITIDOS_REQUERIDOS")
        self.allowed=set(allowed_hosts)
        self.max_html=max_html
        self.window=None
        self.pid=None
        self.started=False
        self.recuperacion_navegacion=None
        if not os.getenv("DISPLAY"):
            # Cuando el MCP remoto abre una shell sin entorno gráfico heredado,
            # recuperar únicamente la sesión X11 *ya existente* del mismo usuario.
            # Exigir prueba real de conexión; jamás iniciar un X-server ni leer secretos.
            auth=os.path.join(os.path.expanduser("~"),".Xauthority")
            try:
                owner_ok=os.stat(auth).st_uid==os.getuid()
            except OSError:
                owner_ok=False
            if owner_ok and os.path.exists("/tmp/.X11-unix/X0"):
                env=dict(os.environ,DISPLAY=":0",XAUTHORITY=auth)
                try:
                    probe=subprocess.run(["xprop","-root","_NET_ACTIVE_WINDOW"],env=env,
                                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=3)
                    if probe.returncode==0:
                        os.environ.update(DISPLAY=":0",XAUTHORITY=auth)
                        runtime=os.getenv("XDG_RUNTIME_DIR",f"/run/user/{os.getuid()}")
                        bus=os.path.join(runtime,"bus")
                        if os.path.exists(bus):
                            os.environ.setdefault("DBUS_SESSION_BUS_ADDRESS","unix:path="+bus)
                except (OSError,subprocess.TimeoutExpired):
                    pass
        if not os.getenv("DISPLAY"):raise AccesoVisualError("DISPLAY_NO_DISPONIBLE")
        for tool in ("firefox-esr","xprop","xclip","xwininfo"):
            if not shutil.which(tool):raise AccesoVisualError("FALTA_HERRAMIENTA_"+tool)
        self.keys=XKeys()
        self.lock=None
    def __enter__(self):
        loc=os.getenv("XDG_RUNTIME_DIR",f"/tmp/acceso-webs-{os.getuid()}")
        if not os.path.isdir(loc):raise AccesoVisualError("LOCK_RUNTIME_NO_DISPONIBLE")
        path=os.path.join(loc,"acceso_webs_visual.lock")
        self.lock=open(path,"a+",encoding="utf-8")
        try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise AccesoVisualError("OTRA_SESION_VISUAL_ACTIVA")
        return self
    def __exit__(self,*exc):
        if self.lock:self.lock.close()
        self.keys.close()
    def _active(self):
        s=_text(["xprop","-root","_NET_ACTIVE_WINDOW"])
        m=re.search(r"0x[0-9a-f]+",s)
        if not m or m.group(0)=="0x0":raise AccesoVisualError("VENTANA_NO_ACTIVA")
        wid=m.group(0)
        data=_text(["xprop","-id",wid,"WM_CLASS","_NET_WM_PID"])
        if '"firefox-esr"' not in data and '"Firefox"' not in data:
            raise AccesoVisualError("VENTANA_NO_ES_FIREFOX")
        m=re.search(r"_NET_WM_PID\(CARDINAL\) = (\d+)",data)
        if not m:raise AccesoVisualError("PID_FIREFOX_INEXISTENTE")
        pid=int(m.group(1))
        try:owner=os.stat("/proc/"+str(pid)).st_uid
        except FileNotFoundError:raise AccesoVisualError("FIREFOX_CERRADO")
        if owner!=os.getuid():raise AccesoVisualError("FIREFOX_NO_ES_DEL_USUARIO")
        return wid,pid
    def _verify_focus(self):
        wid,pid=self._active()
        if self.window is None:self.window,self.pid=wid,pid
        elif (wid,pid)!=(self.window,self.pid):raise AccesoVisualError("FOCO_CAMBIADO")
    def _clipboard(self,mime=None):
        cmd=["xclip","-o","-selection","clipboard"]
        if mime:cmd+=["-t",mime]
        p=_command(cmd,timeout=7)
        if p.returncode:raise AccesoVisualError("CLIPBOARD_SIN_"+(mime or "TEXTO"))
        if len(p.stdout)>self.max_html:raise AccesoVisualError("DOCUMENTO_DEMASIADO_GRANDE")
        return p.stdout.decode("utf-8","replace")
    def _set_clipboard(self,txt):
        # xclip queda como propietario de la selección X11; no esperar el cierre del
        # proceso servidor (subprocess.run puede colgar por los descriptores heredados).
        p=subprocess.Popen(["xclip","-selection","clipboard","-i"],
                          stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,start_new_session=True)
        try:
            p.stdin.write(txt.encode("utf8"))
            p.stdin.close()
        except BrokenPipeError:
            raise AccesoVisualError("CLIPBOARD_SIN_ESCRITURA")
        try:
            rc=p.wait(timeout=0.4)
            if rc:raise AccesoVisualError("CLIPBOARD_SIN_ESCRITURA")
        except subprocess.TimeoutExpired:
            pass
    def introducir_texto_publico(self, texto, comprobar_documento, enfocar_campo, leer_campo):
        """Pegar una consulta pública y acreditar su valor; nunca enviar el formulario.
        Los callbacks verifican URL/DOM sin alterar el foco ni el portapapeles.
        No usar para credenciales, datos sensibles ni campos de cuenta o pago.
        """
        if not isinstance(texto,str) or not texto.strip() or len(texto)>256 or any(ord(c)<32 for c in texto):
            raise AccesoVisualError("TEXTO_PUBLICO_INVALIDO")
        self._verify_focus()
        comprobar_documento()
        if not enfocar_campo():
            raise AccesoVisualError("FOCO_CAMPO_NO_CONFIRMADO")
        time.sleep(1)
        self._verify_focus()
        comprobar_documento()
        self._set_clipboard(texto)
        if self._clipboard()!=texto:
            raise AccesoVisualError("PORTAPAPELES_NO_CONFIRMADO")
        self.keys.hot("a")
        time.sleep(.25)
        self.keys.hot("v")
        for _ in range(8):
            time.sleep(.25)
            self._verify_focus()
            comprobar_documento()
            if leer_campo()==texto:
                return True
        raise AccesoVisualError("VALOR_CAMPO_NO_CONFIRMADO")

    def _url_actual(self):
        self._verify_focus()
        self.keys.hot("l");self.keys.hot("c");time.sleep(.17)
        url=self._clipboard().strip()
        self.keys.key("Escape",True);self.keys.key("Escape",False)
        _host(url,self.allowed)
        return url
    def _focus_body(self):
        self._verify_focus()
        s=_text(["xwininfo","-id",self.window])
        vals={}
        for field in ("Absolute upper-left X","Absolute upper-left Y","Width","Height"):
            m=re.search(r"^\s*"+re.escape(field)+r":\s*(-?\d+)",s,re.M)
            if not m:raise AccesoVisualError("GEOMETRIA_DESCONOCIDA")
            vals[field]=int(m.group(1))
        xx=vals["Absolute upper-left X"]+8
        yy=vals["Absolute upper-left Y"]+min(300,max(180,vals["Height"]//2))
        self.keys.click(xx,yy)
    def _navegar_por_barra_y_confirmar(self,url,esperas=16):
        """Navegación normal, sin asumir éxito por haber tecleado la URL."""
        self._verify_focus()
        self._set_clipboard(url)
        time.sleep(.08)
        if self._clipboard().strip()!=url:
            raise AccesoVisualError("URL_PORTAPAPELES_NO_CONFIRMADA")
        self.keys.hot("l")
        self.keys.hot("v")
        self.keys.key("Return",True);self.keys.key("Return",False)
        for _ in range(esperas):
            time.sleep(.4)
            try:
                current=self._url_actual()
            except AccesoVisualError as e:
                if e.code in ("FOCO_CAMBIADO","URL_NO_PERMITIDA"):
                    raise
                continue
            if _destino_confirmado(current,url,self.allowed):
                return True
        return False

    def open(self,url):
        _host(url,self.allowed)
        self.recuperacion_navegacion=None
        if not self.started:
            subprocess.Popen(["firefox-esr","--new-tab",url],stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,start_new_session=True)
            self.started=True
            for _ in range(18):
                time.sleep(.6)
                try:
                    self._verify_focus()
                    current=self._url_actual()
                    if _destino_confirmado(current,url,self.allowed):
                        break
                except AccesoVisualError:pass
            else:raise AccesoVisualError("FIREFOX_NO_NAVEGO_A_URL")
        else:
            self._verify_focus()
            # M56: se recupera una única pérdida transitoria de navegación.
            # El segundo intento se mantiene en la misma ventana y con origen permitido.
            if not self._navegar_por_barra_y_confirmar(url,esperas=16):
                if not self._navegar_por_barra_y_confirmar(url,esperas=16):
                    raise AccesoVisualError("NAVEGACION_NO_CONFIRMADA_TRAS_REINTENTO")
                self.recuperacion_navegacion="M56_RECUPERAR_NAVEGACION_TRANSITORIA"
        self._verify_focus()
        # La URL puede estar ya en la barra mientras la página todavía carga.
        time.sleep(1.0)
    def _leer_html_visible(self, expected=None):
        """Leer un documento visible, con espera limitada; URL sola nunca acredita carga."""
        last="CONTENIDO_NO_VERIFICADO"
        for attempt in range(3):
            self._verify_focus()
            current=self._url_actual()
            if urlsplit(current).hostname not in self.allowed:
                raise AccesoVisualError("DOMINIO_FINAL_NO_PERMITIDO")
            self._focus_body()
            self.keys.hot("a");self.keys.hot("c");time.sleep(.35)
            try:
                markup=self._clipboard("text/html")
            except AccesoVisualError as e:
                if e.code!="CLIPBOARD_SIN_text/html":
                    raise
                last="PAGINA_SIN_HTML_RENDERIZADO"
                if attempt<2:
                    time.sleep(0.7+attempt)
                continue
            # En caso de desafío interactivo o error de certificado, detenerse.
            if re.search(r"Just a moment|verifica que eres humano|captcha",markup,re.I):
                raise AccesoVisualError("DESAFIO_INTERACTIVO")
            if re.search(r"SEC_ERROR_UNKNOWN_ISSUER|MOZILLA_PKIX_ERROR|SSL_ERROR_BAD_CERT_DOMAIN",markup,re.I):
                raise AccesoVisualError("ERROR_CERTIFICADO_TITULAR")
            if expected is None or expected(markup):
                return {"url":current,"html":markup,"metodo":"firefox_esr_x11_clipboard_html"}
            last="CONTENIDO_NO_VERIFICADO"
            if attempt<2:
                time.sleep(0.7+attempt)
        raise AccesoVisualError(last)

    def read(self,url,expected=None):
        self.open(url)
        try:
            page=self._leer_html_visible(expected)
            if getattr(self, "recuperacion_navegacion", None):
                page["recuperacion_navegacion"]=self.recuperacion_navegacion
            return page
        except AccesoVisualError as e:
            # M55: recuperar UNA carga transitoriamente vacía en el navegador
            # convencional del titular; sin cambiar identidad, IP ni seguridad.
            if e.code not in ("PAGINA_SIN_HTML_RENDERIZADO","CONTENIDO_NO_VERIFICADO"):
                raise
            self._verify_focus()
            current=self._url_actual()
            if urlsplit(current).hostname!=urlsplit(url).hostname:
                raise AccesoVisualError("DESTINO_CAMBIO_ANTES_DE_RECARGA")
            # El foco debe dejar la barra de direcciones antes de recargar.
            self._focus_body()
            self.keys.hot("r")
            time.sleep(1.5)
            try:
                page=self._leer_html_visible(expected)
                page["recuperacion"]="M55_RECUPERAR_CARGA_TRANSITORIA"
                return page
            except AccesoVisualError as e2:
                if e2.code in ("PAGINA_SIN_HTML_RENDERIZADO","CONTENIDO_NO_VERIFICADO"):
                    raise AccesoVisualError("RECARGA_ACOTADA_SIN_CONTENIDO")
                raise
