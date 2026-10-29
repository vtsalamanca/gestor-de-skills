# Gestor de Skills 0.4.38

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
python scripts/package_plugin.py --commit $commit --output "dist/gestor-de-skills-0.4.37.zip"
python -m unittest discover -s tests -v
```

También se crea `dist/gestor-de-skills-0.4.37.zip.sha256.json`, que registra el commit, la versión y los SHA-256 del ZIP y de cada archivo incluido. `dist/` es un artefacto local y no debe incorporarse al repositorio.

### Publicación y verificación

**Antes de iniciar los pasos de catalogación, respaldo, empaquetado o publicación, obtener la autorización específica que exige el protocolo de inventario y resguardo.** No se deduce del permiso de desarrollo. La solicitud actual de instalar esta norma constituye aprobación de esa instalación inicial, no de futuras actualizaciones.

1. Confirmar que el commit está publicado en `vtsalamanca/gestor-de-skills` y ejecutar las pruebas sobre ese SHA completo.
2. Leer el plugin privado existente en Plugin Creator y anotar su identificador y `release_id` actual.
3. Actualizar ese mismo plugin con el ZIP y el `release_id` esperado; no crear otro plugin.
4. Volver a leer los archivos publicados y comprobar versión, nueve skills y contenido frente a los hashes generados.
5. En Codex, actualizar el marketplace `gestor-de-skills-github` y comprobar la versión instalada y la ruta cargada. Un commit en GitHub no demuestra por sí solo que ChatGPT o Codex estén sincronizados.

### Recuperación

Conservar fuera de Git el ZIP y el informe de hashes de la versión anterior. Si una publicación falla, no se cambia la release activa. Si una release ya publicada debe deshacerse, se vuelve a empaquetar el contenido del commit anterior con una versión nueva superior, se publica sobre el mismo plugin privado y se repiten las verificaciones; no se fuerza una regresión de versión ni se crea una identidad distinta.


## Publicación autenticada y recuperación
Para actualizar el plugin privado con el empaquetador reproducible, seguir `skills/ingenieria-fiable/references/actualizar-skills.md`. Incluye transferencia correcta entre Desktop Commander, host del publicador, release ID y verificación real. No entregar una ruta de Windows directamente a Plugin Creator.


## Inventario de habilidades, MCP y control de Debian (29/10/2026)

Nueve skills canónicas, sin crear otra duplicada. [Inventario ampliado del control de Debian](skills/inventariar-skills/references/inventario-control-debian-2026-10-29.md): Open Computer Use, Firefox DevTools MCP/Marionette, Codex CLI, CDC, GitHub Actions a demanda y Piper. Contiene versiones, diferencias entre instalado/validado, límites de permisos y **cuota de Codex frente a coste monetario**.

En el equipo Debian, el catálogo humano de herramientas ejecutables está en `/home/labgestor/utilidades/CATALOGO - Herramientas del laboratorio.md`, dentro de «Documentos → Centro de recursos → 02 - Caja de utilidades».

**Regla de cierre (29/10/2026):** después de implantar o verificar una herramienta, pasarela o habilidad nueva, **detectar proactivamente la necesidad de catalogación y resguardo en las mismas situaciones que antes, pero pedir autorización expresa antes de escribir, copiar o publicar**. Agrupar la solicitud por lote (elementos, destinos, costes/cuotas); con aprobación, ejecutar y verificar en el mismo flujo, y sin ella dejar pendiente en el chat sin modificar ningún registro. No esperar recordatorios de detección ni crear automatizaciones adicionales. `organizaciondeltrabajo` 0.2.21, `bibliotecario-memoria` 0.3.4 y el [protocolo canónico](skills/inventariar-skills/references/autorizacion_catalogacion_y_resguardo.md) regulan esta autorización.

## Inventario de herramientas de acceso web (27/10/2026)

Catálogo verificable: [inventario de acceso web](skills/inventariar-skills/references/inventario-acceso-web-2026-10-27.md).
Procedimiento técnico general: [navegadores, llavero y OAuth](skills/acceso_webs/references/sesiones-navegador-llavero-oauth.md).
Son instrucciones y resultados observados, no claves ni permisos de acceso. Publicar una skill no instala las herramientas en otro equipo ni convierte un login pendiente en una autenticación verificada.

### Ejecutor local sin Codex (29/10/2026)

El puente privado GitHub→CDC mantiene el disparo por eventos, pero los diagnósticos conocidos `list_apps` y `list_firefox_pages` pasan por Open Computer Use y Firefox DevTools MCP directamente, **sin llamadas a Codex ni a la API OpenAI**. El resultado real de issues privados #10 y #11 indica `executor: local_mcp`, `ok:true`; el CDC está íntegro y el temporizador desactivado. El servicio externo GitHub sigue siendo necesario para enviar trabajos desde ChatGPT. Inventario técnico: `skills/inventariar-skills/references/inventario-control-debian-2026-10-29.md`. No atribuir a este piloto escrituras ni control del Firefox personal.

### Diagnósticos de salud a demanda sin Codex (29/10/2026)

La misma vía privada GitHub→CDC admite ahora `status_services` y `status_cdc`, además de las dos consultas MCP previas. Las peticiones reales #13 y #14 concluyeron con `ok:true`, `executor:local_mcp`, sin Codex. El segundo diagnóstico consulta SQLite solo en lectura y el primero conoce tres servicios fijos; ambas operaciones evitan comandos suministrados por el remitente. Véase `skills/inventariar-skills/references/inventario-control-debian-2026-10-29.md`.
