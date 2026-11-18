import sys
import unittest
from pathlib import Path
from unittest.mock import Mock,patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from navegador_visual import FirefoxVisual,AccesoVisualError

URL="https://ejemplo.test/productos?q=portatil"

def fake_browser():
    b=object.__new__(FirefoxVisual)
    b.allowed={"ejemplo.test"}
    b.open=Mock()
    b._verify_focus=Mock()
    b._url_actual=Mock(return_value=URL)
    b._focus_body=Mock()
    b.keys=Mock()
    b._leer_html_visible=Mock()
    return b

class TestVisualRecovery(unittest.TestCase):
    def test_blank_once_then_success(self):
        b=fake_browser()
        b._leer_html_visible.side_effect=[
            AccesoVisualError("PAGINA_SIN_HTML_RENDERIZADO"),
            {"url":URL,"html":"<h1>Productos</h1>","metodo":"firefox_esr_x11_clipboard_html"}]
        with patch("navegador_visual.time.sleep"):
            result=b.read(URL,expected=lambda x:"Productos" in x)
        self.assertEqual(result["recuperacion"],"M55_RECUPERAR_CARGA_TRANSITORIA")
        self.assertEqual(b._leer_html_visible.call_count,2)
        b.keys.hot.assert_called_once_with("r")
    def test_blank_twice_stops(self):
        b=fake_browser()
        b._leer_html_visible.side_effect=AccesoVisualError("PAGINA_SIN_HTML_RENDERIZADO")
        with patch("navegador_visual.time.sleep"):
            with self.assertRaisesRegex(AccesoVisualError,"RECARGA_ACOTADA_SIN_CONTENIDO"):
                b.read(URL)
        self.assertEqual(b._leer_html_visible.call_count,2)
        b.keys.hot.assert_called_once_with("r")
    def test_captcha_never_retry(self):
        b=fake_browser()
        b._leer_html_visible.side_effect=AccesoVisualError("DESAFIO_INTERACTIVO")
        with self.assertRaisesRegex(AccesoVisualError,"DESAFIO_INTERACTIVO"):
            b.read(URL)
        b.keys.hot.assert_not_called()
    def test_certificate_error_never_retry(self):
        b=fake_browser()
        b._leer_html_visible.side_effect=AccesoVisualError("ERROR_CERTIFICADO_TITULAR")
        with self.assertRaisesRegex(AccesoVisualError,"ERROR_CERTIFICADO_TITULAR"):
            b.read(URL)
        b.keys.hot.assert_not_called()
    def test_changed_host_never_refresh(self):
        b=fake_browser()
        b._leer_html_visible.side_effect=AccesoVisualError("PAGINA_SIN_HTML_RENDERIZADO")
        b._url_actual.return_value="https://otro.test"
        with self.assertRaisesRegex(AccesoVisualError,"DESTINO_CAMBIO_ANTES_DE_RECARGA"):
            b.read(URL)
        b.keys.hot.assert_not_called()
    def test_no_reload_when_data_available(self):
        b=fake_browser()
        b._leer_html_visible.return_value={"url":URL,"html":"ok"}
        self.assertEqual(b.read(URL)["html"],"ok")
        b.keys.hot.assert_not_called()

    def test_navigation_retry_once(self):
        b=fake_browser();b.started=True;b._navegar_por_barra_y_confirmar=Mock(side_effect=[False,True]);FirefoxVisual.open(b,URL);self.assertEqual(b.recuperacion_navegacion,"M56_RECUPERAR_NAVEGACION_TRANSITORIA");self.assertEqual(b._navegar_por_barra_y_confirmar.call_count,2)

if __name__ == "__main__":
    unittest.main()
