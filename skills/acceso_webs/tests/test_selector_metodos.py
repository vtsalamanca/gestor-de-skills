import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from selector_metodos import catalogo,recomendar

class TestModalidades(unittest.TestCase):
    def test_catalogo_ordenado(self):
        rows=catalogo()["modalidades"]
        self.assertEqual(len(rows),9)
        self.assertEqual([r["orden"] for r in rows],sorted(r["orden"] for r in rows))
    def test_catalogo_sin_sitios(self):
        data=(ROOT/"references"/"modalidades.json").read_text().lower()
        for site in ("pccomponentes","amazon","fnac","educamos","infojobs","mediamarkt"):
            self.assertNotIn(site,data)
    def test_primero_reutilizacion(self):
        self.assertEqual(recomendar("SIN_PROBAR",{"cache_vigente":True})["metodo"],"M00_REUSO_VALIDADO")
    def test_fuente_oficial(self):
        self.assertEqual(recomendar("SIN_PROBAR",{"fuente_oficial":True})["metodo"],"M10_FUENTE_ESTRUCTURADA")
    def test_http_datos(self):
        self.assertEqual(recomendar("HTTP_200_CON_DATOS")["metodo"],"M20_HTTP_PUBLICO")
    def test_dinamico(self):
        self.assertEqual(recomendar("HTTP_200_SIN_DATOS",{"navegador_dom":True})["metodo"],"M40_NAVEGADOR_DOM")
    def test_403_visual(self):
        r=recomendar("HTTP_403_DESAFIO",{"navegador_visual":True})
        self.assertEqual(r["metodo"],"M50_NAVEGADOR_VISUAL")
        self.assertEqual(r["estado"],"PROPUESTA_SIN_VERIFICAR")
    def test_403_sin_visual(self):
        self.assertEqual(recomendar("HTTP_403_DESAFIO")["metodo"],"M90_ALTERNATIVA_OFICIAL")
    def test_auth_es_transversal(self):
        self.assertEqual(recomendar("HTTP_401")["capa"],"A10_AUTENTICACION")
    def test_stop_429(self):
        self.assertEqual(recomendar("HTTP_429")["estado"],"DETENER")
    def test_stop_mfa_captcha(self):
        for signal in ("MFA_PENDIENTE","CAPTCHA_PENDIENTE"):
            self.assertEqual(recomendar(signal)["estado"],"DETENER")
    def test_no_costes(self):
        self.assertEqual(recomendar("SIN_PROBAR",{"coste_no_autorizado":True})["estado"],"DETENER")
    def test_desconocido_seguro(self):
        self.assertEqual(recomendar("FALLO_DESCONOCIDO")["metodo"],"M90_ALTERNATIVA_OFICIAL")


class TestAprendizajeDeclarativo(unittest.TestCase):
    def test_nuevo_metodo_se_detecta_sin_cambiar_selector(self):
        # Un método añadido al JSON funciona por señales/capacidades, sin if nuevo.
        data=catalogo()
        method={"id":"M35_PRUEBA_NEUTRA","orden":35,"nombre":"Ejemplo",
                "coste":"medio","requisitos":["prueba"],
                "confirma":"dato","siguiente":"M40_NAVEGADOR_DOM",
                "senales":["INCIDENCIA_SINTETICA"],"capacidad_requerida":"inspeccion_autorizada"}
        data["modalidades"].insert(4,method)
        self.assertEqual(recomendar("INCIDENCIA_SINTETICA",
                                     {"inspeccion_autorizada":True},data)["metodo"],
                         "M35_PRUEBA_NEUTRA")
        self.assertEqual(recomendar("INCIDENCIA_SINTETICA",{},data)["metodo"],
                         "M90_ALTERNATIVA_OFICIAL")



class TestRecuperacionNueva(unittest.TestCase):
    def test_recuperacion_blanco(self):
        self.assertEqual(recomendar("PAGINA_SIN_HTML_RENDERIZADO",
                                   {"navegador_visual":True})["metodo"],
                         "M55_RECUPERAR_CARGA_TRANSITORIA")
    def test_sin_navegador_no_reintenta(self):
        self.assertEqual(recomendar("NAVEGADOR_BLANCO",
                                   {"navegador_visual":False})["metodo"],
                         "M90_ALTERNATIVA_OFICIAL")
