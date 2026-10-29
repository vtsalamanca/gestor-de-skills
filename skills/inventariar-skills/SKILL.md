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

## Obligación de actualización al introducir herramientas (29/10/2026)
Cuando se instale, configure, sustituya, desactive o acredite una **nueva capacidad material** (MCP, navegador, agente, pasarela, servicio, runner o skill), actualizar **en el mismo trabajo** el catálogo existente del entorno operativo y este inventario si el cambio repercute en las skills. No esperar otra solicitud del usuario ni crear una décima skill por duplicación. Registrar versión, ubicación real, prueba local o extremo a extremo, autorización, cuota/dinero, límites, reversión y fecha. Leer los documentos actualizados para verificar persistencia; distinguir información meramente diseñada de herramientas realmente disponibles. No crear un temporizador de inventario sin necesidad ni autorización.

Consultar [inventario de control de Debian, CDC y MCP a demanda (29/10/2026)](references/inventario-control-debian-2026-10-29.md). El catálogo humano de utilidades está en `/home/labgestor/utilidades/CATALOGO - Herramientas del laboratorio.md`. Una edición local de skills **no** implica la publicación en el complemento privado: seguir el runbook de actualización y declarar esa fase por separado.


## Registro específico de herramientas de acceso web (27/10/2026)

Consultar [inventario de acceso web, navegador y llavero](references/inventario-acceso-web-2026-10-27.md) antes de crear un conector nuevo. Registrar método, equipo, permisos, fecha y estado comprobado; distinguir prueba de red, sesión, llavero, login y autorización oficial. Una herramienta diseñada o una cuenta autenticada en Firefox no demuestra acceso mediante su contraseña ni permisos API. Mantener el catálogo versionado en la fuente canónica y referencias locales sin secretos; actualizarlo con evidencias, no por mera presencia del programa.
