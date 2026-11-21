# Verificador estructural de trabajos de agentes

## Origen y licencia de la solución
Implementación propia de `gestor-de-skills` con Python estándar. No contiene ni redistribuye código de Agensi. Se evaluó públicamente la ficha de `agent work verifier` (https://www.agensi.io/skills/agent-work-verifier), pero no se pudo obtener su código completo ni verificar su licencia para copia: **no fue instalado ni incorporado**.

## Cuándo utilizarlo
Durante la revisión de código escrito o modificado por un agente, **además** de los tests, comprobaciones de estado y validación funcional. Limitarlo a archivos realmente modificados y aprobados. No sustituye ejecutar tests, validar una integración real o comprobar una entrega.

```sh
python3 skills/ingenieria-fiable/tools/verificador_trabajo.py --base HEAD~1
python3 skills/ingenieria-fiable/tools/verificador_trabajo.py --json --fail-on warning src/modulo.py tests/test_modulo.py
```

## Comportamiento
- Python: análisis AST estático (no ejecuta los archivos). Marca como críticos los cuerpos de funciones vacíos, `pass`, `...`, `raise NotImplementedError` y errores de sintaxis/lectura. Excluye los métodos con `@abstractmethod` o `@overload`.
- En ficheros `test_*.py` o `*_test.py`: avisa si `test_*` no contiene una comprobación sintáctica `assert`, una llamada `assert*` o `raises`/`warns`. El aviso no equivale a demostrar un test inútil.
- Avisa sobre excepciones descartadas con un cuerpo placeholder y puntos de interrupción `breakpoint()` / `pdb.set_trace()`.
- JavaScript/TypeScript: heurísticas de línea para `debugger;` y `test.only`, `it.only`, `describe.only`. Puede señalar comentarios como falsos positivos.
- Salida legible o JSON, `--fail-on critical` predeterminado (código 1 solo con críticos); `--fail-on warning` endurece la política. Código 2 para error al consultar Git.

## Límites y seguridad
Escanea únicamente rutas explícitas o nombres de archivos cambiados entre la revisión Git `--base` y HEAD; no ejecuta la aplicación ni instala dependencias. No leer automáticamente secretos ni escanear de forma recursiva todo el hogar. La búsqueda de referencias o assertions es heurística: puede generar falsos positivos y falsos negativos. Excepciones descartadas pueden ser intencionadas; revisar cada hallazgo. JavaScript se analiza mediante patrones, no con AST. No crear hooks, jobs ni bloqueo automático de despliegues sin autorización específica.

## Pruebas reproducibles
`python3 -m unittest discover -s tests -p test_verificador_trabajo.py -v` cubre hallazgos y casos válidos. Ejecutar además la suite del repositorio antes de distribuir. Registrar resultado, SHA del commit y revisión afectada.
