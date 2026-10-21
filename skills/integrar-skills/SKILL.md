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
