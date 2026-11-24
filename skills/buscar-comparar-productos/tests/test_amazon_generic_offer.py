
import unittest
from types import SimpleNamespace
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from amazon_visual import _buybox_from_doc

class Node:
    def __init__(self,role,name="",children=(),checked=False,text=""):
        self.role,self.name,self.children,self.checked,self.text=role,name,list(children),checked,text
        self.parent=None
        for child in self.children: child.parent=self
    def get_role_name(self): return self.role
    def get_name(self): return self.name
    def get_child_count(self): return len(self.children)
    def get_child_at_index(self,i): return self.children[i]
    def get_state_set(self): return self
    def contains(self,value): return self.checked
    def get_parent(self): return self.parent
    def get_character_count(self): return len(self.text)
class Atspi:
    StateType=SimpleNamespace(CHECKED="checked")
    Text=SimpleNamespace(get_text=lambda n,a,b:n.text)

def variant(label,checked=True): return Node("radio button",label,checked=checked)
def choices(*nodes): return Node("panel","Selecciona una opción",nodes)
def form(*nodes):
    return Node("form",children=[*nodes,Node("button","Añadir a la cesta"),Node("panel","Información del vendedor, el envío y las opciones de compra")])
def amount(t): return Node("section",text=t)
def root(*nodes): return Node("section",children=nodes)
def parse(doc,title): return _buybox_from_doc(doc,Atspi,title)

class GenericOfferTests(unittest.TestCase):
    def test_ssd_variant(self):
        o=parse(root(choices(variant("1TB 146,95 €146,95€ En stock"),variant("2TB 259,99 €",False))),"Kingston NV3 1 TB M.2 2280")
        self.assertEqual(o["precio_eur"],146.95)
        self.assertTrue(o["stock"])
    def test_size_and_color(self):
        self.assertEqual(parse(root(choices(variant("Azul 19,99 € En stock"))),"Camiseta Azul talla M")["precio_eur"],19.99)
    def test_mismatched_capacity(self):
        self.assertIsNone(parse(root(choices(variant("2 TB 259,99 €"))),"SSD 1TB"))
    def test_unchecked_and_recommendation(self):
        self.assertIsNone(parse(root(choices(variant("1TB 22,00 €",False)),amount("22,00 €")),"SSD 1TB"))
    def test_unscoped_checked_recommendation(self):
        self.assertIsNone(parse(root(variant("1TB 22,00 €")),"SSD 1TB"))
    def test_main_form_without_variant_price(self):
        o=parse(root(form(amount("265,99€"),amount("En stock")),amount("1833,87 €"),amount("12,00 €")),"SSD Lexar NQ790 2TB")
        self.assertEqual(o["precio_eur"],265.99)
        self.assertTrue(o["stock"])
    def test_main_form_ambiguous(self):
        self.assertIsNone(parse(root(form(amount("25,00 €"),amount("30,00 €"))),"Producto"))
    def test_old_price_and_shipping_not_offer(self):
        self.assertIsNone(parse(root(form(amount("El precio de lista era de 29,99 €"),amount("6,00 € de envío"))),"Producto"))
    def test_variant_conflicts(self):
        self.assertIsNone(parse(root(choices(variant("1TB 146,95 €")),form(amount("149,99 €"))),"SSD 1TB"))
    def test_large_price(self):
        self.assertEqual(parse(root(form(amount("1833,87 €"))),"Ordenador")["precio_eur"],1833.87)
