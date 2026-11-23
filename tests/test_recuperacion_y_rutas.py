"""Evaluación L0/L1 determinista: no simula una selección real del modelo."""
from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'skills/control-laboratorio/references/20-indice-operativo.md'
class TestRutas(unittest.TestCase):
    def test_canonical_index_has_all_versions(self):
        text=INDEX.read_text()
        skills=list((ROOT/'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills),11)
        for path in skills:
            name=path.parent.name
            self.assertIn(f'| `{name}` |',text)
            m=re.search(r'^version: (\S+)',path.read_text(),re.M)
            version=m.group(1) if m else 'sin versión individual'
            self.assertIn(f'| `{name}` | {version} |',text)
    def test_router_scenarios_13(self):
        text=INDEX.read_text()
        cases={
          'actualiza el complemento':'control-laboratorio',
          'publica el plugin sin ZIP manual':'ingenieria-fiable',
          'repara BrowserLearn':'acceso_webs',
          'entra en InfoJobs':'acceso_webs',
          'consulta Educamos':'control-laboratorio',
          'busca oferta en Amazon':'buscar-comparar-productos',
          'continúa el trabajo pendiente':'organizaciondeltrabajo',
          'qué hemos aprendido sobre FTS5':'bibliotecario-memoria',
          'Control Debian da error':'control-laboratorio',
          'necesito una skill nueva':'descubrir-skills',
          'inventaría herramientas':'inventariar-skills',
          'comprueba versiones Codex':'integrar-skills',
          'redacta pruebas de regresión':'ingenieria-fiable'}
        for phrase,skill in cases.items():
            with self.subTest(phrase=phrase):
                row=next(x for x in text.splitlines() if x.startswith('| '+phrase+' |'))
                self.assertIn(f'| `{skill}` |',row)
    def test_current_runbook_no_obsolete_eight_or_manual_zip(self):
        active=(ROOT/'skills/ingenieria-fiable/references/actualizar-skills.md').read_text()
        self.assertNotIn('ocho habilidades',active)
        self.assertNotIn('adjuntar el ZIP a la misma conversación',active.lower())
        self.assertIn('publicacion-autonoma-complemento.md',active)
        self.assertIn('actualizar-skills-historico.md',active)
    def test_historical_text_retained(self):
        checks=[
          'skills/ingenieria-fiable/references/actualizar-skills-historico.md',
          'skills/organizaciondeltrabajo/references/historico-operativo.md',
          'skills/acceso_webs/references/lecciones-historicas-acceso.md',
          'skills/acceso_webs/references/patrones-repositorios-evaluados.md']
        for c in checks:
            with self.subTest(c=c):
                self.assertTrue((ROOT/c).is_file())
                self.assertGreater(len((ROOT/c).read_text()),200)
    def test_all_internal_links_exist(self):
        broken=[]
        for p in ROOT.glob('skills/**/*.md'):
            s=p.read_text()
            for ref in re.findall(r'\]\(([^)]+)\)',s):
                if ref.startswith(('https:','http:','#','mailto:')): continue
                dest=(p.parent/ref.split('#')[0]).resolve()
                if not dest.is_file(): broken.append((str(p.relative_to(ROOT)),ref))
        self.assertEqual(broken,[])
    def test_entry_size_declined(self):
        self.assertLess((ROOT/'skills/organizaciondeltrabajo/SKILL.md').stat().st_size,20000)
        self.assertLess((ROOT/'skills/acceso_webs/SKILL.md').stat().st_size,20000)
    def test_manifest_versions_same(self):
        a=json.loads((ROOT/'.codex-plugin/plugin.json').read_text())
        b=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
        self.assertRegex(a['version'],r'^0\.4\.[0-9]+$')
        self.assertEqual(b['plugins'][0]['version'],a['version'])
if __name__=='__main__': unittest.main()
