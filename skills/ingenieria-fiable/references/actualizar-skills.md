# Protocolo canónico de actualización y publicación del Gestor de Skills

**Uso obligatorio:** cuando el usuario ordene modificar una skill, actualizar el plugin, publicar una versión o recuperar un fallo de distribución. Fuente única: `vtsalamanca/gestor-de-skills`. Aplicar con `organizaciondeltrabajo`, `integrar-skills` e `ingenieria-fiable`. **No activar comprobaciones por cada chat**, cron ni GitHub Actions por defecto. Presupuesto adicional 0 €.

## Flujo indivisible al modificar cualquier skill (octubre de 2026)
Toda petición de cambio de skill incluye, sin segunda orden del usuario, **edición de la fuente canónica + versión y manifiestos + pruebas + empaquetado + actualización del plugin privado existente + lectura de verificación y comprobación de carga si está disponible**. No cerrar la tarea diciendo únicamente que se actualizó GitHub; si la publicación está bloqueada, declarar `FUENTE_ACTUALIZADA / PUBLICACIÓN_BLOQUEADA` y concretar la causa comprobada. No prometer automatización autónoma fuera de la conversación ni eludir aprobación de la plataforma. No crear otro plugin ni sustituir por archivos para copiar y pegar. Presupuesto adicional cero.

Cuando la modificación trate sobre traspasos de contexto o archivos, mantener como comportamiento preferido `almacenar en Debian mediante MCP → verificar relectura → comunicar dispositivo y ruta para recuperación desde otro chat`. Solo usar descargas, adjuntos o copiado manual si Debian no está accesible o el usuario los solicita expresamente. Esta preferencia no equivale a notificación automática de otra conversación.

## Procedimiento de publicación reproducible y puerta de cierre (versión 2026-10-22)

**Contrato de finalización:** una petición de modificar una skill autoriza a intentar en el mismo trabajo fuente, pruebas, paquete, publicación y verificación. No se solicita una segunda orden para actualizar el plugin. Una actualización solo se declara **COMPLETADA** cuando el plugin privado existente contiene efectivamente la modificación. Si una condición bloquea la publicación, la respuesta indicará `PUBLICACIÓN_PENDIENTE` y el impedimento demostrado, sin dar por finalizada la distribución ni pedir órdenes repetidas.

### Secuencia ejecutable y evidencias
1. **Identidad fija:** comprobar el repositorio `vtsalamanca/gestor-de-skills` y el complemento privado `plugins_6ad40dbac6088191b25671203dfacfe3`; obtener su `current_release_id` y estado PRIVATE/USER mediante Plugin Creator. Rechazar un destino diferente, permisos ambiguos o cambios inesperados. Nunca crear otro complemento.
2. **Cambio atómico de fuente:** modificar lo mínimo necesario en `main` o en rama de trabajo autorizada, comprobar los cambios ajenos, incrementar versión semántica de la skill si tiene campo de versión y del paquete, alinear `.codex-plugin/plugin.json` con `.agents/plugins/marketplace.json`, y fijar SHA completo de commit. Los README no deben prometer versiones no publicadas.
3. **Construcción del commit exacto:** obtener `scripts/package_plugin.py` y `tests/test_package_plugin.py` de ese mismo SHA. Ejecutar sus tests y construir desde los bytes comprometidos, no desde directorios modificados sin confirmar. El ZIP debe contener `.codex-plugin/plugin.json`, README y las ocho skills completas; rechazar secretos, enlaces inseguros, omisiones y discrepancias de versión. Guardar SHA-256, tamaño, inventario, commit y registro de pruebas.
4. **Frontera entre hosts, comprobada ANTES de publicar:** `update_plugin.archive` debe referir a un archivo **host-uploaded** localizable por Plugin Creator. Distinguir **(A)** archivo en Windows/Debian por MCP, **(B)** archivo del contenedor de análisis, **(C)** archivo subido al entorno del publicador. Ni una ruta `C:\...` ni `/home/labgestor/...` ni `/mnt/data/...` demuestran por sí solas C. Comprobar una vía autorizada de carga y que el archivo está presente para ese publicador. Reutilizar la vía que funcionó antes *solo cuando siga comprobada*. No transferir datos privados a un alojamiento público. Si no existe mecanismo accesible, registrar **BLOQUEO_TRANSFERENCIA** sin llamar a `update_plugin` con rutas inventadas; investigar una alternativa nueva una sola vez por hipótesis (por ejemplo, un runtime de Work autorizado con acceso confirmado al publicador).
5. **Preflight de publicación:** releer `current_release_id` inmediatamente antes del cambio; si varió, contrastar los archivos y detenerse ante conflicto. Con archivo cargado y verificado, invocar una vez `Plugin Creator.update_plugin` con `plugin_id` fijo, `archive` válido y `expected_release_id` observado. No modificar visibilidad, credenciales, componentes ajenos o alcance.
6. **Postflight obligatorio:** leer `get_plugin_metadata` y `get_plugin_files` de la nueva release; comprobar nuevo release ID, versión, los ocho `SKILL.md`, referencias relevantes y el texto realmente cambiado. Verificar PRIVATE/USER y capacidad de recuperar versión anterior si disponible. La coincidencia del número de versión SIN contenido no es evidencia suficiente.
7. **Carga en nuevos chats:** comprobar, en conversación nueva con plugin instalado, que la skill accesible contiene el texto o versión recién publicados. Esta etapa requiere una sesión nueva real y puede quedar `CARGA_NO_PROBADA`; no declarar universalidad ni forzar recarga del chat presente.
8. **Informe y continuidad:** registrar por separado `FUENTE_OK`, `TESTS_OK`, `ZIP_OK`, `TRANSFERENCIA_OK`, `PLUGIN_OK`, `CARGA_NUEVO_CHAT` y `CODEX`, cada uno con prueba/fecha. El cierre de entrega diferencia `PUBLICADO_VERIFICADO` de `FUENTE_ACTUALIZADA_PUBLICACIÓN_PENDIENTE`. Presupuesto adicional 0 €; detener cualquier servicio con tarifa por uso no comprobada.

### Pruebas de fallo mínimas
- Ruta visible únicamente en Debian/Windows: publicación detenida antes de enviar path inaccesible.
- `expected_release_id` obsoleto: no sobrescribir.
- ZIP parcial, versión distinta o skill omitida: no publicar.
- Publicación aceptada pero el archivo de la habilidad no aparece: no declarar éxito.
- Chat nuevo carga versión antigua: conservar estado `PLUGIN_OK / CARGA_NO_PROBADA` o `CARGA_FALLIDA`, según evidencia.
- Autoridad o coste desconocidos: detener y conservar release previa.

**Alcance real:** esta metodología reduce pasos manuales y solicitudes repetidas, pero no convierte la skill en un proceso autónomo ni habilita una ruta de transferencia que no exista. No programar acciones automáticas futuras ni publicar sin pruebas y permisos.

## Ruta preferente VERIFICADA: adjunto del chat → Plugin Creator (22-10-2026)
**Evidencia real:** el archivo `gestor-de-skills-0.4.18.zip` (58.307 bytes, SHA-256 `f048569cf620a02ebe0729320a12330116adb78cb9b20b628eecdc0288fff0a1`), creado desde el commit `85e185f47e931f8e6d887bc14106057149166ec1`, fue adjuntado por el usuario a una conversación normal. La herramienta `Plugin Creator.update_plugin` aceptó la ruta del adjunto efectivamente montado `/mnt/data/gestor-de-skills-0.4.18.zip` con `expected_release_id` vigente. Resultado: plugin personal PRIVADO existente actualizado de 0.4.15 a 0.4.18; nueva release `pluginrel_6ada77e02bb881919e0ba8b2921e9d96`. Relectura con `get_plugin_files` confirmó 23 entradas, las ocho skills, `organizaciondeltrabajo` 0.2.15, normas de Debian y runbook de publicación. **No se comprobó aún la carga en un chat nuevo.**

### Ejecución prioritaria para la próxima modificación
1. Verificar GitHub, Plugin Creator, Remote Desktop Commander y permisos presentes. Leer versión/release actual del plugin fijo, comparar con GitHub y definir un único incremento coherente de versión. No repetir búsquedas si está todo disponible.
2. Actualizar la fuente canónica y manifiestos, recuperar el SHA del commit; ejecutar las pruebas del empaquetador **desde la raíz del repositorio** (`python -m unittest discover -s tests -p test_package_plugin.py`). Los tests deben comparar dinámicamente la versión del manifiesto, nunca una versión histórica codificada. Tratar los tests omitidos por separado.
3. Construir con `scripts/package_plugin.py` desde el commit SHA exacto; verificar ZIP, número de skills/archivos y hash. Es posible generar en Windows mediante Desktop Commander, o en Debian si dispone de las herramientas; ninguno de esos paths es automáticamente accesible al publicador.
4. **Ruta preferida demostrada:** adjuntar el ZIP a la **misma conversación** desde el equipo del usuario. Si el chat puede montar el archivo en su entorno, **verificar la ruta real**, SHA-256 e inventario antes de pasarlo a Plugin Creator. No inferir la ruta por nombre del adjunto. Se admite esta intervención única como último tramo fiable. No pedir al usuario que copie archivos de texto, no usar Work por defecto.
5. Consultar de nuevo el `current_release_id`; invocar `update_plugin(plugin_id=ID_PRIVADO_EXISTENTE, archive=RUTA_ADJUNTO_MONTADO, expected_release_id=RELEASE_ACTUAL)`. Ante fallo de host o archivo, **no** repetir la misma ruta; cambiar hipótesis.
6. Leer `get_plugin_files` de la release publicada y verificar contenido de todas las modificaciones, no solo la versión. Confirmar ocho skills, privacidad e identidad conservadas. Distinguir `PUBLICACIÓN_VERIFICADA` de `CARGA_NUEVO_CHAT_PENDIENTE`; el chat abierto antes de la publicación puede tener skill antigua.
7. **Puerta obligatoria de cierre:** no finalizar una petición de modificación de skills mientras quede por intentar publicación y postverificación; si la única barrera es que el usuario todavía no adjuntó el ZIP, pedir **solo esa acción** y retomar directamente la publicación cuando se adjunte, sin abrir otra investigación. Si el host admite carga directa en el futuro, preferirla tras una prueba real.

**Seguridad y límites:** no crear nuevos plugins ni cambiar privacidad; no asumir que un documento alojado en Debian equivale a un adjunto del chat; mantener release anterior y evitar costes no autorizados. La operación tiene pasos verificables, pero no es infalible: declarar bloqueos y pruebas pendientes con precisión.

## Regla principal: recuperar antes de improvisar
Este flujo ya se ha ejecutado con éxito anteriormente. **No declarar imposible la transferencia de un ZIP ni derivar automáticamente a Work solo porque Plugin Creator rechace una ruta `C:\\...`**. Esa ruta pertenece al Windows remoto de Desktop Commander y **no es una ruta local al host de Plugin Creator**. Se debe comprobar primero el procedimiento de preparación de archivo admitido en el entorno de publicación y las herramientas disponibles; una ruta existente en Windows nunca demuestra accesibilidad desde el publicador.

Distinguir con precisión: `FUENTE_ACTUALIZADA`, `PAQUETE_VALIDADO`, `ARCHIVO_TRANSFERIDO`, `PLUGIN_PUBLICADO`, `CARGA_VERIFICADA`, `CODEX_VERIFICADO` y `BLOQUEADO`. No llamar «actualizado» al plugin por haber actualizado GitHub o generado un ZIP.

## Datos persistentes (identidad; no son credenciales)
- Repositorio: `vtsalamanca/gestor-de-skills`, rama `main`, **SHA del commit actual obtenido en cada operación**.
- Plugin privado personal existente: `plugins_6ad40dbac6088191b25671203dfacfe3`. Preservar ID, nombre, ámbito USER y privacidad PRIVATE; **no crear otro plugin**.
- Publicador: herramienta oficial `Plugin Creator`, operación `update_plugin`, con `expected_release_id` recién leído.
- Compilador reproducible: `scripts/package_plugin.py` en el repositorio canónico; pruebas `tests/test_package_plugin.py`. No reutilizar un script antiguo que presuponga siete skills: el inventario actual tiene **ocho**, incluida `acceso_webs`. Volver a contar siempre al empaquetar.
- El número de versión y release ID **no se fijan en esta referencia**: consultarlos al ejecutar. Los ejemplos históricos 0.4.11/0.4.12/0.4.14 solo ayudan al diagnóstico.

## A. Descubrimiento, permisos y versión
1. Recuperar informe de publicación reciente, repo y archivos afectados. Leer instrucciones de las skills. Consultar GitHub `main`, SHA completo, manifiesto `.codex-plugin/plugin.json`, marketplace `.agents/plugins/marketplace.json`, lista de directorios bajo `skills/`, pruebas y README. Evitar tomar una caché local antigua como fuente.
2. Consultar `Plugin Creator.get_plugin_metadata` o `get_plugin_files` para versión instalada, `current_release_id`, lista de archivos y autorización sobre el plugin exacto. Comprobar si ya está en la versión objetivo y si su contenido coincide; si es así, **no republicar**.
3. Comprobar herramientas realmente disponibles en este chat: conector GitHub, Plugin Creator, runtime local del publicador, Desktop Commander (dispositivo conectado) o mecanismo de archivo adjunto/transferencia. No inferir que Chat, Work, Codex, Windows y el runtime de Plugin Creator comparten sistema de archivos.
4. Preservar modificaciones ajenas y árbol de trabajo local: `git status --short`, SHA y remoto; `git fetch` no es `git pull`. Una copia local desfasada puede servir para `git archive origin/main` si el commit está disponible. No sobrescribir el checkout para empaquetar.

## B. Preparación y validación del paquete
5. Fijar el SHA de la versión canónica. Verificar que el empaquetador del **mismo SHA** acepta las skills del inventario actual. El fallo conocido `Faltan=[]; sobran=['acceso_webs']` significa que se ejecutó una copia **antigua** del script: no quitar la skill del ZIP, sino usar el empaquetador actualizado desde GitHub y probar su ejecución.
6. Ejecutar `python -m unittest discover -s tests -p "test_package_plugin.py"` y `python scripts/package_plugin.py --repository . --commit <SHA_COMPLETO> --output dist/gestor-de-skills-<VERSION>.zip` (ajustar sintaxis al terminal). Preferir una exportación desde el SHA exacto y no desde archivos de trabajo. Si no existe repositorio local válido, seguir el parámetro `--repository` oficial y verificar los permisos de red.
7. Comprobar que ZIP y manifiestos tienen la misma versión, que contiene todas las skills y referencias y ningún secreto, archivo temporal o symlink. Calcular SHA-256 de ZIP y entradas, cotejar con el informe; opcionalmente construir dos veces y exigir hash idéntico. Registrar ruta **en el sistema que lo generó**, tamaño, SHA y recuento.

## C. Transferencia: resolver explícitamente el límite entre entornos
8. **No enviar a Plugin Creator un path de Windows (p. ej. `C:\\Users\\...\\dist\\archivo.zip`) como si fuera un archivo del host del publicador**. El error `INVALID_ARGUMENT` puede ser fallo de archivo inaccesible, no de permisos del plugin.
9. Primera ruta: crear o transferir el ZIP a una **ruta absoluta accesible al host de Plugin Creator** usando herramientas de archivo del propio entorno cuando estén realmente disponibles; preferir reproducir desde GitHub en ese runtime con bytes canónicos antes que copiar una ruta opaca. Leer el contrato actual de `update_plugin` y las capacidades de archivo; comprobar la ruta y ZIP allí. Una ruta `/mnt/data/...` solo es válida si se ha creado y verificado en ese host **y** la herramienta publicadora puede acceder a ella; nunca asumir que el contenedor, Work y Plugin Creator comparten host.
10. Si el ZIP solo está en Desktop Commander, buscar un **mecanismo de transferencia admitido** hacia el host de Plugin Creator (adjunto de conversación, carga oficial o vía de archivo compatible). No exponer el ZIP públicamente ni subir credenciales. Si la sesión actual no admite transferir, usar **Work solo si el usuario lo ha autorizado y puede acceder al mismo archivo y publicador**. Work debe verificar hash antes de enviar. No repetir llamadas `update_plugin` con exactamente la misma ruta inválida.
11. Alternativa documentada: el usuario puede adjuntar el ZIP por la interfaz si ningún medio autorizado lo transfiere; **último recurso**, no primera opción. No afirmar que puede completarse «sin intervención» cuando ese tramo no está probado. La llamada `update_plugin` admite archivos ZIP o tar.gz accesibles mediante la carga del host, no texto base64 arbitrario ni URL inventada.
12. Antes de publicar, volver a leer `current_release_id` para prevenir condiciones de carrera. Si cambió, releer la release y comparar antes de ejecutar.

## D. Publicación y verificación
13. `Plugin Creator.update_plugin(plugin_id=<ID_EXISTENTE>, archive=<RUTA_ADMITIDA_Y_VERIFICADA>, expected_release_id=<RELEASE_ACTUAL>)`. No borrar rutas ni alterar ámbitos salvo autorización expresa. Aceptar solo una versión igual a la canónica o un resultado de versionado documentado; no forzar.
14. Releer metadata y archivo publicado mediante `get_plugin_files` en lotes permitidos (el método limita el número de rutas por llamada). Verificar manifest versión, lista de skills, archivos, referencias y muestras o hashes de contenido contra la fuente; comprobar que la release ID cambió, que sigue siendo privada y que la anterior continúa recuperable cuando se pueda verificar.
15. Distinguir `PLUGIN_PUBLICADO` de `CARGA_VERIFICADA`: un chat abierto antes del cambio puede conservar una copia anterior. Una nueva conversación es un test de carga, no una nueva publicación.
16. Si Codex procede: comprobar marketplace e instalación/caché realmente activa. Consultar también `references/mcp-local.md` y el procedimiento de recuperación local ya documentado en `organizaciondeltrabajo`. No concluir que Codex recibió cambios simplemente porque GitHub avanzó.

## E. Fallos conocidos y recuperación
| Síntoma | Causa probable | Reacción obligatoria |
| --- | --- | --- |
| ZIP generado pero `update_plugin` → `INVALID_ARGUMENT` con ruta Windows | Ruta de otro equipo/host; archivo no cargado al publicador | Verificar host, transferir/recrear de modo admitido, **no** repetir mismo path |
| `sobran=['acceso_webs']` | Script local anterior a la incorporación de la octava skill | Utilizar script del SHA actual; mantener ocho skills |
| GitHub versión más nueva que plugin | Fuente editada, aún no distribuida | Generar paquete, transferir, publicar y releer |
| Versión en plugin correcta, chat carga anterior | Caché/sesión iniciada antes de publicar | Validar nueva sesión; no republicar sin divergencia |
| Marketplace Codex o caché desactualizada | Distribución independiente | Verificar marketplace, caché y rutas; seguir recuperación específica |
| `expected_release_id` rechazado | Otra publicación cambió la release | Releer metadata, comparar, no sobrescribir a ciegas |
| Coste desconocido, permisos ausentes, transferencia realmente imposible | Bloqueo de entorno | Conservar la release actual y señalar **un único** paso mínimo fundado |

## F. Criterio de cierre
Entregar **SHA canónico, versión, lista/recuento de skills y archivos, pruebas ejecutadas, SHA-256 del ZIP, release anterior/nueva, lecturas de verificación, estado Codex y coste comprobado**. Si solo se ha creado el ZIP, decir «paquete validado, publicación pendiente», no «actualizado». Registrar qué mecanismo de transferencia funcionó realmente para que la próxima vez se reutilice sin ensayo y error. No afirmar que una ruta de Windows es inaccesible «desde ChatGPT» si no se ha inspeccionado el entorno de transferencia concreto.

**Experiencias documentadas:** una release anterior se publicó con un ZIP adjunto; otra publicación se consiguió desde Work; al actualizar 0.4.14 un ZIP creado en Windows falló en Plugin Creator por ruta de host inválida. Son rutas **observadas**, no promesas de que idénticas herramientas estén disponibles en todas las sesiones.

### Restricción de entorno para publicaciones futuras
Para construir, validar y almacenar paquetes, usar `debian-laboratorio` como entorno MCP ordinario. No emplear Windows como respaldo silencioso aunque figure online; requerir autorización expresa por cada excepción. El ZIP validado de Debian puede almacenarse en `/home/labgestor/intercambio-chatgpt/pendientes/`, pero esa ruta **no** equivale a un archivo subido al entorno de Plugin Creator. Recuperar los bytes mediante una vía de carga realmente demostrada; cuando no la haya, explicar la única intervención manual necesaria. La ausencia de Git u otras dependencias en Debian no autoriza automáticamente instalar software ni cambiar la red.
