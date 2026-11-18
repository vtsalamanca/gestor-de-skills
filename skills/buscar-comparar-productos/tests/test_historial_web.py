import sys, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from historial_web import enlaces,incorporar,comprobar_pccom

class Fake:
    def __init__(self,html):
        self.text=html
        self.status_code=200
        self.content=html.encode()
class Session:
    def __init__(self,html):
        self.html=html
        self.calls=0
    def get(self,url,timeout):
        self.calls+=1
        return Fake(self.html)
class HistoryExternal(unittest.TestCase):
    def test_keepa_es(self):
        row={"tienda":"Amazon","url":"https://www.amazon.es/dp/B0GN5JQPVM"}
        self.assertEqual(enlaces(row)[0]["url"],"https://keepa.com/#!product/9-B0GN5JQPVM")
    def test_pc_id(self):
        row={"tienda":"PcComponentes","id_producto":"17335553"}
        self.assertTrue(enlaces(row)[0]["url"].endswith("ref-17335553"))
    def test_normal_no_hace_peticiones(self):
        row={"tienda":"PcComponentes","id_producto":"17335553","precio_eur":899}
        with patch("historial_web.comprobar_pccom",side_effect=AssertionError("No HTTP")):
            meta=incorporar([row],verificar=False)
        self.assertEqual(meta["consultas_efectuadas"],0)
    def test_limite_de_consultas(self):
        rows=[{"tienda":"PcComponentes","id_producto":str(10000+i),"precio_eur":900} for i in range(4)]
        with patch("historial_web.comprobar_pccom",return_value={"estado":"OK"}) as m:
            meta=incorporar(rows,verificar=True,max_comprobaciones=2)
        self.assertEqual(meta["consultas_efectuadas"],2)
        self.assertEqual(m.call_count,2)
    def test_extrae_minimo_tercero(self):
        row={"tienda":"PcComponentes","id_producto":"17335553","precio_eur":1029}
        html='<link rel="canonical" href="https://pccomtracker.com/producto/producto-17335553"><meta name="description" content="Hoy 899,00 € · mínimo del año 879,00 €.">'
        a=comprobar_pccom(row,Session(html))
        self.assertEqual(a["minimo_anual_eur"],879)
        self.assertEqual(a["aviso"],"YA_EXISTIO_UN_PRECIO_ANUAL_INFERIOR")
        self.assertNotIn("minimo_30_eur",a)
        self.assertEqual(a["advertencia_frescura"],"COTIZACION_EXTERNA_DIFIERE_DE_LA_TIENDA")
    def test_id_distinta_rechazada(self):
        row={"tienda":"PcComponentes","id_producto":"17335553","precio_eur":1029}
        html='<link rel="canonical" href="https://pccomtracker.com/producto/otro-99999999"><meta name="description" content="mínimo del año 879,00 €">'
        self.assertEqual(comprobar_pccom(row,Session(html))["estado"],"IDENTIDAD_NO_CONFIRMADA")
if __name__=="__main__":
    unittest.main()

class TestPublicacionesPrevias(unittest.TestCase):
    def test_enlaces_google_y_wayback(self):
        from urllib.parse import unquote
        row={"tienda":"Amazon","nombre":"Portátil Lenovo LOQ Essential 15IRX11 RTX 5050",
             "url":"https://www.amazon.es/dp/B0GN5JQPVM"}
        links=enlaces(row)
        self.assertEqual(links[0]["fuente"],"Keepa")
        self.assertIn("before:",unquote(links[1]["url"]))
        self.assertEqual(links[2]["fuente"],"Wayback Machine")
    def test_enlaces_sin_consultas(self):
        with patch("historial_web.requests.get",side_effect=AssertionError("HTTP")):
            row={"tienda":"PcComponentes","nombre":"Lenovo LOQ Essential 15IRX11",
                 "url":"https://www.pccomponentes.com/modelo"}
            self.assertGreaterEqual(len(enlaces(row)),2)
