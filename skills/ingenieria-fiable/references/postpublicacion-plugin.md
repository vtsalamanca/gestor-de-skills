# Publicación privada con verificación y recuperación (obligatorio)

**Fuente única:** GitHub vtsalamanca/gestor-de-skills. Plugin activo: plugins_6add39166308819193bc271cfa0af302, PRIVATE, USER. No utilizar jamás el ID anterior.

## Antes de publicar
1. Mantener copia original de la release actual descargada con get_owned_plugin_archive (registrar ID, versión y SHA-256) y copia Git canónica; nunca editar respaldos.
2. Generar ZIP exclusivamente mediante scripts/package_plugin.py desde el SHA exacto de main. Ejecutar scripts/preflight_plugin_upload.py con su SHA-256. Rechazar marketplace y overlays manuales.
3. Obtener get_plugin_files de la release activa y confirmar que es legible y no contiene marketplace. Si hay error, **no actualizar**.

## Después de publicar: prueba obligatoria del plugin real
1. Ejecutar update_plugin con expected_release_id actual y el archivo del artefacto GitHub Actions; registrar nuevo release ID.
2. Ejecutar get_plugin_files sin read_paths y recuperar todos los miembros con read_paths (fraccionar las lecturas si es necesario). El servicio permite hasta 1 MiB por petición. Conservar el resultado estructurado, asegurando que contents contiene todos los archivos. Si el formato del conector no puede exportarse sin pérdidas, comprobar hashes manualmente y declarar esa limitación.
3. Comparar con el ZIP de esa publicación utilizando scripts/postflight_plugin_release.py ZIP export.json. Exige identidad PRIVATE/USER, release ID, versión, inventario completo y hashes del contenido de todos los archivos. Si falla, la publicación **no se considera verificada**.
4. Probar una publicación sucesiva antes de considerar reparado un cambio en la cadena de despliegue. No automatizar la publicación de cambios no aprobados.

## Si falla una actualización
- No repetir indefinidamente el mismo update_plugin ni fabricar ZIP parciales; congelar cambios y conservar URL, ID y hashes.
- Intentar lectura de la nueva release; diferenciar error del archivo transferido, error de autorización, error de formato y conflicto de release existente.
- Si el backend impide rollback o eliminar manifiestos, **no asegurar recuperación automática**: conservar original, levantar informe y preparar una migración con nuevo ID solo tras autorización explícita y respaldo.
- La herramienta uninstall_app no garantiza borrar un objeto de Plugin Creator; comprobar por separado.

Este procedimiento evita errores controlables, no garantiza que OpenAI nunca falle. La verificación posterior depende de que Plugin Creator suministre contenido completo.
