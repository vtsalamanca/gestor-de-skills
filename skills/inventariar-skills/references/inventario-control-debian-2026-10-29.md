# Inventario del control de Debian y nuevas capacidades (29/10/2026)

**Fuente canónica:** `vtsalamanca/gestor-de-skills` · responsable de catálogo: `inventariar-skills`. Complementa [inventario de acceso web (27/10)](inventario-acceso-web-2026-10-27.md), sin sustituir su registro histórico.

## Habilidades del paquete y su relación con el nuevo sistema

| Skill canónica | Papel en el laboratorio | Mejora de uso registrada |
|---|---|---|
| `organizaciondeltrabajo` | Priorizar recursos, reducir consumo de cuota y esfuerzo del usuario | **Puerta de actualización del catálogo** al incorporar una herramienta/skill o acreditar un nuevo flujo. Programar por eventos cuando exista, evitar temporizadores si es posible |
| `inventariar-skills` | Inventario, versiones, permisos, evidencia y no duplicación | Mantener este registro y el catálogo humano de la Caja de utilidades de Debian |
| `ingenieria-fiable` | Diagnóstico, regresión, pruebas extremo a extremo | Incorporar verificación de catálogo y coste/cuota en la fase de cierre, sin convertir instalación en éxito aparente |
| `acceso_webs` | Navegadores, sesiones, WebDriver, llavero, OAuth | Consultar Marionette y Firefox DevTools MCP antes de crear control gráfico propio |
| `integrar-skills` | Alcance de Chat/Work/Codex/MCP y distribución | Asegurar que MCP local no se atribuye a chat web sin vía de conexión real |
| `auditar-skills` | Permisos, riesgo y licencias | Revisar seguridad de runner autohospedado y tareas del repositorio, evitar ejecución de entrada arbitraria |
| `crear-skills` | Diseño de skills propias | Preferir actualizar skill transversal existente antes de crear otra con función duplicada |
| `descubrir-skills` | Buscar alternativas existentes | Registrar Open Computer Use y Firefox DevTools MCP antes de ampliar búsqueda |
| `bibliotecario-memoria` | Conservar el estado, evidencias y trazabilidad | Mantener la separación entre registro local y respuesta de otro chat, registrar resultado real y límites |

**No se crea una décima skill de control de Debian:** estas capacidades pertenecen a herramientas reutilizables y procedimientos ya cubiertos por las nueve skills. Una skill no instala un MCP, no se ejecuta por estar mencionada y no elude controles de seguridad.

## Componentes comprobados

| Componente | Versión | Resultado observado | Pendientes y riesgos | Coste |
|---|---:|---|---|---|
| Open Computer Use MCP, AT-SPI/X11 | 1.3.0 | `list_apps` invocado directamente mediante `ocu` en petición privada #10 `ok:true`, sin Codex; `get_app_state` validado | Escritura, clic y teclado real aún no verificados en este chat | Local sin tarifa |
| Mozilla Firefox DevTools MCP + Marionette | 0.10.7 | SDK Node local llamó `list_pages` en Firefox aislado; petición privada #11 `ok:true`, URL `https://example.org/` | No se ha probado `--connectExisting` con Firefox personal | Local sin tarifa |
| GeckoDriver / Firefox | 0.37.1 / ESR 153.5 | Binario y WebDriver disponibles; MCP Mozilla lista acciones de página, captura y entrada | No inferir control del Firefox personal | Sin tarifa local |
| Codex CLI | 0.165.0 | Conservado como herramienta optativa de programación compleja; historial #8 y #9 acreditado | Ya no participa en peticiones ordinarias #10 y #11; consume cuota al invocarlo | Cuota ChatGPT, API aparte no contratada |
| GitHub CLI | 2.103.2 | Autenticación de repositorio privado, issues, comentarios y registro del runner | Credenciales privadas, rotación y control de acceso | Servicio GitHub sujeto a condiciones |
| GitHub Actions self-hosted runner | 2.338.2 | `debian-cdc-demanda` online; activó E2E directo #10 y #11 | No es sandbox. Solo el repositorio privado autoriza cambios en workflows | Sin coste de minutos autohospedados observado; servicio externo GitHub |
| Puente GitHub→CDC→MCP local | versión piloto 29/10 | `github_cdc_bridge.py`: autor/título/JSON y leases de SQLite; llama a `local_mcp_executor.py`, nunca a Codex; publica `executor: local_mcp` | **E2E #10 y #11**; lista cerrada de dos operaciones, salida minimizada, no comandos arbitrarios | GitHub sin cuota de modelo para esas tareas |
| CDC 1.0 | producción local | `cdc_v1_doctor.py`: `ok:true`, integridad `ok`; pruebas de coordinación anteriores | No despierta conversaciones nativas de ChatGPT cerradas | SQLite local sin tarifa |
| Bridge Piper/PulseAudio y extensión | configuración local | Audio audible confirmado por el usuario tras recuperación de PulseAudio; activación de botón lectora | Lectura real de mensajes nuevos en Firefox no acreditada; complemento temporal no persiste | Síntesis local sin tarifa |
| Desktop Commander | plugin actual | Control de archivos y terminal en Debian; usado para la instalación | Cuota de llamadas; teclado gráfico limitado por controles; no forma parte de la ejecución a demanda | Consultar cuotas |
| Ejecutor MCP directo sin Codex | **IMPLEMENTADO** 29/10 | `local_mcp_executor.py` llama a `ocu call list_apps` y a `mcp_firefox_pages.mjs` (SDK Firefox MCP); peticiones #10 y #11 `ok:true` | **E2E_VERIFICADO**; lectura únicamente, en Firefox aislado; pruebas de rechazo, no exposición de títulos ni claves API | **0 llamadas Codex en el camino de ejecución** |

## Decisiones de ingeniería reutilizables

1. **Eventos en lugar de sondeo:** workflow `issues.opened` en repositorio GitHub privado, receptor `github-actions-cdc-ondemand.service`, sin abrir puertos; el temporizador `github-cdc-codex.timer` se desactivó.
2. **Separación del transporte y razonamiento:** GitHub solamente avisa; CDC valida el número, recupera la solicitud y registra idempotencia; Codex se reserva para razonamiento complejo; las dos consultas actuales se resuelven ya directamente por MCP en los issues #10 y #11, sin modelo.
3. **Resultados exactos:** las peticiones #5 y #6 llegaron pero terminaron `ok:false` por `node` ausente en PATH del servicio; se corrigió. Las peticiones #7, #8 y #9 dieron `ok:true` usando Codex; #10 y #11 dieron `ok:true` usando `executor: local_mcp` sin Codex. Todas las #8–#11 fueron activadas por evento sin temporizador.
4. **Reinicio:** runner habilitado en `systemd --user` y `Linger=yes`, pero la prueba posterior a un reinicio real sigue **pendiente**.
5. **Superficie de seguridad:** no permitir prompts de issues, scripts arbitrarios, clics, compras, cambios de contraseñas o acciones privilegiadas por el simple hecho de que el emisor controla el repositorio. Limitar workflow y perfiles, mantener repositorio privado.
6. **Tarifas reales:** distinguir cero euros incrementales de **cuota de Codex consumida en otros trabajos**; las tareas MCP directas no usan dicha cuota, pero siguen dependiendo de GitHub y de sus condiciones y posibilidad de cambios de tarifa; no etiquetar «gratis» a todo el recorrido.

## Evidencia E2E del ejecutor sin Codex (29/10/2026)

- Solicitud privada #10: `list_apps`, `ok:true`, `executor: local_mcp`, lectura de cinco nombres de aplicaciones; workflow GitHub Actions `completed/success`.
- Solicitud privada #11: `list_firefox_pages`, `ok:true`, `executor: local_mcp`, URL pública de ensayo `https://example.org/`; workflow GitHub Actions `completed/success`.
- Python `local_mcp_executor.py`, Node `mcp_firefox_pages.mjs`, pruebas `test_local_mcp_executor.py`, `test_github_cdc_bridge.py`, `github_cdc_bridge.py selftest`.
- `cdc_v1_doctor.py` informa `ok:true`, integridad de base `ok`, sin issues; el timer permanece desactivado.
- **Seguridad:** salida de Open Computer Use restringida a nombres de aplicaciones (sin títulos de ventana ni PID); Firefox solo permite URL de la página pública fija en perfil separado. No aceptar texto arbitrario del issue como comando.

## Ubicaciones operativas, sin credenciales

- Catálogo humano permanente: `/home/labgestor/utilidades/CATALOGO - Herramientas del laboratorio.md`.
- Código y pruebas de piloto: `/home/labgestor/proyectos/tutorial-generico/control-debian/`.
- CDC canónico: `/home/labgestor/proyectos/comunicacion-chats/`.
- Fuente de las nueve skills: `/home/labgestor/proyectos/gestor-de-skills/skills/`.
- Workflow: `vtsalamanca/prueba-work-puente-local/.github/workflows/cdc-debian-ondemand.yml` (repo privado).
- Fuente de evidencia técnica local: `/home/labgestor/proyectos/tutorial-generico/control-debian/README.md`.

## Puerta de actualización del catálogo (nueva obligación de cierre)

**Disparador:** creación, instalación, desinstalación, actualización o verificación nueva de herramienta/MCP, protocolo, conector, habilidad, servicio o integración; no aplica a respuestas triviales.

1. Antes: leer índice de habilidades y herramientas existente; comprobar nombre, versión, equipo y permisos, decidir si reutilizar.
2. Después: en la **misma tarea**, actualizar ficha de herramienta **y** referencia de skills relacionada, distinguiendo instalado/local/E2E/bloqueado y registrando coste monetario, cuota, evidencias y riesgos.
3. Verificación: releer archivos, validar enlaces/rutas/versiones, ejecutar pruebas pertinentes; no afirmar que el plugin de skills está actualizado por modificar el repositorio.
4. Distribución: para skills canónicas seguir publicación controlada en el complemento privado existente y verificar la versión; si falla, informar del estado exacto.
5. Estado del proyecto: registrar fecha, causa de no actualizar si se excluye y siguiente paso. No crear servicio/timer para esta revisión: es una condición de cierre de cada trabajo, no una promesa de ejecución fuera del chat.

**Estados:** DOCUMENTADO / INSTALADO / VERIFICADO_LOCAL / VERIFICADO_E2E / PENDIENTE / BLOQUEADO / RETIRADO. No almacenar tokens, cookies, contraseñas ni contenido privado de otras conversaciones.
