# Protocolo canónico de actualización y publicación del Gestor de Skills

**Uso obligatorio:** cuando el usuario ordene modificar una skill, actualizar el plugin, publicar una versión o recuperar un fallo de distribución. Fuente única: `vtsalamanca/gestor-de-skills`. Aplicar con `organizaciondeltrabajo`, `integrar-skills` e `ingenieria-fiable`. **No activar comprobaciones por cada chat**, cron ni GitHub Actions por defecto. Presupuesto adicional 0 €.

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
