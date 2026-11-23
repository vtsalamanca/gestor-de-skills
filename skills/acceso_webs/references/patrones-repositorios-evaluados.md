# Patrones de repositorios evaluados — referencia, no instalación

## Catálogo de patrones procedentes de repositorios abiertos (evaluación de octubre de 2026)

Consultar referencias oficiales antes de cada adopción; un repositorio público no implica aprobación automática de seguridad, mantenimiento o licencia para el uso concreto. **No instalar ni ejecutar estos proyectos por defecto**: extraer primero el principio reusable y reutilizar el código existente si basta.

| Repositorio | Patrón útil | Cuándo elegirlo / límite |
| --- | --- | --- |
| [psf/requests](https://github.com/psf/requests) | Cliente HTTP simple, sesiones, timeouts y control explícito de respuestas | Sitios estáticos y peticiones puntuales; un HTTP 200 no acredita extracción |
| [encode/httpx](https://github.com/encode/httpx) | Pool de conexiones, HTTP/1.1 y HTTP/2, sincronía/asincronía, streaming y límites | Muchas solicitudes HTTP autorizadas; medir si la concurrencia realmente mejora coste total |
| [scrapy/scrapy](https://github.com/scrapy/scrapy) | Separación de spiders, selectores, pipelines, seguimiento de enlaces y paginación | Rastreo relativamente amplio con extracción estructurada; evitarlo para un par de URLs simples |
| [microsoft/playwright-python](https://github.com/microsoft/playwright-python) | Reproducción de navegación real, DOM dinámico, contextos aislados y diagnóstico de red | Cuando el contenido depende de JS/interacciones; mayor CPU, RAM y peso de instalación |
| [microsoft/playwright, HAR](https://github.com/microsoft/playwright/blob/main/docs/src/mock.md) | Captura puntual y reproducción de tráfico en pruebas | Depuración offline sin repetir peticiones; **HAR puede incluir cookies, cabeceras y datos privados: sanitizar antes de almacenar y nunca subir capturas reales a repositorios públicos** |
| [gocolly/colly](https://github.com/gocolly/colly) | Caché, límites de concurrencia/demora por dominio y respeto de robots.txt | Patrones para rastreadores eficientes; introducir Go solo con ventajas medibles respecto al stack existente |

### Recetas tecnológicas independientes del lenguaje
1. **Petición HTTP mínima:** comprobar en orden origen autorizado, URL, respuesta, tipo MIME, representación del documento, presencia de datos y siguiente página. Reutilizar sesiones en memoria y conexiones cuando esté permitido; timeouts y errores explícitos.
2. **Paginación demostrable:** identificar enlace o cursor, detener ante ausencia de avance, duplicados persistentes, límites o agotamiento real; registrar páginas vistas versus páginas estimadas. No asumir cobertura completa por recorrer una sola página.
3. **Carga JavaScript:** identificar si el dato está en HTML inicial o llega después. Diagnosticar con navegador una sola vez; si se verifica alternativa ligera permitida y estable, usarla en el conector final.
4. **Evidencia offline:** capturar únicamente muestras sintéticas o previamente anonimizadas del DOM/HTML/JSON/HAR para pruebas; aplicar tests de regresión sin contactos repetidos al origen.
5. **Extracción incremental:** calcular claves estables, almacenar hash/fecha, evitar descargar y procesar documentos sin cambios, límites por dominio y backoff en fallos transitorios. Usar ETag/Last-Modified solo si el servidor los admite y dan resultado correcto.
6. **Balance de recursos:** estimar y medir peticiones, ancho de banda, memoria pico, CPU, duración de trabajos y acciones manuales, comparando HTTP directo, crawler y navegador. El menor número de peticiones no siempre equivale al menor coste total.
7. **Autenticación responsable:** mantener el estado solo en el contexto autorizado, preferir estándares e interfaces oficiales; no exportar sesiones de navegador a runners ni conservar secretos en registros. Verificar permisos sin intentar superar mecanismos de protección.
8. **Criterio de selección:** implementar primero un caso mínimo medible en el stack existente; si falla, formular hipótesis de capa y probar el siguiente escalón. No migrar de lenguaje, herramienta o servicio por popularidad.

### Control de adopción de una dependencia
Antes de incluir código ajeno: revisar licencia y compatibilidad, mantenedores y actividad reciente, política de versiones, vulnerabilidades conocidas y cadena de dependencias; limitar permisos y comparar peso de instalación y coste de ejecución. Documentar **seleccionado / descartado / solo referencia** junto con la razón. Las referencias de este catálogo están **documentadas**, no significa que hayan sido instaladas, auditadas en profundidad, ejecutadas ni probadas contra los portales de nuestros proyectos.
