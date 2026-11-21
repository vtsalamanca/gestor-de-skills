# Portabilidad de skills entre ChatGPT, Codex, Windows y Debian

El validador propio `tools/portabilidad_agentes.py` busca rutas rígidas de usuario, manifiestos incompatibles, enlaces locales rotos y patrones de riesgo antes de distribuir skills. **No ejecuta** el código inspeccionado, no consulta la red ni instala nada.

Uso desde la raíz del repositorio:

    python3 skills/integrar-skills/tools/portabilidad_agentes.py --root .

Los **errores** bloquean la distribución; las advertencias exigen revisión. Las rutas Debian específicas pueden ser documentación deliberada, no fallos: no sustituirlas sin análisis. El validador también puede dar falsos negativos. No afirmar compatibilidad Windows por un resultado estático: allí se necesitan pruebas reales de cliente/instalación.

Para regresiones: `python3 -m unittest discover -s tests -p test_tres_mejoras_agentes.py -v`. La sincronización real con Codex/ChatGPT se comprueba en cada destino, nunca por una versión escrita en README. Inspiración conceptual del marketplace Agensi; implementación **propia** sin importar su código.
