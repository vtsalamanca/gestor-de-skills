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
| Open Computer Use MCP, AT-SPI/X11 | 1.3.0 | Codex utilizó `list_apps`; petición privada GitHub #9 `ok:true`; `get_app_state` validado contra XFCE | Escrituras, clic y teclado de Firefox habitual no validados | MIT, local sin tarifa de llamada |
| Mozilla Firefox DevTools MCP + Marionette | 0.10.7 | `list_pages` en sesión headless de prueba; petición privada #8 `ok:true` con `https://example.org/` | Conexión a Firefox personal `--connectExisting` no verificada | Sin tarifa de operación local |
| GeckoDriver / Firefox | 0.37.1 / ESR 153.5 | Binario y WebDriver disponibles; MCP Mozilla lista acciones de página, captura y entrada | No inferir control del Firefox personal | Sin tarifa local |
| Codex CLI | 0.165.0 | Ejecutó MCP Debian y Mozilla y respondió con ChatGPT; sesión existente autenticada | Consume cuota del plan; no emplear en tareas de lectura determinista si basta llamar directamente al MCP | Suscripción/cuota; API aparte no contratada |
| GitHub CLI | 2.103.2 | Autenticación de repositorio privado, issues, comentarios y registro del runner | Credenciales privadas, rotación y control de acceso | Servicio GitHub sujeto a condiciones |
| GitHub Actions self-hosted runner | 2.338.2 | `debian-cdc-demanda` online; ejecuciones #8 y #9 `completed/success` | Runner tiene acceso al host; NO es sandbox. No activar workflows no confiables | Minutos self-hosted sin coste adicional observado; dependemos de GitHub |
| Puente local GitHub→CDC→Codex | versión piloto 29/10 | Restringe JSON/autor/título, controla leases SQLite, ejecuta `list_apps` o `list_firefox_pages`, publica resultado | Solo dos operaciones permitidas; identidad de alias local, no de chat Instant | GitHub + cuota Codex |
| CDC 1.0 | producción local | `cdc_v1_doctor.py`: `ok:true`, integridad `ok`; pruebas de coordinación anteriores | No despierta conversaciones nativas de ChatGPT cerradas | SQLite local sin tarifa |
| Bridge Piper/PulseAudio y extensión | configuración local | Audio audible confirmado por el usuario tras recuperación de PulseAudio; activación de botón lectora | Lectura real de mensajes nuevos en Firefox no acreditada; complemento temporal no persiste | Síntesis local sin tarifa |
| Desktop Commander | plugin actual | Control de archivos y terminal en Debian; usado para la instalación | Cuota de llamadas; teclado gráfico limitado por controles; no forma parte de la ejecución a demanda | Consultar cuotas |
| Ejecutor MCP directo sin Codex | pendiente | **No implementado** | Propuesta de ahorro de cuota; exigir pruebas y seguridad antes de promover | Sin coste de modelo si se implementa |

## Decisiones de ingeniería reutilizables

1. **Eventos en lugar de sondeo:** workflow `issues.opened` en repositorio GitHub privado, receptor `github-actions-cdc-ondemand.service`, sin abrir puertos; el temporizador `github-cdc-codex.timer` se desactivó.
2. **Separación del transporte y razonamiento:** GitHub solamente avisa; CDC valida el número, recupera la solicitud y registra idempotencia; Codex se reserva para razonamiento no determinista. Las dos consultas actuales podrían resolverse directamente por MCP, **pero todavía no está implementado**.
3. **Resultados exactos:** las peticiones #5 y #6 llegaron pero terminaron `ok:false` por `node` ausente en PATH del servicio; se corrigió. Las peticiones #7, #8 y #9 dieron `ok:true`; #8 y #9 se ejecutaron con aviso de GitHub sin temporizador.
4. **Reinicio:** runner habilitado en `systemd --user` y `Linger=yes`, pero la prueba posterior a un reinicio real sigue **pendiente**.
5. **Superficie de seguridad:** no permitir prompts de issues, scripts arbitrarios, clics, compras, cambios de contraseñas o acciones privilegiadas por el simple hecho de que el emisor controla el repositorio. Limitar workflow y perfiles, mantener repositorio privado.
6. **Tarifas reales:** distinguir cero euros incrementales de **cuota de Codex consumida**, dependencia de servicios externos y posibilidad de cambios de tarifa; no etiquetar «gratis» a todo el recorrido.

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
