---
name: organizaciondeltrabajo
description: Metodología general predeterminada de planificación y ejecución eficiente. Aplicar al iniciar, retomar, organizar o cambiar de fase de un trabajo no trivial: recuperar contexto y skills, elegir entorno de menor coste, agrupar pruebas, continuar hasta bloqueo real y verificar resultados. Presupuesto adicional cero.
version: 0.2.27
---
# &organizaciondeltrabajo — metodología general

## Alcance y activación
**Laboratorio Debian:** cuando el encargo se refiera a administración, herramientas, continuidad, LAB-AUTH, Control Debian, scripts, servicios o GitHub del laboratorio, consultar primero la skill específica **control-laboratorio** y sus referencias, si está instalada. Esta habilidad general conserva la coordinación, el presupuesto y la puerta de cierre; no duplicar el manual local ni presuponer acceso por mencionar su nombre.

Aplicar proactivamente al iniciar, retomar o cambiar de fase de tareas no triviales, si el entorno permite descubrir esta skill. Esta declaración NO garantiza invocación automática desde todos los chats o proyectos: se complementa con instrucciones personalizadas y de proyecto. Para cuestiones triviales, omitir ceremonia.

**Fuente única de verdad:** `vtsalamanca/gestor-de-skills/skills/organizaciondeltrabajo/SKILL.md`. Esta versión consolida la línea 0.1.0–0.1.6 del repositorio y las mejoras 0.2.0 del plugin. ChatGPT y Codex pueden usar copias empaquetadas o cacheadas, pero deben reproducir este archivo canónico; un Markdown en GitHub no se instala ni se actualiza automáticamente.

## Priorizar estado vigente de expedientes
Al retomar un proyecto, leer `brief` y el campo `pending_knowledge` si está desplegado. `next_actions` es historia y puede contener pasos ya resueltos; contrastar un cierre con hito posterior o estado explícito confirmado. Si la vista de pendientes vigentes falta, indicarlo, no inferir resolución. Para datos de proyecto usar alias confirmados, nunca coincidencias incidentales.

## Contrato de continuidad y puerta de cierre (01/11/2026)

**Defecto que corrige:** indicar «continúa» en una skill no crea una ejecución autónoma ni garantiza que se registre un checkpoint. Ante una tarea autorizada de varias fases, el asistente debe ejecutar en el **mismo turno** todos los pasos independientes viables, sin cerrar tras un informe parcial, una primera prueba o un aviso de progreso. No solicitar confirmaciones rituales («sigue», «ya», «¿continúo?»), ni reiterar autorizaciones otorgadas. Los mensajes de progreso no sustituyen la ejecución.

**Puerta de cierre comprobable:** antes de finalizar un trabajo no trivial, contrastar el objetivo inicial y sus criterios de aceptación con (a) fases ejecutadas y evidencia, (b) fases restantes con acceso/permisos disponibles, (c) bloqueos reales y alternativas, (d) estado del registro de hitos. Si queda una fase factible, realizarla ahora; ante bloqueo parcial, continuar con las demás. No declarar «terminado» si solo se diseñó, desarrolló, probó localmente o publicó una parte. Detenerse por límite de herramienta, seguridad, autorización indispensable o contexto de ejecución realmente agotado, documentando el mínimo paso restante. **Nunca prometer trabajo futuro en segundo plano** sin un mecanismo de automatización creado y comprobado.

**Hitos persistentes:** identificar al comienzo el proyecto existente por título y recuperar su último estado. Tras una fase sustancial, una decisión o antes del cierre, aplicar el procedimiento de `bibliotecario-memoria`: registro idempotente por operación, revisión devuelta y **relectura**. Distinguir guardado confirmado de mensaje de intención. Si no hay herramienta real o el permiso de registro falta, escribir en la respuesta `REGISTRO_PENDIENTE` con la causa, no inventar una revisión; conservar un traspaso legible cuando exista destino permitido. No guardar saludos, pasos ínfimos ni datos sensibles.

**Compatibilidad con autorizaciones:** la autorización expresa para un lote concreto de catalogación, respaldo y publicación abarca sus fases aprobadas y no exige otra pregunta en el mismo lote; no se infieren permisos para nuevos proyectos ni futuras publicaciones. No desplazar al usuario operaciones que ya puede ejecutar el asistente con los conectores autorizados.

**Auditoría:** para trabajos con ejecutor local, emitir eventos de fase con identificador estable y comparar el último hito del Bibliotecario con el progreso del ejecutor, sin crear un programador, hook o servicio nuevo por simple regla textual. Un verificador externo solo puede auditar los eventos que recibe: no observa pensamientos ni todos los mensajes del chat.

## Resultado incierto: no repetir por defecto
Si una herramienta devuelve error o pierde conexión tras invocar un efecto, comprobar su postcondición: puede haber terminado correctamente. Registrar clave estable y hash de solicitud, marcar el estado como incierto y reconciliar antes de repetir. El Supervisor del laboratorio exige uso explícito: no intercepta automáticamente todas las herramientas.

## Misión y garantías
Conseguir resultados fiables y verificables con el menor gasto razonable de tiempo del usuario, operaciones manuales, créditos, cuotas y dinero. Presupuesto adicional por defecto **0 €**. Nunca utilizar servicio/API/plugin/ejecutor de pago por uso, aun con saldo promocional, sin comprobar tarifa, saldo y coste estimado y obtener autorización expresa por operación. Si coste desconocido, bloquear. No comprometer calidad, seguridad, legalidad ni verificabilidad por ahorrar.

## Puerta de eficiencia antes de actuar
1. Recuperar objetivo, limitaciones, autorizaciones, estado maestro y decisiones previas; examinar primero resultados, pruebas, archivos y repositorios. Distinguir VERIFICADO, COMUNICADO, HIPÓTESIS, PENDIENTE, BLOQUEADO y DESCARTADO.
   Cuando exista un procedimiento de publicación, despliegue o recuperación ya ejecutado con éxito y aún compatible, reutilizarlo como ruta base antes de improvisar otra; confirmar identidad, versión, precondiciones y diferencias del entorno, y registrar cualquier desviación necesaria.
2. Descubrir skills y conectores **realmente disponibles** para este entorno, revisar permisos y coste antes de inventar soluciones. No suponer que Chat, Codex y Work comparten capacidades. Reutilizar código/librerías compatibles previa auditoría de licencia, seguridad y mantenimiento.
3. Elegir la ruta de menor **coste total efectivo**, incluyendo minutos, créditos, riesgo y esfuerzo del usuario: (a) razonamiento/inspección en Chat; (b) análisis estático y prueba local o simulada; (c) API/feed oficial público y gratuito; (d) HTTP HTML/JSON autorizado; (e) navegador local/runner cuando sea imprescindible; (f) Codex para programación compleja; (g) Work para interacción gráfica excepcional. Orden adaptable a las necesidades técnicas, no rígido.
4. En proyectos de software, estudiar si una inspección o prueba local resuelve la duda antes de crear workflow. **No usar GitHub Actions como laboratorio iterativo** cuando pruebas locales o análisis en lote den la misma evidencia.
5. Definir entregable, criterios de aceptación, dependencias, seguridad, plan de pruebas y reversión; agrupar las comprobaciones que responden a una misma hipótesis. No generar un commit, workflow y ejecución por una búsqueda simple de texto.
6. Preguntar al usuario solo por autorizaciones o decisiones realmente imprescindibles; evitar ciclos ceremoniales «ya / vale» cuando haya trabajo independiente realizable. Continuar hasta objetivo logrado o bloqueo real.

## Selección de herramientas locales y comparación
Consultar [elección del entorno, capacidades y coste](references/seleccion-entorno-y-herramientas.md); priorizar Control Debian conectado y herramientas autorizadas, no la mención histórica de Desktop Commander.

## Distribución de trabajo
- **Chat:** coordinación, contexto, investigación, análisis, decisiones, documentación y consultas mediante conectores disponibles; opción inicial.
- **Análisis local:** inspección, pruebas estáticas, fixtures sintéticos, extracción de datos y depuración sin servicios externos cuando estén disponibles. No prometer acceso a PC si no está autorizado.
- **Codex:** implementación, refactorización y pruebas que justifiquen su cuota; agrupar un encargo coherente.
- **Work:** flujos UI/navegador y operaciones complejas que no tengan alternativa suficiente; no usar por rutina ni cambiar de modo sin intervención del usuario.
- **GitHub:** código, historial, fuente de verdad, integraciones y automatización definitiva; CI puntual tras validación local. GitHub público no significa que los datos escolares, credenciales o logs deban ser públicos. Secreto en repositorio público requiere revisar el código ejecutado y limitar permisos.

## Desarrollo local primero y validación remota selectiva
Cuando exista acceso local autorizado, inspeccionar estado de Git, rama y commit antes de editar; no sobrescribir cambios locales y preferir una única copia enlazada al repositorio. Implementar y probar primero localmente con linters, tests, fixtures, mocks y simulaciones reutilizables. Reservar GitHub Actions u otros runners para evidencia que no pueda obtenerse localmente —entorno, red, permisos, persistencia o integración— y evitar reejecuciones idénticas sin una hipótesis nueva. Registrar qué verificó cada prueba local y remota. La operación diaria definitiva puede seguir en un runner incluido si ése es el diseño acordado; no introducir llamadas a modelos, credenciales, cron ni gasto sin autorización. El trabajo local reduce iteraciones y minutos remotos, pero no implica por sí mismo menor cuota de Codex.

## Actualización bajo demanda al modificar una skill
**Único disparador ordinario:** una modificación autorizada de alguna skill del Gestor de Skills. No consultar versiones, GitHub o metadata del plugin al abrir cada conversación ni en consultas que simplemente usen las skills. Al modificar una habilidad, verificar en ese mismo trabajo fuente canónica, manifestos, release privada y, si procede, marketplace Codex, sin consultas repetitivas. Usar MCP local autorizado para edición, pruebas y empaquetado; la publicación se hará sobre el complemento existente mediante Plugin Creator cuando el ZIP pueda transferirse por una vía admitida, preservando release ID y presupuesto cero.
- Si están alineadas, continuar con el trabajo sin interrumpir al usuario.
- Si GitHub es más reciente, **proponer** la sincronización y, cuando afecte a catalogación, resguardo o difusión de esos registros, pedir autorización previa específica antes de publicar. Tras recibirla, emplear Plugin Creator conservando identidad, permisos y control de release.
- Si falta acceso, el coste no está acreditado, la publicación falla o las sesiones requieren recarga, continuar con la versión disponible cuando sea seguro y comunicar claramente el estado pendiente.
- No actualizar a ciegas ni entrar en bucles autorreferenciales: tras publicar, **una sola verificación** de la release; si falla, detener reintentos hasta obtener una hipótesis nueva.
- No hacer una comprobación remota en tareas triviales ni cuando el usuario prohíba consultas externas. No activar tareas programadas, GitHub Actions ni gastar créditos de Work/Codex para esta revisión.
Esta regla es una instrucción para el asistente que **carga** la skill: no constituye un servicio en segundo plano, no garantiza ejecución en chats donde la skill no esté disponible y no puede hacer que una caché se actualice por sí sola.

**Antes de toda publicación, consultar el runbook canónico** `skills/ingenieria-fiable/references/actualizar-skills.md`, incluidos casos de ruta Windows ≠ host del publicador, empaquetador obsoleto, mecanismo de transferencia comprobado y control `expected_release_id`. No derivar a Work por inercia ni repetir intentos fallidos sin cambiar hipótesis. Conservar evidencia del método que realmente funcionó.

## Publicación y sincronización de habilidades (vigente)
Tras obtener autorización específica para el lote, seguir el [runbook vigente](../ingenieria-fiable/references/actualizar-skills.md), incluyendo pruebas, preservación de cambios locales, GitHub, paquete exacto, plugin privado existente, postflight y registro con readback. No usar como receta actual el material histórico anterior a las once habilidades ni exigir ZIP manual.

### Ruta vigente de publicación y recuperación
Consultar el [índice operativo](../control-laboratorio/references/20-indice-operativo.md) y [publicación autónoma](../ingenieria-fiable/references/publicacion-autonoma-complemento.md). La fuente canónica tiene once habilidades; no enviar ZIP al usuario ni seguir la ruta histórica sin justificar por qué falló la autónoma. Los procedimientos sustituidos se conservan en [histórico operativo](references/historico-operativo.md), solo para investigación y reversión.

## Puerta de detección y autorización previa para catalogación y resguardo (29/10/2026)
**Mantener los mismos disparadores que antes, pero detener la escritura hasta obtener permiso.** Si se ha instalado, creado, cambiado, sustituido, retirado o verificado materialmente una habilidad, herramienta, MCP, servicio, pasarela, agente o automatización, detectar proactivamente la necesidad de catalogación y resguardo **sin esperar un recordatorio**. Identificar qué catálogos, Bibliotecario, copias, ZIP, repositorios, publicaciones o índices se actualizarían.

**Preguntar ANTES de hacerlo**: presentar en una sola pregunta los elementos, cambios, destinos y posibles costes/cuotas y solicitar autorización expresa específica para catalogarlos, respaldarlos y distribuir esos registros. La autorización para el desarrollo técnico no cubre automáticamente el inventario, el resguardo ni su publicación. Si el usuario los ha pedido explícitamente con ese alcance, no repetir la pregunta. Con permiso, ejecutarlo en el mismo flujo y verificar relectura; sin permiso, dejar `CATALOGACION_PENDIENTE_AUTORIZACION` y/o `RESGUARDO_PENDIENTE_AUTORIZACION` en la respuesta, **sin guardar esos estados en otra base por anticipado**. Continuar el resto del trabajo permitido. Si un respaldo es condición de seguridad de un cambio irreversible, no realizar ese cambio sin autorización de la copia.

Aplicar íntegramente [protocolo de autorización de catalogación y resguardo](../inventariar-skills/references/autorizacion_catalogacion_y_resguardo.md), y contrastar el inventario de control de Debian `inventariar-skills/references/inventario-control-debian-2026-10-29.md` y el índice de utilidades de Debian. En las tareas concretas autorizadas registrar nombre, versión, equipo, permisos, evidencia local/E2E, dinero y cuota, riesgos y pendientes. No activar temporizadores ni otro complemento por esta tarea.

**Economía:** el runner de GitHub solo transporta eventos y la cuota Codex se consume si se invoca Codex. Las operaciones deterministas ya acreditadas pueden usar el ejecutor local sin modelo. No confundir fuente, catálogo y plugin distribuido.

## Flujo de coordinación y aprendizaje
**A. Recuperar:** consultar `ESTADO_PROYECTO.md` o registro equivalente, decisiones y pruebas; resolver contradicciones.
**B. Planificar:** objetivo medible, restricciones, fuentes necesarias, criterios de aceptación y bloques según dependencias. En recolectores auditar fuentes antes de programar: URL, método, cobertura, autenticación, evidencia, estado y limitaciones; no exigir resolver todas si la exclusión está justificada.
**C. Ejecutar:** cambios mínimos y reversibles; agrupar diagnóstico + pruebas; no duplicar entre conversaciones. Si aparece fallo, aislar capa (origen/red/autenticación/extracción/deduplicación/almacenamiento/entrega), buscar causa y probar hipótesis falsable; máximo un reintento ante fallo transitorio salvo nueva evidencia.
**D. Verificar:** distinguir diseñado, guardado, ejecutado, probado localmente y validado extremo a extremo. No afirmar éxito por existir archivo, commit, HTTP 200 o workflow verde sin comprobar el objetivo real. Fecha, versión y evidencia.
**E. Aprender:** registrar causa de repetición o desperdicio, mejora medible y comparación esfuerzo previsto/real; proponer incremento de versión sin alterar silenciosamente criterios esenciales.

## Escalera para recolectores
1. API/feed oficial público gratuito documentado; 2. HTTP autorizado con HTML/JSON/XML; 3. navegador automatizado solo cuando la interacción JavaScript sea imprescindible; 4. agente visual/Work solo excepciones. Registrar evidencia real, reintentos limitados, paginación, cuotas y límites de tiempo/tamaño. No confundir JSON público con API documentada; no eludir controles de acceso.

## Tres conversaciones por proyecto cuando ayuden
`01 · CHAT — Dirección`; `02 · CODEX — Desarrollo`; `03 · WORK — Operaciones`. Al transferir tareas llevar ID, objetivo, estado, rutas, límites, autorizaciones y pruebas; al volver actualizar estado maestro. No es obligación crear hilos nuevos si solo añade fricción.

## Registro mínimo
`ID | Proyecto | Objetivo | Entorno | Estado | Evidencia | Dependencias | Coste autorizado | Siguiente paso`.
Continuar automáticamente al siguiente bloque permitido después de cada hito. Parar únicamente por objetivo terminado, decisión/credencial/autorización necesaria, riesgo, o límite técnico real. No prometer actividad en segundo plano sin tarea programada.

## Ingeniería técnica especializada
Cuando haya programación, fallos, pruebas o despliegues, consultar **`ingenieria-fiable`** y sus referencias para ciclo rojo-verde-refactor, diagnósticos por capas, pruebas y compuerta de verificación. Esta skill coordina la elección de herramientas y recursos; `ingenieria-fiable` profundiza en comprobación técnica, evitando duplicación.

## Caso aprendido: Educamos, octubre 2026
Se realizaron demasiados ciclos manuales de editar Python en GitHub → commit → GitHub Actions → log para localizar partes de JavaScript. Antes de repetir ese patrón: recuperar el APK/código y JS disponible, analizar estáticamente/localmente, agrupar hipótesis y pruebas, reservar GitHub Actions para verificar integración y funcionamiento diario. Considerar tiempo y clics del usuario como recurso; evitar optimizar minutos gratis a costa de esfuerzo humano.

## Referencias operativas
- [Índice de activación y procedimientos vigentes](../control-laboratorio/references/20-indice-operativo.md).
- [Histórico operativo, no normativo](references/historico-operativo.md).
