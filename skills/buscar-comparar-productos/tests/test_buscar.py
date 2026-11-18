import sys
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import buscar


TITLE = 'ASUS V16 V3607VH-TK214 - Portátil 144Hz, 16GB RAM, 512GB SSD, RTX 5050, Teclado QWERTY español'
URL = 'https://www.amazon.es/dp/B0GN5JQPVM'


class FakeResponse:
    def __init__(self, text="", status=200, url=URL):
        self.text = text
        self.status_code = status
        self.url = url
        self.headers = {"Date": "Tue, 17 Nov 2026 21:00:00 GMT"}


class FakeSession:
    def __init__(self, response):
        self.response = response
    def get(self, url, timeout, allow_redirects=True):
        return self.response


class TestPure(unittest.TestCase):
    def test_eur(self):
        self.assertEqual(buscar.money("806,66 €"), Decimal("806.66"))
        self.assertEqual(buscar.money("1.299,99 €"), Decimal("1299.99"))
        self.assertIsNone(buscar.money("Sin precio"))
    def test_features(self):
        self.assertEqual(buscar.features(TITLE), {"gpu":"RTX 5050","ram_gb":16,
            "ssd_gb":512,"hz":144,"teclado_es_explicito":True})
    def test_ram_without_label(self):
        self.assertEqual(buscar.features("RTX 5050, 16GB, 1TB SSD, W11")["ram_gb"],16)
    def test_vram_not_ram(self):
        self.assertIsNone(buscar.features("RTX 5050 8GB, 512GB SSD")["ram_gb"])
    def test_tb_and_locale(self):
        self.assertEqual(buscar.features("16GB RAM, 1TB SSD, RTX 5060")["ssd_gb"],1024)
    def test_amazon_search(self):
        fixture = '<div data-asin="B0GN5JQPVM" data-component-type="s-search-result"><h2 aria-label="'+TITLE+'"></h2><span class="a-offscreen">806,66 €</span></div>'
        offers=buscar.parse_amazon_results(fixture)
        self.assertEqual(len(offers),1)
        self.assertEqual(offers[0]["url"], URL)
        self.assertEqual(offers[0]["precio_indice_eur"],806.66)
    def test_ad_not_credible_without_detail(self):
        fixture = '<div data-asin="B0GN5JQPVM" data-component-type="s-search-result"><h2 aria-label="Anuncio patrocinado: '+TITLE+'"></h2></div>'
        offers=buscar.parse_amazon_results(fixture)
        self.assertTrue(offers[0]["patrocinado"])
        self.assertNotIn("Anuncio patrocinado",offers[0]["nombre"])
    def test_eci_search(self):
        fixture = '<article><a class="product_preview-title pds" title="'+TITLE+'" href="/electronica/A123-pr/">Portátil</a></article>'
        offers=buscar.parse_eci_results(fixture)
        self.assertEqual(len(offers),1)
        self.assertEqual(offers[0]["url"],"https://www.elcorteingles.es/electronica/A123-pr/")
    def test_amazon_detail(self):
        fixture = '<meta name="title" content="'+TITLE+'"><span class="apex-pricetopay-value"><span class="a-offscreen">806,66€</span></span><div id="availability"><span>En stock</span></div><span data-csa-c-delivery-price="GRATIS">'
        row=buscar.amazon_detail(fixture)
        self.assertEqual(row["precio_eur"],806.66)
        self.assertTrue(row["stock"])
        self.assertTrue(row["envio_general_gratis_indicio"])
        self.assertFalse(row["envio_a_destino_verificado"])
    def test_eci_detail(self):
        fixture = '<script type="application/ld+json">{"@type":"Product","name":"'+TITLE+'","offers":{"priceCurrency":"EUR","price":849.9,"availability":"https://schema.org/InStock"}}</script>'
        row=buscar.eci_detail(fixture)
        self.assertEqual(row["precio_eur"],849.9)
        self.assertTrue(row["stock"])
    def test_unknown_ecommerce(self):
        self.assertIsNone(buscar.card("Web",TITLE,"https://compras-falsas.com/dp/B0GN5JQPVM"))
    def test_status_candidate_not_certified(self):
        item={"nombre":TITLE,"nombre_ficha":TITLE,"precio_eur":806.66,"stock":True,
              "envio_a_destino_verificado":False,"garantia_verificada":False}
        row=buscar.assess(item,900)
        self.assertEqual(row["estado"],"CANDIDATO_PENDIENTE")
        self.assertIn("ENVIO_DESTINO_Y_COSTE_TOTAL",row["pendientes"])
    def test_status_verified_when_all_confirmed(self):
        item={"nombre":TITLE,"nombre_ficha":TITLE,"precio_eur":806.66,"stock":True,
              "envio_a_destino_verificado":True,"garantia_verificada":True}
        self.assertEqual(buscar.assess(item,900)["estado"],"COMPRABLE_VERIFICADO")
    def test_no_stock(self):
        item={"nombre":TITLE,"precio_eur":800,"stock":False}
        self.assertEqual(buscar.assess(item,900)["estado"],"DESCARTADO")
    def test_budget(self):
        item={"nombre":TITLE,"precio_eur":901,"stock":True}
        row=buscar.assess(item,900)
        self.assertIn("FUERA_DE_PRESUPUESTO",row["incumplimientos"])
    def test_ssd(self):
        item={"nombre":TITLE.replace("512GB SSD","500GB SSD"),"precio_eur":700,"stock":True}
        self.assertIn("SSD_INSUFICIENTE",buscar.assess(item,900)["incumplimientos"])
    def test_missing_keyboard(self):
        item={"nombre":TITLE.replace("Teclado QWERTY español",""),"precio_eur":800,"stock":True}
        self.assertIn("TECLADO_ES",buscar.assess(item,900)["pendientes"])
    def test_http_403(self):
        result,err=buscar.get(FakeSession(FakeResponse("bloqueado",403)) ,URL)
        self.assertIsNone(result)
        self.assertEqual(err,"HTTP_403")
    def test_http_challenge(self):
        result,err=buscar.get(FakeSession(FakeResponse("<html>Just a moment...</html>")),URL)
        self.assertIsNone(result)
        self.assertEqual(err,"PROTECCION_WEB")
    def test_redirect_unsafe(self):
        result,err=buscar.get(FakeSession(FakeResponse("ok",200,"https://otro-ejemplo.com")),URL)
        self.assertIsNone(result)
        self.assertEqual(err,"REDIRECCION_NO_AUTORIZADA")
    def test_no_unknown_domain(self):
        result,err=buscar.get(FakeSession(FakeResponse("ok")), "https://store-maliciosa.com")
        self.assertEqual(err,"DOMINIO_NO_AUTORIZADO")
    def test_markdown(self):
        report={"fecha_utc":"2026-11-17T21:00:00+00:00","presupuesto_total_eur":900,"destino":"Toledo",
                "candidatos_en_listados":0,"fichas_directas_comprobadas":0,"comprables_verificados":0,
                "cobertura_tiendas":[],"ofertas":[]}
        self.assertIn("Búsqueda automática desde Debian",buscar.md(report))

class TestGeneric(unittest.TestCase):
    def test_european_thousands_without_cents(self):
        self.assertEqual(buscar.money("1.199 €"), Decimal("1199"))
    def test_generic_amazon_no_gpu(self):
        fixture='<div data-asin="B0C34CGM44" data-component-type="s-search-result"><h2 aria-label="Despertador digital con temperatura"></h2><span class="a-offscreen">19,95 €</span></div>'
        offers=buscar.parse_amazon_results(fixture,require_gpu=False)
        self.assertEqual(len(offers),1)
        self.assertEqual(offers[0]["precio_indice_eur"],19.95)
    def test_generic_relevance_and_price(self):
        item={"nombre":"Despertador digital con alarma","nombre_ficha":"Despertador digital con alarma",
              "precio_eur":19,"stock":True,"envio_a_destino_verificado":False,"garantia_verificada":False}
        x=buscar.assess(item,50,profile="general",product_query="despertador digital")
        self.assertEqual(x["estado"],"CANDIDATO_PENDIENTE")
        self.assertNotIn("GPU_INCOMPATIBLE",x["incumplimientos"])
    def test_generic_irrelevant(self):
        item={"nombre":"Televisor 4K OLED","precio_eur":19,"stock":True}
        x=buscar.assess(item,50,profile="general",product_query="despertador digital")
        self.assertIn("NO_COINCIDE_BUSQUEDA",x["incumplimientos"])
    def test_general_mandatory_attribute_not_assumed_false(self):
        item={"nombre":"Despertador digital simple","precio_eur":19,"stock":True}
        x=buscar.assess(item,50,profile="general",product_query="despertador digital",must=["proyector"])
        self.assertIn("REQUISITO_NO_VERIFICADO:proyector",x["pendientes"])

class TestMediaMarkt(unittest.TestCase):
    def test_tm_gpu(self):
        self.assertEqual(buscar.features("GeForce RTX™ 5050, 16GB RAM")["gpu"],"RTX 5050")
    def test_listed_product_price_is_lead_not_verified(self):
        fixture='<script type="application/ld+json">{"@type":"ItemList","itemListElement":[{"item":{"@type":"Product","name":"Portátil RTX™ 5050 16GB RAM 512GB SSD","url":"https://www.mediamarkt.es/es/product/_ejemplo.html","offers":{"priceCurrency":"EUR","price":799}}}]}</script>'
        row=buscar.parse_media_results(fixture)
        self.assertEqual(len(row),1)
        self.assertEqual(row[0]["precio_indice_eur"],799.0)
        self.assertNotIn("stock",row[0])
    def test_direct_buyaction(self):
        fixture='<script type="application/ld+json">{"@type":"BuyAction","object":{"@type":"Product","name":"Portátil RTX™ 5050, 16GB RAM","offers":{"priceCurrency":"EUR","price":799,"availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition","shippingDetails":{"shippingRate":{"value":0}}}}}</script>'
        row=buscar.media_detail(fixture)
        self.assertEqual(row["precio_eur"],799.0)
        self.assertTrue(row["stock"])
        self.assertTrue(row["envio_general_gratis_indicio"])
        self.assertFalse(row["envio_a_destino_verificado"])

class TestMediaTechSpecs(unittest.TestCase):
    def test_unique_hz_and_es_keyboard(self):
        fixture=(
         '<script type="application/ld+json">{"@type":"BuyAction","object":{"@type":"Product",'
         '"name":"Portátil RTX™ 5050 16GB RAM 512GB SSD",'
         '"offers":{"priceCurrency":"EUR","price":799,'
         '"availability":"https://schema.org/InStock"}}}</script>'
         '"name":"Frecuencia de actualización","type":null,"unit":"Hz","value":"165"'
         '"name":"Tipo de teclado","type":null,"unit":null,"value":"Teclado QWERTY español"')
        row=buscar.media_detail(fixture)
        self.assertEqual(row["especificaciones_ficha"],{"hz":165,"teclado_es_explicito":True})
        x=buscar.assess({"nombre":row["nombre_ficha"],**row},900)
        self.assertNotIn("HZ",x["pendientes"])
        self.assertNotIn("TECLADO_ES",x["pendientes"])
    def test_conflicting_hz_not_verified(self):
        fixture=(
         '<script type="application/ld+json">{"@type":"BuyAction","object":{"@type":"Product",'
         '"name":"Portátil RTX™ 5050 16GB RAM 512GB SSD",'
         '"offers":{"priceCurrency":"EUR","price":799,'
         '"availability":"https://schema.org/InStock"}}}</script>'
         '"name":"Frecuencia de actualización","type":null,"unit":"Hz","value":"165"'
         '"name":"Frecuencia de actualización","type":null,"unit":"Hz","value":"144"')
        row=buscar.media_detail(fixture)
        self.assertIsNone(row["especificaciones_ficha"]["hz"])

class TestSearchCoverage(unittest.TestCase):
    def test_http_200_no_extraction_not_success(self):
        self.assertEqual(buscar.classify_empty_result(
            "Amazon",'<div data-component-type="s-search-result">sin h2</div>'),
            "EXTRACCION_FALLIDA_CON_TARJETAS")
    def test_200_unknown_layout(self):
        self.assertEqual(buscar.classify_empty_result("Amazon",'<html>Página no esperada</html>'),
                         "RESPUESTA_SIN_CATALOGO_VERIFICABLE")
    def test_explicit_empty(self):
        self.assertEqual(buscar.classify_empty_result("Amazon","No se han encontrado resultados"),
                         "SIN_RESULTADOS_DECLARADOS")

if __name__ == "__main__":
    unittest.main()
