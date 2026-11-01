# Estado y continuidad de Control Debian y puente GitHub (01/11/2026)

**Anexo aditivo:** no sustituye ni corrige retrospectivamente [inventario 29/10](inventario-control-debian-2026-10-29.md). Responsable: `inventariar-skills`. Autorización explícita del usuario para catalogar habilidades, herramientas y Bibliotecario, con preservación del puente GitHub.

## Estado contrastado
| Ruta/componente | Evidencia | Estado | Limitación |
|---|---|---|---|
| MCP Control Debian v5 | 37 tools y túnel en Plus; filesystem/GUI acotados | verificado E2E histórico | No equivalencia completa de Desktop Commander |
| MCP stdio-v7 | #777 338 tests OK; #778 instalador verificado; #779 handshake 38 herramientas; #780 preflight; #781 cambio de servicio | **activo desde Plus**, `debian_estado` anuncia `stdio-v7`, 38 | Esta sesión anterior solo exponía 37; operación nueva de lotes aún no probada desde chat fresco |
| Reconexión v7 | `debian_estado_reconexion`: wrapper y perfil v7 reconocidos, credenciales no exportadas | verificado después de reiniciar el servicio | Reinicio completo Debian posterior a v7 aún pendiente |
| Diagnóstico Firefox corregido | PR #782 + #784; regresión #785 341 tests OK | fuente `main` validada | Fix todavía no incorporado en directorio inmutable v7 en ejecución |
| Operaciones archivos | leer/escribir/editar por hash, copiar y consultar SHA; mover/borrar de prueba acreditados en fases previas | E2E parcial | escritura sólo en `bridge-workspace`; límites de tamaño/formato |
| GUI X11 | geometría/enfoque/teclado acotado, capturas PNG y SHA sin píxeles exportados | E2E parcial | movimiento/redimensión real no acreditados |
| Terminal y procesos | Bubblewrap sin HOME ni red; proceso listados del propio usuario | aislada verificable | **no** consola anfitrión; no gestión universal de procesos |
| GitHub privado → Issues/Actions → runner Debian → CDC/ejecutor local | repositorio `vtsalamanca/prueba-work-puente-local`; flujo E2E histórico y servicio `github-actions-cdc-ondemand.service` visto activo el 01/11; workflows `cdc-debian-ondemand.yml`, `cdc-debian-v2.yml` presentes | **conservar como respaldo independiente** | Depende de GitHub; la ruta normal usa túnel privado |
| Gestor de Skills | fuente `vtsalamanca/gestor-de-skills`, 9 skills; antes de esta revisión release 0.4.38 | actualización documental propuesta 0.4.39 | distribución debe verificarse independientemente |
| Bibliotecario Debian | trabajos existentes de homologación y gestor recuperados por título; identificadores mantenidos únicamente en Bibliotecario privado | conservar y añadir nuevos hitos no duplicados | el catálogo v7 no ofrece API general al Bibliotecario; puente GitHub tiene allowlist de un expediente narrativo; usar acceso local autorizado |

## Restauración: preservar por diseño
- Fuente GitHub canónica del código del puente: `vtsalamanca/prueba-work-puente-local`, repositorio **privado**. No borrarlo, no sustituir los workflows por el túnel, ni tocar claves/tokens locales. En la máquina se verificó un servicio receptor de eventos GitHub activo.
- En Debian: `/home/labgestor/proyectos/tutorial-generico/control-debian/resguardo-control-debian-github-20261101/`. Contiene copia preexistente del catálogo, `git archive` de 169 archivos rastreados sin `.git` y `manifest.json` con SHA-256; commit de código conservado: `5ab9a3a992c7747a6537063636f5969004406b2f`.
- Directorios previos MCP v3, v4, v5 y v6 no se deben destruir; rollback v5 permanece preparado. Versiones anteriores del plugin de skills no se eliminan.
- Backup es una copia **de archivos rastreados en Git**, no respaldo de credenciales, base SQLite ni estado de servicios. No atribuir a ella capacidad de recuperación completa sin verificar componentes externos.
- No tocar expedientes personales o narrativos para alojar catálogo técnico. Permisos de archivos temporales y copias son privados; presupuesto adicional autorizado 0 €.

## Pruebas y siguientes criterios
- Ejecutar `debian_consultas_lote` sólo cuando aparezca en un chat nuevo con catálogo 38; comprobar datos sintéticos y límites, no aceptar mera presencia del nombre.
- Integrar corrección X11 mediante un futuro runtime **versionado** y tests de regresión, sin modificar v7 inmutable ni afectar a otros perfiles.
- Control de procesos anfitrión, archivos grandes y transferencia de imágenes visibles siguen pendientes de diseño y autorización granular.
- Para cambios de habilidades: comparar fuente, tests, ZIP y release de Plugin Creator. No decir actualizado en ChatGPT por un commit en GitHub; ni suponer actualización de Codex.
