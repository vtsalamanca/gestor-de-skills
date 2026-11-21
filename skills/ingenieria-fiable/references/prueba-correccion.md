# Evidencia reproducible de reparación (herramienta propia)

La utilidad Python estándar tools/prueba_correccion.py complementa los tests del proyecto y el detector estático verificador_trabajo.py. Inspiración conceptual: comprobaciones de huellas, repetición del fallo original y verificación posterior. **No incorpora ni necesita la skill de pago Proof of Fix de Agensi.**

## Contrato

Solo usar con proyecto y comandos de prueba autorizados, archivos seleccionados y un caso de reproducción explícito. No ejecutar pruebas genéricas sin entender qué modifican, ni activar hooks, trabajos de CI, instalaciones, APIs, datos privados o servicios facturables. La utilidad no tiene acceso propio a redes; el comando de prueba que se le suministre sí podría tenerlo, por eso debe revisarse antes.

1. Formular una condición de aceptación concreta con etiqueta R1, R2, etc.
2. Antes de corregir, ejecutar exactamente el test que demuestra el defecto: salida distinta de cero, no error de entorno.
3. Aplicar la corrección mínima; no cambiar el comando de test ni las etiquetas.
4. Repetir la misma prueba; exigir salida cero y que el test no altere los archivos vigilados.
5. Verificar que el conjunto de archivos vigilados conserva sus huellas tras la prueba. Si cambia cualquier byte, la evidencia caduca, incluso si solo cambia un comentario.
6. Inspeccionar los resultados funcionales, assertions, casos negativos y otras dependencias no incluidas. Un recibo coherente no es una prueba independiente de calidad, honestidad, integridad de logs o despliegue.

## Ejemplo con archivos ficticios

Desde el proyecto cuyos archivos se van a revisar, después de localizar la ruta de la skill instalada:

    TOOL=/ruta/al/gestor-de-skills/skills/ingenieria-fiable/tools/prueba_correccion.py
    python3 "$TOOL" record --root . --evidence /tmp/caso-123.json --phase before --requirement R1 --watch src/parser.py --watch tests/test_parser.py -- python3 -m unittest tests.test_parser
    # aplicar cambio
    python3 "$TOOL" record --root . --evidence /tmp/caso-123.json --phase after --requirement R1 --watch src/parser.py --watch tests/test_parser.py -- python3 -m unittest tests.test_parser
    python3 "$TOOL" check --root . --evidence /tmp/caso-123.json

Elegir una ubicación local privada para los recibos, nunca un repositorio público ni un directorio compartido. Los recibos contienen nombres relativos, hash del directorio del proyecto, marcas de tiempo, etiquetas, códigos de salida y SHA-256; no guardan salida de pruebas ni contenidos de archivo. No guardan el propio comando de prueba: solo su SHA-256 para comprobar igualdad, sin reproducir argumentos que pudieran incluir secretos. Los datos se escriben con permiso 0600.

## Limitaciones y manejo de incertidumbre

- Si el test anterior ya pasa, no se acredita haber reproducido el fallo; el veredicto queda incompleto.
- Si las dos ejecuciones no usan el mismo comando exacto, el recibo falla.
- Si la prueba cambia archivos vigilados o estos cambian después, hay que obtener nueva evidencia.
- No asume que las rutas vigiladas cubren todo el programa. No analiza automáticamente dependencias ni comprueba que el caso original representa la incidencia real.
- No verifica ejecución en producción ni protege el JSON contra manipulación o falsificación: manifiesto **de coherencia**, no firma ni certificación externa.
- Una excepción o fallo del entorno puede producir exit distinto de cero; la persona o agente debe comprobar que el fallo anterior es el defecto buscado, no un test mal configurado.
- Un comando de prueba podría tener efectos secundarios. Revisarlo, utilizar fixtures sintéticos y aislarlo antes de ejecutarlo.
- No incluir secretos, historiales privados, tokens o rutas sensibles entre los archivos vigilados.
- No presentar la prueba como universal para proyectos frontend, navegador, MCP o sistemas distribuidos: estos requieren comprobación end-to-end independiente.

Pruebas del verificador: python3 -m unittest discover -s tests -p 'test_prueba_correccion.py' -v
