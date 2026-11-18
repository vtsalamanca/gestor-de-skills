# Guía rápida para recuperar el mando del laboratorio

## Checklist previo a cualquier encargo
- ¿Qué pidió exactamente el usuario? ¿Incluye ejecución, edición, envío, borrado o publicación?
- ¿Ya existe un procedimiento probado? Recuperar Bibliotecario y documento, no volver a construir.
- ¿Qué herramientas del chat están conectadas y autorizadas ahora? Preferir Control Debian.
- ¿Qué componente local está vivo? Confirmar UID, servicio, proceso, versión y directorio.
- ¿Hay riesgo de coste, secreto, pérdida de datos o intervención gráfica del usuario?
- ¿Cuál es la prueba mínima que confirma la postcondición?
- ¿Qué debo limpiar y qué hito merece relectura del Bibliotecario?

## Acciones típicas y primera fuente
| Petición | Punto de entrada | No confundir con |
|---|---|---|
| «Comprueba Debian» | Control Debian estado, servicio y una operación real | un único flag de túnel |
| «Soluciona la denegación» | límites de MCP, operación, UID y permiso local | autorización global ilimitada |
| «Entra en un portal» | LAB-AUTH, sesión existente, adaptador verificado | introducir clave en el chat |
| «InfoJobs MFA» | Firefox dedicado + Thunderbird LAB-AUTH, intento único | nueva cuenta Gmail OAuth |
| «Educamos adjuntos» | colector y prueba del fichero, leído/no leído | contador agregado |
| «Busca curro» | servicio diario, ATE privado, fuentes parciales | repetir scrape sin motivo |
| «Envía informe diario» | estado del colector y Automations por separado | run_now inline |
| «Publica nuestras skills» | crear/auditar/integrar, Git SHA, ZIP, Plugin Creator | push = plugin cargado |
| «Ordena el escritorio» | ventanas propiedad de la prueba y estado usuario | cerrar todas |
| «Elimina backups» | inventario, hash, recuperación y autorización explícita | limpieza automática |
| «Recupera lo que hicimos» | buscar expediente → brief → documento → readback | memoria del chat como base única |
| «Pide a Igor que lo haga» | coste/herramientas de Igor vs MCP simple | delegación siempre superior |

## Formato mínimo del informe al terminar
Resultado VERIFICADO/PROBADO/PARCIAL/BLOQUEADO; herramienta y operación observada; componente, versión, fecha y prueba; cambio real y su rollback; procesos/ventanas propios cerrados; coste adicional y cuota si aplica; Bibliotecario revisión releída; siguiente paso solo si sigue pendiente. No describir trabajo en segundo plano sin tarea creada realmente.

## Reglas de operación
No confirmar prematuramente; no repetir la pregunta ya respondida; no usar herramientas facturables sin presupuesto; no exportar secretos; no cambiar configuración de seguridad para sortear un error; no dejar residuos de pruebas; no duplicar servicios, tareas ni repositorios; no sustituir el código real por un plan de implementación.
