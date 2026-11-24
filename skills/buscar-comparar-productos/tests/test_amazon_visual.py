import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from amazon_visual import AmazonVisual, VisualError, match_product, search_candidate, offer_from_text
import buscar

class TestAmazonVisual(unittest.TestCase):
    def test_model_and_size_strict(self):
        self.assertTrue(match_product("Xiaomi S Mini LED 55", "Xiaomi S Mini LED 55 pulgadas"))
        self.assertFalse(match_product("Xiaomi S Mini LED 55", "Xiaomi S Mini LED 65 pulgadas"))
        self.assertFalse(match_product("TCL 55T8D", "TCL 55P8L"))
        self.assertTrue(match_product("TCL 55T8D", "TCL 55T8D 55 Pulgadas Mini LED"))

    def test_merchant_listing_not_validated_price(self):
        c=search_candidate("TCL 55T8D 55 Pulgadas Precio, página del producto 449,00 €",
                           "TCL 55T8D 55 Pulgadas",
                           "https://www.amazon.es/TCL-55T8D/dp/B0GR9JWH4T/ref=sr_1_6")
        self.assertEqual(c["precio_indice_eur"],449)
        self.assertNotIn("precio_eur",c)
        self.assertIsNone(search_candidate("TCL 65T8D Precio, página del producto 449,00 €",
                                            "TCL 55T8D 55 Pulgadas",
                                            "https://www.amazon.es/dp/B0GR9JWH4T"))

    def test_offer_not_full_buyable(self):
        o=offer_from_text("Nuevo 460,51 € Entrega GRATIS","OCASIONIA")
        self.assertEqual(o["precio_eur"],460.51)
        self.assertEqual(o["vendedor"],"OCASIONIA")
        self.assertIsNone(o["stock"])
        self.assertFalse(o["envio_a_destino_verificado"])
        self.assertIsNone(offer_from_text("Ver todas las opciones"))

    def test_exact_url_validation(self):
        same=AmazonVisual._same_url
        self.assertTrue(same("https://www.amazon.es/TCL-55T8D/dp/B0GR9JWH4T/ref=abc",
                             "https://www.amazon.es/dp/B0GR9JWH4T"))
        self.assertFalse(same("https://www.amazon.es/dp/B0GR9JWH4T",
                              "https://www.amazon.es/dp/B0DJM9GBHK"))
        self.assertFalse(same("https://evil.example/dp/B0GR9JWH4T",
                              "https://www.amazon.es/dp/B0GR9JWH4T"))

    def test_foco_en_otro_dominio_detiene_lectura(self):
        v=object.__new__(AmazonVisual)
        v.requested="https://www.amazon.es/dp/B0GR9JWH4T"
        v._current=lambda:object()
        v._url=lambda window:"https://otro-sitio.example/privado"
        with self.assertRaises(VisualError):v._checked_document()

    def test_buscador_integrado_no_confunde_indice_con_ficha(self):
        class FakeBrowser:
            def search(self,q):
                return [{"url":"https://www.amazon.es/dp/B0GR9JWH4T",
                         "nombre":"TCL 55T8D 55 Pulgadas Mini LED",
                         "precio_indice_eur":449.0,"id_producto":"B0GR9JWH4T"}]
            def detail(self,url,title):
                return {"nombre_ficha":title,"precio_eur":449.0,
                        "stock":None,"vendedor":"Amazon",
                        "envio_a_destino_verificado":False,"garantia_verificada":False}
            def close_own_tab(self):
                return True
        args=SimpleNamespace(perfil="general",presupuesto=500,min_hz=144,
                             teclado_es=True,producto="TCL 55T8D",debe_contener=[],
                             max_fichas_por_tienda=2)
        rows,found,verified=buscar.amazon_por_acceso_webs(["TCL 55T8D"],args,factory=FakeBrowser)
        self.assertEqual(len(found),1)
        self.assertEqual(len(verified),1)
        self.assertEqual(verified[0]["precio_eur"],449.0)
        self.assertEqual(verified[0]["estado"],"CANDIDATO_PENDIENTE")
        self.assertIn("ENVIO_DESTINO_Y_COSTE_TOTAL",verified[0]["pendientes"])

    def test_storage_filter_excludes_cases_and_cables(self):
        query="SSD SATA 2.5 500GB"
        self.assertFalse(buscar.storage_candidate_matches(query,"SABRENT Carcasa HDD SSD de 2,5 pulgadas"))
        self.assertFalse(buscar.storage_candidate_matches(query,"Cable adaptador SATA a USB para SSD 500GB"))
        self.assertFalse(buscar.storage_candidate_matches("HDD SATA 2.5 500GB","Disco duro portátil 500 GB HDD USB 3.0 2.5 pulgadas"))
        self.assertFalse(buscar.storage_candidate_matches(query,"Seagate BarraCuda HDD 500GB"))
        self.assertTrue(buscar.storage_candidate_matches(query,"Crucial BX500 SSD interno 500GB SATA 2,5 pulgadas"))
        self.assertTrue(buscar.storage_candidate_matches(query,"Silicon Power Ace A55 512GB SSD interno 2,5 pulgadas"))
        self.assertTrue(buscar.storage_candidate_matches(query,"DIGIERA 512GB SSD SATA 6Gb/s interno 2,5 pulgadas"))
        self.assertFalse(buscar.storage_candidate_matches(query,"Fikwot FS810 SSD interno 128GB SATA"))
        self.assertFalse(buscar.storage_candidate_matches(query,"Ediloca SSD interno (128GB) SATA 500MB/s"))
        self.assertFalse(buscar.storage_candidate_matches(query,"SSD 500GB/1TB SATA"))
        self.assertTrue(buscar.storage_candidate_matches(query,"SSD SATA 480GB 2.5 pulgadas"))
        self.assertFalse(buscar.storage_candidate_matches("HDD SATA 1TB","Seagate BarraCuda 500GB HDD SATA"))
        self.assertTrue(buscar.storage_candidate_matches("portatil gaming RTX 4060","ASUS gaming RTX 4060"))
        self.assertFalse(buscar.storage_candidate_matches("HDD 2.5 1TB","WD10EURX HDD interno 1TB 3.5 pulgadas"))
        self.assertFalse(buscar.storage_candidate_matches("HDD 2.5 1TB","WD10EURX HDD interno 1TB"))
        self.assertTrue(buscar.storage_candidate_matches("HDD 2.5 1TB","Seagate BarraCuda HDD interno 1TB 2,5 pulgadas"))
        item={"nombre":"SABRENT Carcasa para SSD 500GB SATA","stock":True,
              "precio_eur":10.0,"envio_a_destino_verificado":False,"garantia_verificada":False}
        checked=buscar.assess(item,100,profile="general",product_query=query)
        self.assertEqual(checked["estado"],"DESCARTADO")
        self.assertIn("ACCESORIO_O_TIPO_INCORRECTO",checked["incumplimientos"])

    def test_buybox_variant_checked_and_seller_scope(self):
        from amazon_visual import _buybox_from_doc
        class Node:
            def __init__(self,role,name="",children=(),checked=False,text=""):
                self.role,self.name,self.children,self.checked,self.text=role,name,list(children),checked,text
                for child in self.children:child.parent=self
            def get_role_name(self):return self.role
            def get_name(self):return self.name
            def get_child_count(self):return len(self.children)
            def get_child_at_index(self,i):return self.children[i]
            def get_state_set(self):return self
            def contains(self,value):return self.checked
            def get_parent(self):return self.parent
            def get_character_count(self):return len(self.text)
        class Atspi:
            StateType=SimpleNamespace(CHECKED="checked")
            Text=SimpleNamespace(get_text=lambda node,a,b:node.text)
        seller=Node("section",text="Amazon")
        heading=Node("heading","Remitente / Vendedor")
        block=Node("section",children=[heading,seller])
        chosen=Node("radio button",'55" 449,00 € En stock',checked=True)
        other=Node("radio button",'65" 549,00 € En stock',checked=False)
        root=Node("section",children=[other,chosen,block])
        row=_buybox_from_doc(root,Atspi,"TCL 55T8D 55 Pulgadas")
        self.assertEqual(row["precio_eur"],449)
        self.assertEqual(row["vendedor"],"Amazon")
        self.assertTrue(row["stock"])
        self.assertIsNone(_buybox_from_doc(root,Atspi,"TCL 65T8D 65 Pulgadas"))

    def test_visual_initialization_failure_does_not_abort_search(self):
        args=SimpleNamespace(perfil="general",presupuesto=500,min_hz=144,
                             teclado_es=True,producto="TCL 55T8D",debe_contener=[],
                             max_fichas_por_tienda=2)
        def fail():
            raise RuntimeError("interfaz no disponible")
        rows,items,verified=buscar.amazon_por_acceso_webs(["TCL 55T8D"],args,factory=fail)
        self.assertIn("BLOQUEADO_VISUAL_RuntimeError",rows[0]["resultado"])
        self.assertFalse(items)
        self.assertFalse(verified)


if __name__=="__main__":
    unittest.main()
