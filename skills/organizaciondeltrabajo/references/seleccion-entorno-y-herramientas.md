# Selección vigente del entorno local y comparación de herramientas

Consultar primero SKILL.md y el índice; las referencias a Desktop Commander son ejemplos históricos, no preferencia actual sobre Control Debian.

## MCP local: alternativa prioritaria cuando exista acceso autorizado
En proyectos de programación, antes de emplear Codex, Work o GitHub Actions para pruebas repetitivas, comprobar si existe un MCP de acceso al equipo propio (p. ej., Desktop Commander) **realmente conectado** y si su coste y permisos son aceptables. Priorizar lectura y pruebas locales reproducibles con datos sintéticos, sin servicios facturables. No conectar dispositivos, ampliar permisos, instalar dependencias, ejecutar código ajeno ni automatizar el inicio sin autorización.

Una skill no proporciona acceso al PC por sí sola: comprobar dispositivo en línea, ruta permitida, terminal disponible, repositorio canónico, estado Git y límites de seguridad. No confundir allowedDirectories (operaciones de archivos) con aislamiento efectivo de PowerShell; la terminal requiere controles independientes. Mantener la sesión local activa y verificar resultados, hashes y estado Git antes y después; detener ante divergencias, cambios inesperados o costes desconocidos. Consultar `ingenieria-fiable/references/mcp-local.md` para procedimiento técnico y evidencias.

## Puerta reforzada de descubrimiento y comparación de herramientas (lección Firecrawl)
Antes de implementar una solución nueva, cambiar de herramienta o realizar otra serie de pruebas ante un bloqueo:
1. Consultar **una vez por bloque de trabajo** el inventario actual de skills, plugins, conectores, código, repositorios y herramientas del entorno real (Chat, Codex, Work o local); comprobar su disponibilidad y alcance. Reutilizar inventarios ya válidos, sin búsquedas redundantes.
2. Comparar al menos la solución ya existente y alternativas pertinentes de bajo consumo: API/feed oficial gratuito, HTTP HTML/JSON, librería o conector propio, análisis local, navegador, Firecrawl u otra herramienta especializada *solo como candidata*. Comprobar antes límites, mantenimiento, privacidad, licencia, permisos, tarifas, saldo, estimación de consumo y cobertura.
3. Seleccionar el método por **coste total efectivo** (dinero, créditos, CPU, memoria, ancho de banda, minutos de GitHub Actions, mantenimiento, fiabilidad y tiempo/intervención del usuario), no por comodidad ni popularidad. Herramienta de investigación puede ser distinta del conector de producción; priorizar producción ligera y autónoma.
4. Si una serie de fallos no converge, **detener el procedimiento repetitivo** y revisar la capa afectada, la hipótesis y las alternativas que aún no se evaluaron; agrupar experimentos discriminantes y comparar antes de otra ejecución.
5. Registrar de modo compacto `problema | herramientas disponibles y evaluadas | opción seleccionada | opciones descartadas y motivo | prueba | coste/cuota estimada o medida | nuevo conocimiento reutilizable`. No dar por evaluado algo solo porque figura instalado.
6. Para acceso a webs, autenticación, scraping y desarrollo de conectores, consultar `acceso_webs` cuando esté disponible; sus patrones genéricos prevalecen sobre repetir experiencias específicas de proyectos. Si no está cargada, consultar la fuente canónica o seguir las pautas de esta skill.
**Límite:** descubrir/comparar no implica autorización para ejecutar servicios con tarifas por uso; presupuesto adicional 0 € hasta permiso concreto.
