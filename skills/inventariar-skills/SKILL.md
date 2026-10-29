---
name: inventariar-skills
description: Inventaría skills y plugins existentes, detecta duplicados, registra versiones y planifica actualizaciones seguras sin reinstalar ni actualizar automáticamente.
---
# Inventariar skills

## Procedimiento
1. Lee primero el catálogo de skills habilitadas y los plugins disponibles con las herramientas de la sesión. No atribuyas acceso a dispositivos remotos no conectados.
2. Construye una ficha por skill: nombre, finalidad, plataforma, origen, versión conocida, permisos, coste marginal, último análisis, riesgos y evidencia. Marca como desconocido lo no verificable.
3. Agrupa funciones similares, detecta duplicados por objetivo/entorno, y recomienda reutilizar, fusionar o separar. No desinstales por iniciativa propia.
4. Para propuestas de actualización, compara notas, archivos modificados, dependencias y coste con la versión anterior; solicita auditoría estática mediante `auditar-skills`.
5. Da prioridades por impacto: seguridad, incompatibilidad, obsolescencia, mantenimiento o valor real. No actualizar para subir números sin beneficio.
6. Presenta inventario exportable como tabla o Markdown/CSV si se solicita. Si se requiere persistirlo fuera de la conversación, pide destino o utiliza el ya expresamente indicado; no afirmes que hay una base de datos continua sin ella.
7. Cualquier publicación, instalación, desinstalación o cambio persistente requiere la autorización pertinente. Para operación facturable, presupuesto cero hasta tarifa/saldo/coste y autorización explícita.

## Salida
Resumen de cobertura, duplicados, elementos a revisar y recomendación priorizada. Indica fechas de comprobación y **desconocido** cuando no pueda comprobarse mantenimiento/versión.

## Detección obligatoria y permiso previo (29/10/2026)
En las **mismas situaciones de antes** (instalar, configurar, sustituir, retirar o verificar una nueva capacidad material), detectar sin que el usuario lo recuerde la necesidad de actualizar catálogo, inventario, resguardos, snapshots y distribución de habilidades/herramientas. **No escribir todavía.**

Antes de cada lote, proponer qué elementos, qué archivos, qué resguardos, qué destinos (Debian, GitHub, Bibliotecario, plugin, etc.) y qué costes/cuotas se verían afectados y **pedir autorización expresa para catalogación y resguardo**. La autorización de desarrollo o instalación no basta. Si el usuario solicita expresamente ese inventario/respaldo concreto, ya cuenta como permiso para dicho alcance. Tras recibir permiso, realizar en esa misma ocasión los registros y copias, verificar y publicar solo si esa distribución estaba comprendida. Con negativa, silencio o aplazamiento, continuar el trabajo restante pero dejar `CATALOGACION_PENDIENTE_AUTORIZACION` / `RESGUARDO_PENDIENTE_AUTORIZACION` en el chat, sin registrar pendientes en otra base.

Aplicar [protocolo canónico de autorización previa](references/autorizacion_catalogacion_y_resguardo.md). Consultar también [inventario de control de Debian, CDC y MCP](references/inventario-control-debian-2026-10-29.md) y `/home/labgestor/utilidades/CATALOGO - Herramientas del laboratorio.md`. Documentar, cuando se autorice, versión, ubicación, prueba local/E2E, coste en euros y cuota, permiso, riesgos, reversión y fecha. No crear temporizadores por esta política. La edición local de una skill no equivale a publicación del plugin privado.

## Registro específico de herramientas de acceso web (27/10/2026)

Consultar [inventario de acceso web, navegador y llavero](references/inventario-acceso-web-2026-10-27.md) antes de crear un conector nuevo. Registrar método, equipo, permisos, fecha y estado comprobado; distinguir prueba de red, sesión, llavero, login y autorización oficial. Una herramienta diseñada o una cuenta autenticada en Firefox no demuestra acceso mediante su contraseña ni permisos API. Mantener el catálogo versionado en la fuente canónica y referencias locales sin secretos; actualizarlo con evidencias, no por mera presencia del programa.
