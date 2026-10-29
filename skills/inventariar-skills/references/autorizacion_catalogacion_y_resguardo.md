# Autorización previa para catalogar y resguardar habilidades y herramientas
**Vigente desde el 29/10/2026.** Fuente canónica del Gestor de Skills. Este protocolo prevalece sobre instrucciones históricas de catalogación, memoria y publicación automática cuando traten de habilidades o herramientas.

## Cuándo activar la comprobación (sin reducir su frecuencia)
Comprobar la necesidad de catalogar o resguardar en **las mismas situaciones que antes**: instalación, creación, descubrimiento material, actualización, sustitución, retirada o prueba/validación importante de una habilidad, MCP, herramienta, integración, automatización, servicio, agente o procedimiento reutilizable; cierre de una fase que afecte al inventario o a su recuperación. También al detectar una discrepancia entre fuente, catálogo, resguardo y plugin distribuido. La detección y la propuesta son automáticas; **la ejecución persistente no lo es**.

## Puerta de autorización obligatoria
1. Identificar los elementos y los destinos existentes; comparar versiones y pruebas mediante lecturas sin cambios. Preparar mentalmente o en el chat la propuesta sin crear aún registros, copias ni artefactos persistentes.
2. **Antes de escribir** preguntar una vez, de forma breve y explícita: qué se va a catalogar, qué se va a respaldar, qué repositorio/archivo/Bibliotecario/plugin se alteraría y si hay costes/cuotas o datos confidenciales. Ofrecer aprobar el conjunto por una sola respuesta. La aprobación debe ser **previa, específica para catalogación y resguardo y limitada a esos destinos y alcance**.
3. No interpretar el permiso para ejecutar la tarea técnica como permiso para catalogar, respaldar o publicar su documentación. Un «sigue», una autorización genérica de acceso o una petición para implementar otra función no sustituyen la autorización concreta de este paso. **Excepción:** si el usuario ya solicita de manera expresa catalogar/respaldar esos elementos y destinos, esa petición cuenta como autorización de ese alcance y no se pregunta de nuevo. La petición de incorporar este propio protocolo autoriza su implantación inicial, sin otorgar permisos permanentes para futuros inventarios.
4. Tras la aprobación: catalogar y resguardar en la **misma ocasión en que antes se hacía automáticamente**, verificar los archivos y las copias, y, si se autorizó, sincronizar y publicar la versión del **mismo** complemento privado. No pedir confirmaciones adicionales para pasos ya incluidos en la autorización; sí detenerse antes de cualquier destino nuevo, cambio de permisos, difusión, coste o acción no prevista.
5. Si no hay respuesta, se deniega o se aplaza: **no crear, editar, registrar, copiar, subir, versionar ni publicar** los catálogos o respaldos afectados. Continuar las otras tareas autorizadas, explicar en el cierre `CATALOGACION_PENDIENTE_AUTORIZACION` y/o `RESGUARDO_PENDIENTE_AUTORIZACION`, con la propuesta sin registrar en el catálogo. No afirmar que una copia o actualización quedó realizada.
6. Si el trabajo técnico necesita necesariamente una copia de seguridad antes de un cambio irreversible, pedir la autorización de ese respaldo **antes de proceder con la operación irreversible**. Si se rechaza, detener esa operación peligrosa; no omitir la copia para continuar.
7. Registrar el permiso y su alcance **solo después de haber obtenido autorización para guardarlo**; citarlo en el informe del chat aunque aún no esté persistido. No guardar por anticipado un «pendiente» en SQLite, GitHub, la Librería, documentos o automatizaciones.

## Qué cubre «catalogar y resguardar»
- Crear o editar inventarios y catálogos de habilidades/herramientas en Debian, GitHub, Drive, Librería o archivos del proyecto.
- Copias de seguridad, snapshots, exportaciones, empaquetados, ZIP, hashes de respaldo y transferencia a otro destino.
- Registros estructurados de habilidades/herramientas en Bibliotecario, SQLite, notas persistentes y archivos de recuperación.
- Commits, sincronización y publicación cuyo objeto sea distribuir estos catálogos o sus respaldos (incluido Plugin Creator o marketplaces).
- No afecta a consultas de solo lectura, al análisis de necesidades ni a la ejecución de **otras tareas técnicas** autorizadas por separado. Si una publicación/versión es parte inseparable de un cambio de skill, detallar y solicitar la autorización explícita para ese lote.

## Ejemplo de pregunta, en una sola intervención
«He detectado que corresponde catalogar **[elementos]** y respaldar **[archivos/versiones]** en **[destinos]**. No supone un coste adicional / coste estimado **[importe y cuota]**. ¿Me autorizas a realizar **estos registros, copias y, si procede, su publicación** ahora?». Tras la respuesta afirmativa, ejecutar y verificar sin más interrupciones por ese mismo lote.

## Precedencia y límites
Esta norma sustituye cualquier frase histórica «sin segunda orden», «guardar automáticamente», «actualizar en la misma tarea sin pedir permiso» y «publicar por defecto» **solo en lo relativo a catalogación y resguardo de habilidades y herramientas**. Los procedimientos de seguridad, protección de secretos, consentimiento para pagos y controles propios de otras operaciones siguen plenamente vigentes. No crea una automatización en segundo plano.
