---
name: organizaciondeltrabajo
description: Metodología general predeterminada de planificación y ejecución eficiente. Aplicar al iniciar, retomar, organizar o cambiar de fase de un trabajo no trivial: recuperar contexto y skills, elegir entorno de menor coste, agrupar pruebas, continuar hasta bloqueo real y verificar resultados. Presupuesto adicional cero.
version: 0.2.20
---
# &organizaciondeltrabajo — metodología general

## Alcance y activación
Aplicar proactivamente al iniciar, retomar o cambiar de fase de tareas no triviales, si el entorno permite descubrir esta skill. Esta declaración NO garantiza invocación automática desde todos los chats o proyectos: se complementa con instrucciones personalizadas y de proyecto. Para cuestiones triviales, omitir ceremonia.

**Fuente única de verdad:** `vtsalamanca/gestor-de-skills/skills/organizaciondeltrabajo/SKILL.md`. Esta versión consolida la línea 0.1.0–0.1.6 del repositorio y las mejoras 0.2.0 del plugin. ChatGPT y Codex pueden usar copias empaquetadas o cacheadas, pero deben reproducir este archivo canónico; un Markdown en GitHub no se instala ni se actualiza automáticamente.

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
- Si GitHub es más reciente, intentar en el mismo flujo la publicación bajo demanda mediante la herramienta oficial Plugin Creator, conservando identidad, permisos y control de release; pedir una intervención únicamente si es realmente imprescindible.
- Si falta acceso, el coste no está acreditado, la publicación falla o las sesiones requieren recarga, continuar con la versión disponible cuando sea seguro y comunicar claramente el estado pendiente.
- No actualizar a ciegas ni entrar en bucles autorreferenciales: tras publicar, **una sola verificación** de la release; si falla, detener reintentos hasta obtener una hipótesis nueva.
- No hacer una comprobación remota en tareas triviales ni cuando el usuario prohíba consultas externas. No activar tareas programadas, GitHub Actions ni gastar créditos de Work/Codex para esta revisión.
Esta regla es una instrucción para el asistente que **carga** la skill: no constituye un servicio en segundo plano, no garantiza ejecución en chats donde la skill no esté disponible y no puede hacer que una caché se actualice por sí sola.

**Antes de toda publicación, consultar el runbook canónico** `skills/ingenieria-fiable/references/actualizar-skills.md`, incluidos casos de ruta Windows ≠ host del publicador, empaquetador obsoleto, mecanismo de transferencia comprobado y control `expected_release_id`. No derivar a Work por inercia ni repetir intentos fallidos sin cambiar hipótesis. Conservar evidencia del método que realmente funcionó.

## Publicación y sincronización obligatoria de skills
Tras cualquier modificación autorizada de una skill canónica en `vtsalamanca/gestor-de-skills`, incluir en el mismo trabajo la distribución y verificación sin necesitar una segunda solicitud:
1. Comparar `main` con la release del plugin privado ChatGPT/Work y con el marketplace de Codex; identificar diferencias por contenido, no solo por número de versión.
2. Validar estructura, seguridad, cambios, reversibilidad y coste adicional (por defecto 0 €). Incrementar versiones de skill y paquete de forma coherente cuando corresponda.
3. Si las herramientas y permisos disponibles lo permiten, preparar el paquete desde GitHub y actualizar el **mismo plugin privado**, conservando su identidad, con control de concurrencia por ID de release; nunca afirmar que un commit de GitHub actualiza por sí solo ChatGPT/Work.
4. Verificar publicación y contenido de los archivos distribuidos; cuando sea posible comprobar la carga en una sesión nueva y el marketplace Codex. Distinguir `FUENTE_ACTUALIZADA`, `PLUGIN_PUBLICADO`, `CARGA_VERIFICADA` y `PENDIENTE`.
5. Si publicar o comprobar exige otra herramienta, permiso, tarifa desconocida o servicio de pago, no ejecutarlo; comunicar el bloqueo concreto, el siguiente paso mínimo y la versión que continúa activa. Nunca marcar la sincronización como completada sin evidencia.
No prometer ejecución desatendida ni actualización instantánea de sesiones/cache. Esta regla aplica a cualquier skill del repositorio y complementa las instrucciones generales del usuario.

### Publicacion de plugin sin transferir ZIP desde Windows
Ante un fallo al entregar a Plugin Creator un ZIP ubicado en Windows, recuperar el procedimiento probado el 20 de octubre de 2026 (release 0.4.12). No pedir adjuntos al usuario ni recrear pasarelas descartadas.
1. Leer el README, scripts/package_plugin.py y pruebas del repositorio canonico. Fijar commit SHA exacto, version y listado completo de archivos. Recuperar archivos del repositorio privado mediante el conector GitHub autorizado; no depender de un clon anonimo.
2. Reconstruir el ZIP en el entorno de ejecucion accesible al publicador, con .codex-plugin/plugin.json, README.md y skills/ completas (ocho habilidades y referencias). Validar estructura, manifiestos y hashes SHA-256 de cada archivo. No usar una ruta Windows como si fuera local al publicador.
3. Consultar el complemento privado existente mediante Plugin Creator; conservar plugin_id y current_release_id. Llamar update_plugin con la ruta absoluta del ZIP accesible al publicador y expected_release_id; no crear otro plugin y preservar la release anterior.
4. Releer la release publicada y sus archivos, comparar version, ocho habilidades y hashes. Registrar por separado FUENTE_ACTUALIZADA, PAQUETE_VALIDADO, PLUGIN_PUBLICADO, CARGA_VERIFICADA o PENDIENTE.
5. Si no existe capacidad real de crear el ZIP en el host del publicador, diagnosticar esa limitacion especifica y no inventar exito, rutas ni transferencias. No repetir intentos identicos sin una nueva hipotesis.
Presupuesto adicional cero; sin credenciales, servicios de pago ni modificaciones de la pasarela descartada. La ruta funciono antes, pero se debe verificar su disponibilidad en la sesion actual.
### Recuperación de la actualización local del marketplace de Codex
Cuando la fuente y el plugin privado estén publicados pero Codex mantenga una versión anterior, reutilizar este procedimiento antes de improvisar reinstalaciones:
1. Consultar primero, sin modificar, `codex plugin marketplace list` y `codex plugin list --marketplace <nombre> --available --json`; anotar fuente, versión, estado instalado/habilitado y ruta activa.
2. Solicitar únicamente permisos de escritura sobre las rutas locales que el actualizador necesita —normalmente `.codex/.tmp`, el caché de ese marketplace y temporales de `.codex`— y comprobar el acceso con un archivo sonda que se elimine inmediatamente. Un permiso concedido no sustituye esta prueba real.
3. Si Git falla en Windows con `schannel: AcquireCredentialsHandle failed` o `SEC_E_NO_CREDENTIALS`, no repetir la misma orden. Para esa invocación, y sin alterar la configuración global, establecer `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=http.sslBackend` y `GIT_CONFIG_VALUE_0=openssl`; después ejecutar `codex plugin marketplace upgrade <nombre> --json`.
4. Releer inmediatamente el marketplace y la lista de plugins. Si ya muestran la versión objetivo como instalada y habilitada y existe su directorio de caché, **no ejecutar `plugin add`**: el `marketplace upgrade` puede haber actualizado tanto la instantánea como el caché instalado. Instalar de nuevo solo si la verificación demuestra que sigue ausente o desactualizado.
5. Verificar el commit de la instantánea, versión de marketplace y manifiesto, ruta de caché, número/nombres de skills y el contenido afectado. Una advertencia auxiliar —por ejemplo, limpieza fallida de temporales `arg0`— no invalida por sí sola una actualización cuyo resultado estructurado no contiene errores y cuya versión/contenido se han releído correctamente.
6. Si una operación posterior falla pero la verificación ya acredita el objetivo, registrar ese intento como innecesario y detenerse; no convertirlo en falso pendiente. Las sesiones abiertas pueden conservar instrucciones anteriores hasta iniciar una conversación nueva.

Este procedimiento no autoriza permisos amplios permanentes, cambios globales de Git, borrado manual de cachés ni crear otro marketplace o plugin. Ante otro síntoma, volver al diagnóstico por capas y permitir como máximo un reintento por hipótesis nueva.

## Puerta de catalogación obligatoria al cerrar una implementación (29/10/2026)
**No esperar a que el usuario lo recuerde.** Si esta tarea ha instalado, actualizado, desactivado o validado materialmente una herramienta, MCP, skill, servicio, pasarela, modelo ejecutor o automatización, comprobar antes de concluir si cambiaron el inventario de habilidades o el catálogo de utilidades del laboratorio. Actualizar ambos donde corresponda **en el mismo trabajo**: nombre, versión, ubicación, permiso, equipo, comprobación local/E2E, coste monetario **y cuota consumida**, seguridad y pendientes; releer el resultado y enlazarlo desde los índices habituales. La catalogación no requiere abrir otro chat, crear otra skill ni activar cron/Actions. Para el control de Debian consultar `inventariar-skills/references/inventario-control-debian-2026-10-29.md` y el índice de `/home/labgestor/utilidades/`.

**Economía del nuevo puente:** GitHub Actions con runner autohospedado es transporte de eventos, no sustituto de la cuota Codex. Para consultas deterministas (lista de aplicaciones/páginas) considerar ejecutar MCP directamente sin modelo **solo después de implementarlo y probarlo**; no afirmar que ya existe. Conserva versiones de catálogo, fuentes y plugin separadas; una modificación local de SKILL.md no actualiza por sí sola el plugin de ChatGPT.

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

## Historial
- 0.2.20 (29 oct 2026): obligación de actualizar los catálogos de habilidades y herramientas en el mismo cierre de cada implementación material; registro diferenciado de cuota y coste monetario, pruebas E2E y límites de los MCP/CDC.
- 0.2.7 (19 oct 2026): recuperación verificable de actualizaciones locales de marketplaces Codex: permisos específicos, fallback OpenSSL para Schannel y parada cuando `marketplace upgrade` ya actualizó instalación y caché.
- 0.2.6 (19 oct 2026): reutilización prioritaria de procedimientos publicados ya verificados, con comprobación de identidad, versión, precondiciones y diferencias antes de repetirlos.
- 0.2.5 (19 oct 2026): puerta reforzada para detectar alternativas disponibles antes de programar o repetir diagnósticos; integración metodológica con acceso_webs.
- 0.1.0–0.1.5 (18 oct 2026): protocolo original en `vtsalamanca/Buscar-Curro`; continuidad, auditoría de fuentes, elección HTTP/API y descubrimiento de capacidades.
- 0.1.6 (19 oct 2026): desarrollo y pruebas locales primero; validación remota selectiva y medición del coste total.
- 0.2.0 (19 oct 2026): integración en Gestor de Skills; activación proactiva donde sea posible, puerta obligatoria de eficiencia, preferencia local, caso Educamos y enlace a ingenieria-fiable.
- 0.2.1 (19 oct 2026): unificación de 0.1.6 y 0.2.0; GitHub pasa a ser la fuente única de verdad y las copias empaquetadas deben reproducirla.
- 0.2.2 (19 oct 2026): la fuente canónica se integra en el paquete completo de GitHub y se distribuye mediante su marketplace.
- 0.2.3 (19 oct 2026): publicación y verificación de plugin incorporadas como fase obligatoria de cambios en skills.
- 0.2.4 (19 oct 2026): autocomprobación al iniciar trabajos, una vez por sesión, con actualización bajo demanda y límites antibucle.




## Ejecución local en Debian aislado por MCP (octubre 2026)
Cuando exista un laboratorio Linux autorizado accesible mediante Desktop Commander en Windows y SSH por clave, considerarlo **antes** de consumir iteraciones de Codex, Work o GitHub Actions en pruebas repetitivas. Seleccionar entre Windows y Debian por dependencias, seguridad, reproducibilidad y coste total; no desplazar automáticamente todo el trabajo a la VM.

**Procedimiento:** verificar dispositivo MCP en línea, máquina virtual encendida, conexión SSH, directorio autorizado, estado de Git, rutas y ausencia de gastos adicionales. Ejecutar inspección, programación y pruebas localmente; comprobar salida real y registrar evidencia. Si se necesita GUI, validar X11/XTEST y ventana; si se necesita `sudo`, preparar la operación y solicitar al usuario únicamente que introduzca la contraseña en la terminal gráfica de Debian. No pedirle que copie comandos si el agente puede realizarlos. Nunca capturar ni guardar contraseñas ni otorgar privilegios permanentes.

**Aislamiento no absoluto:** host-only sin ruta a Internet es una medida verificada de configuración, no una garantía contra reenvío desde Windows o cambios posteriores. Mantener SSH por clave y restringido a la red privada, sin reenvíos innecesarios; no cambiar red ni seguridad sin prueba de reversión y autorización. Conservar instantánea de recuperación y registros sin secretos. Si una tarea requiere Internet, estudiar la obtención autorizada de recursos en Windows y su traslado controlado a Debian, sin abrir NAT ni puente por defecto.

**Evidencia de referencia:** ejecución de SSH/SCP, GUI XFCE mediante XTEST, autorización sudo presencial, desactivación de Avahi y endurecimiento SSH comprobados en laboratorio Debian 13 (2026-10-21). La revisión del firewall/ICS/NAT de Windows y la captura de paquetes no se demostraron exhaustivamente; no presentarlas como certificadas. Consultar `ingenieria-fiable/references/mcp-local.md` para el protocolo técnico. Una skill no instala ni activa el puente por sí misma.

## Continuidad documental mediante almacenamiento autorizado (MCP)
Cuando el usuario quiera dejar documentación, informes o traspasos recuperables desde otras conversaciones, **priorizar un almacén persistente ya autorizado** (por ejemplo, el laboratorio Debian accesible mediante Remote Desktop Commander) frente a obligarle a descargar y volver a subir archivos. Esta regla es transversal; no limita su aplicación al proyecto Golón.
1. Comprobar que el conector existe, que el dispositivo correcto está **online**, que la ruta está autorizada y que su coste marginal es admisible. Una ruta mencionada en otro chat no demuestra conectividad actual. Preferir lecturas directas mediante `read_file` y escrituras seguras cuando estén disponibles.
2. Antes de escribir, determinar documento, destino, clasificación y permisos. No sobrescribir sin comparar el contenido/versión; crear nombres únicos o usar control de concurrencia y copia de seguridad cuando proceda. Prohibido guardar secretos, credenciales o documentación privada en un lugar público.
3. Tras escribir, **leer de vuelta** el archivo, comprobar completitud (líneas/tamaño; hash cuando proceda) y registrar ruta exacta, dispositivo lógico, fecha y estado `GUARDADO_VERIFICADO`. Una respuesta de escritura sin verificación solo acredita `ESCRITURA_COMUNICADA`.
4. Para traspasar a otra conversación, facilitar un **encargo autocontenido de lectura**, con dispositivo y ruta verificados, y pedir a la otra conversación que confirme lectura completa. Evitar cargar y descargar ficheros si ambos chats tienen acceso autorizado; nunca afirmar que pueden leerlos antes de comprobar sus herramientas y permisos.
5. Mantener separadas tres capacidades: **persistencia del archivo**, **lectura bajo demanda desde otro chat** y **entrega/notificación automática entre chats**. Las dos primeras no prueban la tercera. Ante conector ausente, dispositivo apagado, permisos faltantes o coste incierto, informar del bloqueo y usar una alternativa disponible (archivo adjunto, Library o texto copiable), sin inventar un acceso.
6. Este método **no instala plugins ni activa skills en otras cuentas**, no comparte memoria entre chats y no hace que el asistente consulte Debian automáticamente en cada conversación. La activación depende de que esta skill/instrucción esté cargada, de la intención de la tarea y de la conexión real. En pilotos de evaluación (por ejemplo, ChatGPT Free), controlar qué documentación se entrega para no contaminar pruebas de aprendizaje.
**Evidencia de origen (2026-10-22):** lectura completa de un documento Markdown de 72 líneas desde `debian-laboratorio` mediante Remote Desktop Commander en Chat normal. Queda por verificar como procedimiento genérico de extremo a extremo la escritura, relectura y recuperación desde otra conversación nueva; no presentar esa cadena como ya superada.

### Directorios operativos y conservación en Debian (configuración del usuario)
Para los traspasos temporales usar el dispositivo lógico `debian-laboratorio` y la base `/home/labgestor/intercambio-chatgpt/` **solo tras verificar conexión, ruta y permisos**. Directorios creados y verificados el 2026-10-22:
- `descargas/`: archivos temporales de intercambio ya recuperados, cuando no sean la única copia.
- `pendientes/`: archivos todavía no recuperados o cuya recepción no está verificada.
- `/home/labgestor/proyectos/`: resultados y documentación permanente de los proyectos, fuera de la limpieza temporal.

Al solicitar el usuario un resumen para abrir otro chat, un traspaso o el envío de un archivo sin formato de entrega alternativo explícito, **intentar por defecto guardar el contenido en Debian**, verificar la lectura y facilitar una instrucción breve con el dispositivo y la ruta exacta para que el chat destinatario lo recupere. No obligar a copiar grandes bloques, descargar o subir de nuevo. Si el chat destinatario no tiene Desktop Commander cargado, indicarlo y no prometer recuperación automática.

**Limpieza segura:** revisión mensual recomendada; los 30 días constituyen un *umbral para inventariar candidatos*, no permiso de borrado. Nunca borrar automáticamente por antigüedad, ni borrar un pendiente, un documento único, un expediente activo o un archivo bajo `proyectos/`. Antes de toda eliminación, listar candidatos con fecha, tamaño, ruta y estado de recepción; comprobar que existe una copia permanente o recepción confirmada, solicitar aprobación específica para borrar y registrar el resultado. No instalar cron, timers, trabajos programados ni servicios persistentes para limpieza sin autorización separada. La limpieza no está activada.

### Publicación integrada como condición de cierre
Cuando el usuario autoriza modificar una habilidad, esa misma autorización incluye **preparar y publicar la actualización en el plugin privado existente** y verificar los archivos publicados, siempre que herramientas, permisos y coste cero estén comprobados. Ejecutar el runbook `skills/ingenieria-fiable/references/actualizar-skills.md` en la misma tarea: fuente canónica y versión → tests → ZIP desde commit exacto → carga en host del publicador → `Plugin Creator.update_plugin` protegido por `expected_release_id` → relectura de release. No exigir una segunda solicitud de «actualiza el plugin».
**Prohibición de cierre ambiguo:** si la transferencia al host de Plugin Creator o la publicación no se ha efectuado, registrar `FUENTE_ACTUALIZADA / PUBLICACIÓN_PENDIENTE`, no «actualización completada». No usar rutas de Debian o Windows como si fueran rutas locales del publicador, ni prometer carga en chats nuevos sin comprobarla. Mantener release anterior, plugin ID, privacidad y coste adicional cero; no habilitar automatizaciones ni inventar accesos.

### Transferencia probada al Plugin Creator
El 22-10-2026 se actualizó el plugin privado existente desde una **conversación normal** con `Plugin Creator.update_plugin`, usando un ZIP que el usuario adjuntó y cuya ruta real `/mnt/data/...` fue verificada, con SHA-256 y release ID comprobados. El plugin 0.4.18 y las ocho skills se releyeron satisfactoriamente. **Esta es la ruta prioritaria verificada**, y debe intentarse antes de Work o de experimentar de nuevo con rutas remotas. Tras modificar cualquier skill, empaquetar, solicitar el adjunto únicamente si no existe transferencia directa verificada, publicar y comprobar la nueva release en el mismo trabajo. Leer el procedimiento canónico en `ingenieria-fiable/references/actualizar-skills.md`. La carga en un chat nuevo es una comprobación independiente.

### Preferencia obligatoria del usuario: Debian como ejecutor
Para empaquetado, pruebas, organización de archivos y procesos locales de este proyecto **utilizar directamente el dispositivo MCP `debian-laboratorio`, no Windows**. No elegir Windows por comodidad, por conservar una copia Git anterior ni para trasladar archivos, salvo autorización expresa posterior del usuario. Si Debian carece de Git u otra dependencia, intentar una alternativa segura allí mismo usando archivos canónicos obtenidos mediante el conector GitHub y verificar su integridad; si las garantías de reproducibilidad no son equivalentes, registrar esa limitación. No instalar dependencias ni alterar el aislamiento de red sin permiso. El almacenamiento temporal está en `/home/labgestor/intercambio-chatgpt/`. Para Plugin Creator, comprobar separadamente la transferencia del ZIP hasta el entorno del publicador; la existencia del ZIP en Debian no demuestra que el publicador lo reciba.

### Arquitectura MCP ordinaria: Debian exclusivo, Windows excepcional
La infraestructura ordinaria de escritorio remoto del usuario es **únicamente `debian-laboratorio`**. En cada sesión, consultar dispositivos y seleccionar Debian; la ausencia/desconexión del agente Windows es **normal y esperada**, no una incidencia a reparar. No usar herramientas contra Windows, no encender su agente, no abrir sesiones SSH a través de Windows ni pedir al usuario que reactive Windows por conveniencia. Si Debian no está disponible, informar del bloqueo real y ofrecer una alternativa sin Windows. **Cualquier acceso excepcional a Windows requiere autorización expresa para la operación concreta**, incluso cuando el dispositivo figure online. No apagar ni desinstalar Windows ni alterar SSH, proxy o red sin consentimiento y plan de recuperación. La disponibilidad futura de Debian debe verificarse de forma independiente del anfitrión: no suponer conexión autónoma si todavía depende del proxy Windows; documentar la dependencia y comprobarla antes de prometerla.

### Norma transversal: Debian principal, Drive auxiliar, Windows excepcional
**Aplicación general a todos los proyectos, chats y tareas:** `debian-laboratorio` es el centro operativo habitual (archivos, scripts, pruebas y transferencia directa entre conversaciones). Utilizar Google Drive **solo como transporte privado y temporal** cuando la entrega/descarga de archivos no pueda realizarse directamente por Debian y se compruebe un beneficio real; no duplicar documentos innecesariamente ni hacerlos públicos. Verificar la capacidad real de subir ZIP a Drive: `upload_file` necesita una referencia de archivo compatible, **no acepta rutas locales**. No asegurar ni automatizar un puente Debian→Drive antes de probarlo. Aplicar retención con revisión, nunca borrar por antigüedad sin autorización. Windows: acceso remoto cerrado al terminar la migración, **uso excepcional solo con autorización expresa para operación concreta**, aunque aparezca conectado. **Puerta previa al cierre:** probar que Debian y su recuperación funcionan sin agente ni proxy de Windows; no cerrar prematuramente el acceso ni cambiar redes sin consentimiento. Si Debian falla, explicar el bloqueo, no activar Windows por iniciativa propia. Coste adicional 0 € salvo autorización.


## Puente binario verificado: GitHub Actions → Plugin Creator (23-10-2026)
**Ruta preferente** para cambios en las ocho skills: GitHub `vtsalamanca/gestor-de-skills` es fuente canónica. Cada push a `main` que cambia `skills/**`, manifiesto, pruebas, empaquetador o workflow dispara `.github/workflows/prueba-puente-plugin.yml` en runner estándar `ubuntu-latest`, timeout 5 minutos, y genera un artefacto ZIP SIN DOBLE ENVOLTURA mediante `actions/upload-artifact@v7` y `archive: false`, retención 1 día.
1. Confirmar permiso/autorización de publicación, repo público y runner estándar; presupuesto extra 0 €. No crear runners grandes, endpoints de pago ni secretos. El workflow solo **empaqueta**, nunca publica automáticamente sobre el plugin.
2. Confirmar ejecución concluida y satisfactoria. Obtener ID de ejecución y de artefacto con conector GitHub `fetch_workflow_run_artifacts`. El ZIP se denomina según la versión del manifiesto. Confirmar que el SHA del artefacto coincide con el hash esperado del empaquetado canónico; que haya ocho skills, sin claves ni datos sensibles.
3. `download_workflow_artifact` devuelve referencia binaria y crea archivo montado en ChatGPT. Usar la ruta **exacta anunciada por la herramienta en la sesión activa**, jamás inventarla. No pasar ruta de Debian directamente a Plugin Creator ni tratar una URL de Drive como ZIP.
4. Obtener release actual con `Plugin_Creator.get_plugin_metadata`. `Plugin_Creator.update_plugin` con `plugin_id=plugins_6add39166308819193bc271cfa0af302`, `archive` apuntando a archivo montado comprobado y `expected_release_id` vigente. No crear plugin adicional.
5. Leer `get_plugin_files` después: versión correcta, ocho skills, soporte y manifiesto; distinguir publicación verificada de recarga efectiva de otras sesiones. Anotar nuevo release ID y mantener rollback. Si falla, preservar release vigente e informar `PUBLICACION_BLOQUEADA`.
6. Sin workflow concluido o sin referencia registrada, detener publicación, no probar rutas remotas repetidamente. No activar publicación automática sin control de cambios y de permisos.
**Prueba real:** workflow run `39876898171`; artifact `12467699397`; hash `af8a2ef92e7d9a2e03bf057a69411550de1720b88166e77aa1f18d841b28bf09`; Plugin Creator confirmó release `pluginrel_6adaa70f636881918703ea77cc60d33f` versión 0.4.22, 23 ficheros. Se mantiene la publicación como acción explícitamente autorizada, mientras que la creación del artefacto queda automatizada.

## Control del presupuesto de herramientas remotas (2026-10-28)

Aplicar a Desktop Commander Remote y conectores con cuota. Consultar saldo una vez al empezar cada bloque importante, sin confundir el porcentaje remoto con contadores de ejecución locales. No inferir operaciones exactas ni fecha de reinicio.

Umbrales operativos: más de 30 % restante: lotes normales; de 15 a 30 %: ahorro, agrupar diagnóstico, ejecución y verificación; 15 % o menos: reserva para seguridad, recuperación, entregables e hitos; 5 % o menos: detener exploraciones no esenciales. Son reglas internas conservadoras, no límites del proveedor.

Antes de una llamada: recuperar resultados existentes, formular hipótesis, seleccionar el programa local revisado, fijar tiempos, número de páginas y reintentos máximos. Una llamada remota puede lanzar un lote local delimitado con salida breve; no usar la cuota para ejecutar cada búsqueda, regex o comprobación. Evitar sondeos repetitivos de procesos; leer salida una vez tras un intervalo razonable. Usar caché no sensible y deduplicar.

Tras dos fallos equivalentes sin nueva evidencia: detener y diagnosticar. Diferenciar errores de red, herramienta, permisos, bloqueo de seguridad, autenticación y agotamiento de cuota. Nunca eludir protecciones, ampliar permisos ni activar procesos persistentes por ahorrar llamadas.

Al cerrar: registrar cuota inicial/final cuando esté disponible, operaciones remotas por fase, resultado comprobado, bloqueos y siguiente acción. Reutilizar Debian para procesamiento intensivo local, MCP remoto para orquestación desde ChatGPT. Coste adicional por defecto 0 €: ninguna API, plugin o recurso facturable sin tarifa, estimación y autorización expresa.
