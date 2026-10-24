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


## Método directo alternativo: comparación exhaustiva por conectores (verificado 25-10-2026)

Cuando no sea posible exportar automáticamente todo el JSON de Plugin Creator a un archivo local, realizar la comprobación con el orquestador de herramientas, sin pasar por transferencias de archivos. **Este método se probó con 26/26 coincidencias sobre la release 0.4.32**.

1. Leer una vez `Plugin_Creator.get_plugin_files` (sin read_paths) y fijar `plugin_id`, `current_release_id`, versión, estado PRIVATE y listado completo. Rechazar next_offset sin consumir y nombres repetidos.
2. Tomar los paths del resultado, nunca inventarlos. Procesar subgrupos de **cuatro o cinco archivos** (el servicio rechaza peticiones de demasiados archivos).
3. Para cada subgrupo leer contenido con `Plugin_Creator.get_plugin_files({plugin_id,read_paths:subgrupo})`. Rechazar missing_paths, size_limited_paths y content ausente. Comparar cada cadena `contents[path]` **exactamente** con el contenido UTF-8 de `GitHub.fetch_file` del mismo path y del SHA concreto usado para empaquetar, no de main móvil. Verificar las 26 rutas esperadas.
4. Si todos los ficheros son UTF-8, una igualdad exacta con los bytes de GitHub equivale a igualdad de SHA-256 respecto del paquete canónico que conserva los bytes Git. No aplicar conversión de líneas ni normalización Unicode. Para archivos binarios esta técnica no sirve: usar descarga oficial y validador de hashes.
5. Releer el release al finalizar. Si cambió el release_id durante la prueba, invalidar los resultados y repetir para una versión estable. Publicación verificada solo cuando nombre, privacidad, release, inventario, contenido completo y versión coinciden.
6. Guardar un informe de comprobación en Debian con commit SHA, plugin_id, release_id, total, discrepancias y limitaciones. Este método compara directamente, pero **no constituye exportación JSON automática ni ejecución desatendida**. Si en el futuro el conector facilita volcado fiable, utilizar `postflight_plugin_release.py` sobre el JSON exportado.

**Prueba real:** ID `plugins_6add39166308819193bc271cfa0af302`, release `pluginrel_6add3ad46ad8819185ecab3034fe1f8c` (0.4.32), commit `3b5b89f8e5f206c12abaca52e77bd98ff71df837`, 26 comparaciones de contenido contra GitHub, 0 diferencias, tres lotes de 8/8/10 archivos, subpeticiones de hasta cinco.
