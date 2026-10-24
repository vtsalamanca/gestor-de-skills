---
name: bibliotecario-memoria
description: Recupera trabajos y registra proactivamente decisiones, pruebas y documentos importantes en SQLite de Debian mediante Remote Desktop Commander.
version: 0.3.3
---
# Bibliotecario — memoria y documentación

**Ejecución compatible con Free y Plus cuando Remote Desktop Commander esté disponible:** Python estándar + SQLite en `debian-laboratorio`. No requiere Codex, Work, API de pago ni GitHub para guardar.

## Comportamiento al recuperar
1. Identifica el tema real de la conversación, sin suponer ningún proyecto preexistente. Busca con `{"action":"find","title":"TÍTULO"}` mediante `interfaz_chat.py` y comprueba el **título de cada coincidencia**: una mención incidental a un proyecto en otro trabajo no significa que ambos sean el mismo.
2. Si ya existe el trabajo adecuado, reutiliza su ID. Si no existe, consulta el protocolo local y, cuando haya un hito real que guardar, crea el trabajo para **cualquier proyecto** con `python3 /home/labgestor/bibliotecario-piloto/bibliotecario.py create "TÍTULO"`. Utiliza el ID que devuelva. Evita duplicados comprobando primero el catálogo real.
3. No crees registros prefabricados para una prueba de activación autónoma, no uses IDs fijos de ejemplo ni metas un proyecto en el trabajo de desarrollo del Bibliotecario por una simple coincidencia de palabras.
4. Recupera con `{"action":"brief","work":"ID_REAL"}` o `resume` de `/home/labgestor/bibliotecario-piloto/interfaz_chat.py` (petición JSON por stdin).
5. Reutiliza documentos y avances ya registrados sin afirmar que se han comprobado pasos que solo figuran como pendientes.

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
