---
name: integrar-skills
description: Planifica cómo incorporar una skill en ChatGPT, Codex, Claude, un agente local o GitHub Actions; comprueba compatibilidad, permisos, validación y coste sin instalar sin aprobación.
---
# Integrar skills por entorno

## Ruta de integración
1. Identifica el destino real y comprueba si ya existe la capacidad. Distingue siempre ChatGPT (plugin privado/skills disponibles), Codex, agentes CLI locales y repositorios/workflows de GitHub.
2. Revisa previamente con `auditar-skills`; si el riesgo es alto o faltan archivos críticos, detener la instalación.
3. Identifica la variante más simple: instrucciones en una skill sin scripts; skill + referencias; plugin privado con varias skills; agente local; automatización GitHub Actions separada del archivo SKILL.md.
4. Prepara un plan en pasos con dependencias, permisos, ruta de configuración, pruebas sin coste y rollback. No prometas que Skills.sh se instala automáticamente en ChatGPT.
5. Antes de cambiar archivos, publicar, instalar, habilitar tareas, crear tokens, conectar cuentas o ejecutar instaladores, solicita aprobación explícita. Si la autorización ya está clara en el contexto, reutilízala solo dentro del alcance concedido.
6. Tras un cambio autorizado, verifica presencia de archivos, identificación de versión, capacidad de lectura, prueba mínima inofensiva y comportamiento de retorno a versión anterior.

## Publicación del Gestor de Skills: procedimiento obligatorio
Cuando el objetivo sea actualizar nuestras skills en el plugin privado existente, **antes de generar, transferir o publicar un ZIP**, leer y seguir `skills/ingenieria-fiable/references/actualizar-skills.md` en GitHub (versión canónica). No reconstruir un procedimiento ad hoc ni trasladar el problema al usuario por defecto.

Especialmente: (1) leer versión, commit y release activos; (2) ejecutar el empaquetador del **commit actual**, no una copia local obsoleta; (3) distinguir ruta de Windows vía Desktop Commander de archivo que realmente pueda cargar Plugin Creator; (4) usar una vía de transferencia soportada, comprobando hash; (5) `update_plugin` del **mismo** plugin con `expected_release_id` vigente; (6) verificar por lectura los archivos de la nueva release, Codex y la carga en sesiones nuevas por separado. No repetir intentos idénticos tras un error.

No asumir que un error de transferencia indica que el empaquetador falla, ni que un plugin con versión igual ya contiene todos los cambios: cotejar archivos relevantes. Mantener la release anterior disponible para recuperación. Presupuesto adicional 0 €.

## Perfiles
**ChatGPT:** si se tiene permiso para editar el plugin existente, conserva ID, nombre, estructura y controles, modifica solo lo necesario, actualiza versión y verifica con lectura de archivos. No afirmes que ejecutar `npx skills add` añade una habilidad al plugin de ChatGPT.

**Codex/agentes locales:** verificar documentación del cliente, sistema operativo y ubicación correcta antes de ofrecer un comando. Inspeccionar primero y no ejecutar por defecto.

**GitHub Actions:** un `SKILL.md` por sí solo no ejecuta una tarea programada. La integración requiere workflow, código y mecanismo de entrega; credenciales siempre en secretos del repositorio. En público, runners estándar pueden estar incluidos; en privado hay cuotas y el uso adicional puede ser facturable. Runners grandes o APIs de terceros pueden generar cargos incluso en repositorio público. No iniciar trabajos si no está acreditado coste 0 para la operación.

## Entregables
Compatibilidad por entorno (confirmada / pendiente / incompatible), requisitos, arquitectura, pasos de instalación con aprobación pendiente, pruebas, coste marginal esperado y rollback. No repetir preguntas resueltas.

## Ruta de publicación del plugin privado comprobada
Tras modificar una skill del Gestor de Skills, aplicar el procedimiento de `ingenieria-fiable/references/actualizar-skills.md` **en el mismo encargo**. La ruta preferente demostrada el 22-10-2026 es ZIP reproducible → adjunto del chat montado en ruta verificada → `Plugin Creator.update_plugin` sobre ID existente con `expected_release_id` → relectura de archivos. No confundir archivo remoto de Windows/Debian con adjunto accesible al publicador. Preferir una carga directa solo si queda comprobada; si no, solicitar al usuario únicamente adjuntar el ZIP y continuar sin otra orden. Verificar la publicación, preservar privacidad y release anterior, y diferenciarla de la carga efectiva en otra conversación.


## Puente binario verificado: GitHub Actions → Plugin Creator (23-10-2026)
**Ruta preferente** para cambios en las ocho skills: GitHub `vtsalamanca/gestor-de-skills` es fuente canónica. Cada push a `main` que cambia `skills/**`, manifiesto, pruebas, empaquetador o workflow dispara `.github/workflows/prueba-puente-plugin.yml` en runner estándar `ubuntu-latest`, timeout 5 minutos, y genera un artefacto ZIP SIN DOBLE ENVOLTURA mediante `actions/upload-artifact@v7` y `archive: false`, retención 1 día.
1. Confirmar permiso/autorización de publicación, repo público y runner estándar; presupuesto extra 0 €. No crear runners grandes, endpoints de pago ni secretos. El workflow solo **empaqueta**, nunca publica automáticamente sobre el plugin.
2. Confirmar ejecución concluida y satisfactoria. Obtener ID de ejecución y de artefacto con conector GitHub `fetch_workflow_run_artifacts`. El ZIP se denomina según la versión del manifiesto. Confirmar que el SHA del artefacto coincide con el hash esperado del empaquetado canónico; que haya ocho skills, sin claves ni datos sensibles.
3. `download_workflow_artifact` devuelve referencia binaria y crea archivo montado en ChatGPT. Usar la ruta **exacta anunciada por la herramienta en la sesión activa**, jamás inventarla. No pasar ruta de Debian directamente a Plugin Creator ni tratar una URL de Drive como ZIP.
4. Obtener release actual con `Plugin_Creator.get_plugin_metadata`. `Plugin_Creator.update_plugin` con `plugin_id=plugins_6add39166308819193bc271cfa0af302`, `archive` apuntando a archivo montado comprobado y `expected_release_id` vigente. No crear plugin adicional.
5. Leer `get_plugin_files` después: versión correcta, ocho skills, soporte y manifiesto; distinguir publicación verificada de recarga efectiva de otras sesiones. Anotar nuevo release ID y mantener rollback. Si falla, preservar release vigente e informar `PUBLICACION_BLOQUEADA`.
6. Sin workflow concluido o sin referencia registrada, detener publicación, no probar rutas remotas repetidamente. No activar publicación automática sin control de cambios y de permisos.
**Prueba real:** workflow run `39876898171`; artifact `12467699397`; hash `af8a2ef92e7d9a2e03bf057a69411550de1720b88166e77aa1f18d841b28bf09`; Plugin Creator confirmó release `pluginrel_6adaa70f636881918703ea77cc60d33f` versión 0.4.22, 23 ficheros. Se mantiene la publicación como acción explícitamente autorizada, mientras que la creación del artefacto queda automatizada.