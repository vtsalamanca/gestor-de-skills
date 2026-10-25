# Gestor de Skills 0.4.33

Repositorio canónico independiente para skills transversales de ChatGPT y Codex.

Complemento privado con nueve skills especializadas:
- `descubrir-skills`: búsqueda y comparación de skills públicas.
- `auditar-skills`: revisión estática y control de seguridad/costes.
- `integrar-skills`: compatibilidad e integración por plataforma.
- `inventariar-skills`: versiones, inventario y detección de duplicados.
- `crear-skills`: diseño y validación de skills propias.
- `organizaciondeltrabajo`: coordinación general, continuidad y coste total.
- `acceso_webs`: estrategias de acceso web y conectores eficientes, incluida la integración MCP y patrones aprendidos con Golon.
- `ingenieria-fiable`: adaptación práctica para planificar, diagnosticar, probar y verificar software, agentes y automatizaciones.
- `bibliotecario-memoria`: recuperación y registro conservador de hitos del Bibliotecario en Debian, sin asumir ejecución automática entre chats.

## Nueva metodología
Inspirada en principios generales de Superpowers de Jesse Vincent (MIT): https://github.com/obra/superpowers . Se conserva atribución al proyecto de referencia. Esta adaptación se ha redactado para ChatGPT; no contiene scripts remotos, hooks de arranque, autorizaciones globales, instalación automática, subagentes obligatorios ni permisos de escritura adicionales.

## Seguridad y costes
Presupuesto por defecto: cero euros. Una skill no confiere herramientas ni permisos. Las acciones externas y cualquier uso facturable necesitan aprobación expresa y verificación. El manifiesto sigue declarando solo `Read`.

## Alcance de las pruebas
Las pruebas de este paquete validan estructura y consistencia; no demuestran acceso a portales, autonomía de GitHub Actions ni ejecución real de un programa de terceros. Requiere verificación independiente al aplicarlo a cada proyecto.

## Empaquetado reproducible

El empaquetador obtiene un commit exacto, valida los manifiestos y las nueve skills, y genera un ZIP determinista para Plugin Creator. El ZIP contiene únicamente `.codex-plugin/plugin.json`, `README.md` y `skills/`; el marketplace de Codex se valida, pero no se entrega a Plugin Creator. No se reescriben los archivos originales.

```powershell
$commit = git rev-parse HEAD
python scripts/package_plugin.py --commit $commit --output "dist/gestor-de-skills-0.4.33.zip"
python -m unittest discover -s tests -v
```

También se crea `dist/gestor-de-skills-0.4.33.zip.sha256.json`, que registra el commit, la versión y los SHA-256 del ZIP y de cada archivo incluido. `dist/` es un artefacto local y no debe incorporarse al repositorio.

### Publicación y verificación

1. Confirmar que el commit está publicado en `vtsalamanca/gestor-de-skills` y ejecutar las pruebas sobre ese SHA completo.
2. Leer el plugin privado existente en Plugin Creator y anotar su identificador y `release_id` actual.
3. Actualizar ese mismo plugin con el ZIP y el `release_id` esperado; no crear otro plugin.
4. Volver a leer los archivos publicados y comprobar versión, nueve skills y contenido frente a los hashes generados.
5. En Codex, actualizar el marketplace `gestor-de-skills-github` y comprobar la versión instalada y la ruta cargada. Un commit en GitHub no demuestra por sí solo que ChatGPT o Codex estén sincronizados.

### Recuperación

Conservar fuera de Git el ZIP y el informe de hashes de la versión anterior. Si una publicación falla, no se cambia la release activa. Si una release ya publicada debe deshacerse, se vuelve a empaquetar el contenido del commit anterior con una versión nueva superior, se publica sobre el mismo plugin privado y se repiten las verificaciones; no se fuerza una regresión de versión ni se crea una identidad distinta.


## Publicación autenticada y recuperación
Para actualizar el plugin privado con el empaquetador reproducible, seguir `skills/ingenieria-fiable/references/actualizar-skills.md`. Incluye transferencia correcta entre Desktop Commander, host del publicador, release ID y verificación real. No entregar una ruta de Windows directamente a Plugin Creator.
