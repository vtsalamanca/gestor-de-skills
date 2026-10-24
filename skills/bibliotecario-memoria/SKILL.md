---
name: bibliotecario-memoria
description: Recupera trabajos y registra proactivamente decisiones, pruebas y documentos importantes en SQLite de Debian mediante Remote Desktop Commander.
version: 0.3.1
---
# Bibliotecario — memoria y documentación

**Ejecución compatible con Free y Plus cuando Remote Desktop Commander esté disponible:** Python estándar + SQLite en `debian-laboratorio`. No requiere Codex, Work, API de pago ni GitHub para guardar.

## Comportamiento al recuperar
1. Identifica el trabajo: busca por título en el Bibliotecario, nunca presupongas que el ID de otro proyecto sirve. Si falta, consulta el protocolo local antes de crear nada.
2. Recupera con `{"action":"brief","work":"ID_REAL"}` o `resume` de `/home/labgestor/bibliotecario-piloto/interfaz_chat.py` (petición JSON por stdin).
3. Reutiliza documentos y avances ya registrados sin afirmar que se han comprobado pasos que solo figuran como pendientes.

## Guardado proactivo: dos capas complementarias
- **Documentos:** cuando produzcas un informe, script o material importante, guárdalo en la carpeta del proyecto en Debian y verifica que existe y se puede leer. El Observador indexa cambios de archivos, pero NO crea checkpoints por sí solo.
- **Hitos estructurados:** al completar una fase sustancial, antes de cambiar de tema o al cerrar una respuesta que incluya decisiones importantes, registra un hito **sin esperar una orden específica del usuario**. Incluye la decisión, resultado comprobado, error o próxima acción y la ruta precisa de los documentos relacionados, si existen. No registres cada saludo ni dupliques hitos equivalentes.

Ejemplo (sustituir ID, textos y rutas por datos reales):
`{"action":"record_and_brief","work":"ID_REAL","operation_id":"id-estable-para-este-hito","label":"Fase de trabajo","entries":[{"kind":"verified_result","text":"Resultado comprobado; documento: /home/labgestor/proyectos/.../informe.md"},{"kind":"next_action","text":"Próxima comprobación pendiente"}]}`

El programa crea sesión y revisión atómicamente y devuelve `write.status` y `context.latest_revision`. Confirmar `saved` o `duplicate` y la revisión obtenida; `duplicate` solo es correcto para reintento idéntico con el mismo `operation_id`. Ante errores no afirmar que se ha guardado.

**Precauciones:** guardar solo hitos útiles, no conversaciones completas ni credenciales; verificar rutas antes de registrarlas; no borrar ni modificar proyectos ajenos. La habilidad es una directriz, no un hook de fin de turno: no puede asegurar activación en todos los mensajes ni guardar tras un cierre brusco. La selección espontánea y la ejecución de `record_and_brief` deben verificarse por separado.
