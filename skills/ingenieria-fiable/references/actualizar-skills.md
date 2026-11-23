# Actualización canónica vigente — Gestor de Skills

**Vigencia:** 23/11/2026, once habilidades. El procedimiento principal verificado está en [publicacion-autonoma-complemento.md](publicacion-autonoma-complemento.md). El [índice operativo](../../control-laboratorio/references/20-indice-operativo.md) selecciona el punto de entrada; nunca seguir un historial sin comprobar vigencia.

## Regla vigente de autorización
Esta regla tiene **prioridad sobre las instrucciones históricas** y exige aprobación específica para catalogación, resguardo y distribución; se reutiliza la autorización ya concedida para este lote.

1. **Permiso y coste:** obtener autorización específica para modificación, catalogación, resguardo y distribución de este lote. Coste marginal 0 €, salvo consentimiento separado. No publicar si falla seguridad o preflight.
2. **Fuente y conflictos:** comprobar GitHub y checkout Debian, preservar cambios locales ajenos mediante rama/worktree. Consultar la release privada actual antes de editar; no crear otro plugin.
3. **Cambios y pruebas:** ajustar solo archivos afectados, versiones de cada skill (cuando existan), los dos manifiestos y el README. Ejecutar tests, enlaces, seguridad y escenarios de enrutamiento. No equiparar L0 estático con activación E2E.
4. **Publicación GitHub:** generar commit desde contenido revisado con GitHub autenticado, mantener HEAD anterior y verificar SHAs; reconciliar Debian sin descartar modificaciones locales.
5. **Paquete desde el commit exacto:** usar `scripts/package_plugin.py`; ZIP contiene once skills, manifest V2, README y referencias, **sin marketplace dentro**. Verificar checksum, inventario y `scripts/preflight_plugin_upload.py`.
6. **Transferencia autónoma:** preferir artefacto subido al host de ChatGPT o el puente GitHub Actions → referencia binaria compatible, con hashes verificados. Una ruta Debian/Windows o base64 no es por sí misma un archivo host-uploaded. No exigir al usuario adjuntar ni copiar ZIP mientras exista la vía probada.
7. **Release privada con control de concurrencia:** comprobar USER/PRIVATE, obtener `current_release_id` actual y ejecutar una sola actualización sobre el plugin existente con `expected_release_id`. Ante respuesta incierta, releer antes de repetir.
8. **Postflight:** verificar nueva versión, identidad, 11 habilidades, archivos modificados y privacidad por lectura de la release. Registrar por separado GitHub, ZIP, transferencia, plugin, Codex y prueba en chat nuevo. No atribuir recarga al chat ya abierto.
9. **Registro:** guardar hito idempotente en Bibliotecario y confirmar revisión mediante relectura; anotar estado real y reversión.

Los procedimientos reemplazados se conservan exclusivamente en [actualizar-skills-historico.md](actualizar-skills-historico.md). No usar allí cifras históricas ni instrucciones de intervención manual como referencia actual.
