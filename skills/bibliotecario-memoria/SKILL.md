---
name: bibliotecario-memoria
description: Recupera trabajos y registra hitos autorizados en SQLite de Debian por el acceso realmente disponible, priorizando Control Debian cuando exponga la operación.
version: 0.3.6
---
# Bibliotecario — memoria y documentación

**Ejecución en Debian:** Python estándar + SQLite, sin API de pago. Primero comprobar las herramientas realmente expuestas por el chat. El puente privado `stdio-v83` de Control Debian anuncia 43 herramientas; entre ellas `debian_bibliotecario_buscar`, `debian_bibliotecario_resumen` y `debian_bibliotecario_registrar`. Su disponibilidad en una conversación nueva y la operación de registro deben probarse realmente. Si no aparecen, utilizar un canal alternativo autorizado sin simular acceso. GitHub→Issues→runner sigue como alternativa aprobada, con alcance restringido; Remote Desktop Commander queda para excepciones justificadas, solo en Debian. Nunca mezclar expedientes ni exponer credenciales.

## Protocolo exigible de registro verificado y continuación (01/11/2026)

1. **Identificar, no adivinar:** si están disponibles, ejecutar `debian_bibliotecario_buscar({title})`; contrastar título exacto y contexto, usar su ID de trabajo devuelto. A continuación `debian_bibliotecario_resumen({work})` para recuperar la revisión y los pendientes. No copiar identificadores reales a skills públicas.
2. **Decidir el hito:** registrar al completar una fase sustancial, al cambiar de fase y antes de cerrar una tarea duradera. Evitar duplicados, secretos y registros vacíos. Para habilidades y herramientas, cumplir la autorización previa específica para catalogación y resguardo; una autorización expresa de lote ya concedida no debe repetirse.
3. **Escribir con confirmación:** `debian_bibliotecario_registrar({work,operation_id,label,entries})`, con ID de operación estable e idempotente y tipos permitidos `decision|constraint|verified_result|next_action|note`. Exigir `status=saved` o `duplicate`, `revision` entero y `readback_confirmed=true`. Si la herramienta no devuelve estas pruebas, consultar nuevamente el resumen y confirmar que la revisión incorpora el resultado; si sigue dudoso, marcar `REGISTRO_NO_VERIFICADO`.
4. **Continuidad de la tarea:** el registro no sustituye completar fases pendientes en el mismo turno. Solo interrumpir cuando no quede trabajo autorizado y viable, haya impedimento técnico real o sea indispensable la intervención humana. Si el turno finaliza con trabajo pendiente, registrar su estado y siguiente acción cuando sea posible, sin prometer trabajo autónomo futuro.
5. **Diagnóstico sin fingir:** una skill no ejecuta hooks por sí sola y los conectores pueden no estar instalados en otro chat o en Free. Diferenciar herramienta anunciada, herramienta cargada, escritura real y lectura posterior. Si falta acceso, no atribuir al Bibliotecario un guardado que solo consta en la conversación.

**Control de calidad en proyectos con ejecutor:** cuando el ejecutor emita eventos identificables, comparar cada hito sustancial con la revisión y el identificador de operación en SQLite; reportar pérdidas, conflictos y demoras. Esta comparación no rastrea automáticamente todas las conversaciones ni instala servicios de vigilancia.

## Comportamiento al recuperar
1. Identifica el tema real de la conversación, sin suponer ningún proyecto preexistente. Busca con `{"action":"find","title":"TÍTULO"}` mediante `interfaz_chat.py` y comprueba el **título de cada coincidencia**: una mención incidental a un proyecto en otro trabajo no significa que ambos sean el mismo.
2. Si ya existe el trabajo adecuado, reutiliza su ID. Si no existe, consulta el protocolo local y, cuando haya un hito real que guardar, crea el trabajo para **cualquier proyecto** con `python3 /home/labgestor/bibliotecario-piloto/bibliotecario.py create "TÍTULO"`. Utiliza el ID que devuelva. Evita duplicados comprobando primero el catálogo real.
3. No crees registros prefabricados para una prueba de activación autónoma, no uses IDs fijos de ejemplo ni metas un proyecto en el trabajo de desarrollo del Bibliotecario por una simple coincidencia de palabras.
4. Recupera con `{"action":"brief","work":"ID_REAL"}` o `resume` de `/home/labgestor/bibliotecario-piloto/interfaz_chat.py` (petición JSON por stdin).
5. Reutiliza documentos y avances ya registrados sin afirmar que se han comprobado pasos que solo figuran como pendientes.

## Excepción: autorización previa para resguardo de habilidades y herramientas (29/10/2026)
La recuperación y lectura del Bibliotecario siguen permitidas. **Cuando el hito, documento, checkpoint, inventario o copia trate de habilidades o herramientas**, la detección de su importancia es proactiva, pero **se debe preguntar antes de crear el trabajo, guardar un documento, registrar `record_and_brief`, hacer backup o publicar**. Presentar qué se guardaría, dónde y sus costes/cuotas; pedir una autorización expresa específica. La autorización para desarrollar una habilidad o herramienta no sirve automáticamente para resguardarla o catalogarla. Si ese resguardo concreto ya fue solicitado explícitamente por el usuario, no volver a preguntar. Con aprobación, registrar y verificar en el mismo flujo. Si no la hay, informar en el chat `RESGUARDO_PENDIENTE_AUTORIZACION` sin escribirlo en SQLite ni crear archivos, y continuar el resto del trabajo permitido.

**Esta excepción se aplica solo a la catalogación y el resguardo de habilidades y herramientas.** Para otros proyectos e hitos conserva el comportamiento anterior, sujeto a las demás autorizaciones de seguridad. Seguir [protocolo de autorización previa](../inventariar-skills/references/autorizacion_catalogacion_y_resguardo.md).

## Guardado proactivo: dos capas complementarias
- **Documentos:** cuando produzcas un informe, script o material importante, guárdalo en la carpeta del proyecto en Debian y verifica que existe y se puede leer. El Observador indexa cambios de archivos, pero NO crea checkpoints por sí solo.
- **Hitos estructurados:** al completar una fase sustancial, antes de cambiar de tema o al cerrar una respuesta que incluya decisiones importantes, registra un hito **sin esperar una orden específica del usuario**. Incluye la decisión, resultado comprobado, error o próxima acción y la ruta precisa de los documentos relacionados, si existen. No registres cada saludo ni dupliques hitos equivalentes.

Ejemplo (sustituir ID, textos y rutas por datos reales):
`{"action":"record_and_brief","work":"ID_REAL","operation_id":"id-estable-para-este-hito","label":"Fase de trabajo","entries":[{"kind":"verified_result","text":"Resultado comprobado; documento: /home/labgestor/proyectos/.../informe.md"},{"kind":"next_action","text":"Próxima comprobación pendiente"}]}`

El programa crea sesión y revisión atómicamente y devuelve `write.status` y `context.latest_revision`. Confirmar `saved` o `duplicate` y la revisión obtenida; `duplicate` solo es correcto para reintento idéntico con el mismo `operation_id`. Ante errores no afirmar que se ha guardado.

**Precauciones:** guardar solo hitos útiles, no conversaciones completas ni credenciales; verificar rutas antes de registrarlas; no borrar ni modificar proyectos ajenos. La habilidad es una directriz, no un hook de fin de turno: no puede asegurar activación en todos los mensajes ni guardar tras un cierre brusco. La selección espontánea y la ejecución de `record_and_brief` deben verificarse por separado.
## Motor semántico contextual (ChatGPT durante la conversación, Free/Plus)
ChatGPT actúa como intérprete de recuerdos al trabajar en un chat activo. No depende de APIs de pago, otro LLM ni de un proceso continuo. Aplicar a cualquier trabajo, no solo a un proyecto concreto.

1. Recupera el trabajo mediante la interfaz habitual y contrasta los checkpoints originales. Los resúmenes extractivos sirven de índice; la detección de coincidencias léxicas de contexto_relaciones.py solo genera candidatos.
2. Compara el significado del hito anterior y posterior: asunto exacto, condiciones de éxito, prueba real, alcance parcial y hechos pendientes. No equipares "se abrió manualmente" con "se abre automáticamente". Descarta relaciones sin contexto suficiente.
3. Clasifica como related, resolved, superseded, contradicts, still_open, unrelated o insufficient_evidence, expresando una justificación concreta, límites y referencias a ID de checkpoint, revisión y ordinal. Prioriza insufficient_evidence ante la duda.
4. Si procede registrar una hipótesis, ejecuta en Debian evaluacion_semantica.py: draft(work,(checkpoint_anterior,ordinal),(checkpoint_posterior,ordinal),relation,reason,uncertainties), verify y record. La salida es agent_hypothesis_unapproved y se guarda aparte. Los hashes comprueban citas, no demuestran la interpretación; reviewer=human no acredita identidad ni autoriza cambios.
5. En la respuesta diferencia: hecho corroborado, interpretación fundamentada e hipótesis. Solo registra verified_result en la memoria principal si el hecho se comprobó realmente. Nunca declares cerrada una tarea basándote en similitud superficial.
6. Conserva originales y procedencia, evita duplicados mediante claves estables. No borres, fusiones o sustituyas hitos automáticamente. Si falla la conexión, declara el límite en lugar de inventar verificaciones.

La skill orienta conductas, NO garantiza ejecución espontánea en cada turno, recuperación tras cierre abrupto ni funcionamiento cuando ChatGPT no está activo. Observador de Debian y auditoría horaria son procesos distintos y no generan inferencia. Coste adicional objetivo: 0 €.

## Continuidad de Control Debian y del puente alternativo (01/11/2026)
- Localizar primero los trabajos existentes por título exacto (homologación de Control Debian, Gestor de Skills y CDC). Recuperar identificadores reales del Bibliotecario local; nunca incluir IDs privados en skills públicas ni reutilizarlos como autorización.
- El canal cotidiano de archivos/GUI/terminal limitada y registro es ChatGPT → Control Debian → Secure MCP Tunnel → Debian, cuando las herramientas de Bibliotecario están efectivamente cargadas en el chat. GitHub→Issues/Actions→runner→CDC/ejecutor local sigue disponible como **alternativa de recuperación y mantenimiento**; no desinstalarlo ni deshabilitarlo por completar la vía directa.
- Conservar los originales del Bibliotecario, `operation_id` estable y comprobación de revisión; no leer credenciales ni usar GitHub para datos personales. No inferir que el canal MCP permite registrar memoria hasta probar una operación propia y autorizada.
- Evidencia y riesgos: consultar inventario fechado 01/11/2026 de `inventariar-skills`; presupuesto marginal 0 € y catalogación/resguardo solo tras permiso específico.
