import sys
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"buscar-comparar-productos"/"tools"))
sys.path.insert(0,str(ROOT/"acceso_webs"/"tools"))
import buscar
import navegador_visual
from pccomponentes_adapter import search_cards, detail

TARGET="https://www.pccomponentes.com/portatil-asus-v16-ejemplo"
TITLE='Portátil ASUS V16 16GB RAM 512GB SSD RTX 5050 144Hz Teclado QWERTY español'
LIST=(
  '<div id="search-results-product-grid">'
  '<a data-product-list="Search results / portatil gaming rtx 5050" '
  'data-product-name="'+TITLE+'" data-product-id="1234" data-product-price="750" '
  'data-product-seller="PcComponentes" data-product-stock-web="undefined" '
  'href="'+TARGET+'">Artículo</a>'
  '</div>'
)
PDP=(
  '<h1>'+TITLE+'</h1><div id="pdp-price-current-container">'
  '<span id="pdp-price-current-integer">806'
  '<span id="pdp-price-current-decimals"><span>,</span>66 €</span></span></div>'
)

class FakeBrowser:
    visited=[]
    def __init__(self,**kwargs):self.kwargs=kwargs
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,url,expected=None):
        self.visited.append(url)
        markup=LIST if "/search/" in url else PDP
        assert not expected or expected(markup)
        return {"url":url,"html":markup,"metodo":"test_visual"}

def args():
    return SimpleNamespace(perfil="portatil-gaming",gpus=["5050"],max_fichas_por_tienda=3,
                           presupuesto=900,min_hz=144,teclado_es=True,
                           producto="portatil gaming",debe_contener=[])

class TestPcComponentes(unittest.TestCase):
    def test_cards(self):
        cards=search_cards(LIST)
        self.assertEqual(len(cards),1)
        self.assertEqual(cards[0]["price_text"],"750")
        self.assertEqual(cards[0]["url"],TARGET)
    def test_no_foreign_domains(self):
        html=LIST.replace('www.pccomponentes.com','otro.dominio.example')
        self.assertEqual(search_cards(html),[])
    def test_duplicated_card(self):
        self.assertEqual(len(search_cards(LIST+LIST)),1)
    def test_real_pdp_price_not_crossselling_price(self):
        self.assertEqual(detail(PDP+'<span data-product-price="1499">'),detail(PDP))
        self.assertEqual(detail(PDP)["precio_eur"],806.66)
        self.assertIsNone(detail(PDP)["stock"])
    def test_pdp_thousands(self):
        self.assertEqual(detail(PDP.replace('>806<','>1.024<').replace('>66 €','>45 €'))["precio_eur"],1024.45)
    def test_no_guess_if_price_not_found(self):
        self.assertIsNone(detail('<h1>'+TITLE+'</h1>')["precio_eur"])
    def test_full_visual_integration(self):
        FakeBrowser.visited=[]
        with patch.object(navegador_visual,'FirefoxVisual',FakeBrowser):
            rows,candidates,checked=buscar.pccomponentes_por_acceso_webs(["portatil gaming rtx 5050"],args())
        self.assertEqual(rows[0]["resultado"],"EXTRACCION_GUI_VERIFICADA")
        self.assertEqual(len(candidates),1)
        self.assertEqual(len(checked),1)
        self.assertEqual(checked[0]["precio_indice_eur"],750.0)
        self.assertEqual(checked[0]["precio_eur"],806.66)
        self.assertEqual(checked[0]["estado"],"CANDIDATO_PENDIENTE")
        self.assertEqual(len(FakeBrowser.visited),2)
    def test_visual_not_available_is_classified(self):
        class BrokenBrowser:
            def __init__(self,**kw):raise navegador_visual.AccesoVisualError("DISPLAY_NO_DISPONIBLE")
        with patch.object(navegador_visual,'FirefoxVisual',BrokenBrowser):
            rows,candidates,checked=buscar.pccomponentes_por_acceso_webs(["portatil gaming rtx 5050"],args())
        self.assertEqual(rows[0]["resultado"],"BLOQUEADO_VISUAL_DISPLAY_NO_DISPONIBLE")
        self.assertEqual(candidates,[])
        self.assertEqual(checked,[])
    def test_url_https_allowlist(self):
        for bad in ['https://pccomponentes.com.evil.example/search',
                    'http://www.pccomponentes.com/search/',
                    'https://www.pccomponentes.com@evil.example/search/']:
            with self.assertRaises(navegador_visual.AccesoVisualError):
                navegador_visual._host(bad,{"www.pccomponentes.com","pccomponentes.com"})

if __name__ == "__main__":
    unittest.main()


class TestIntegracionCatalogo(unittest.TestCase):
    def test_http_200_elige_ligero(self):
        self.assertEqual(buscar.elegir_modalidad_publica(
            "HTTP_200_CON_DATOS", True)["metodo"], "M20_HTTP_PUBLICO")
    def test_403_elige_visual_autorizado(self):
        self.assertEqual(buscar.elegir_modalidad_publica(
            "HTTP_403_DESAFIO", True)["metodo"], "M50_NAVEGADOR_VISUAL")
    def test_403_sin_visual_se_detiene_en_alternativa(self):
        self.assertEqual(buscar.elegir_modalidad_publica(
            "HTTP_403_DESAFIO", False)["metodo"], "M90_ALTERNATIVA_OFICIAL")
    def test_429_obliga_a_detener(self):
        self.assertEqual(buscar.elegir_modalidad_publica(
            "HTTP_429", True)["estado"], "DETENER")
