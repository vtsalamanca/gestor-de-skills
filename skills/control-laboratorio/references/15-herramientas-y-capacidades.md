# Herramientas, conectores, funciones MCP y selección operativa

## Inventario individual en Debian
La lista completa de **cada función MCP de la sesión observada** está en el fichero local de Debian, no se congela aquí. Consultar [17-inventario-operativo.md](17-inventario-operativo.md) para conocer las rutas, el generador, los cambios entre capturas y las pruebas limitadas por operación. Verificar siempre el catálogo disponible en este chat y los permisos reales antes de actuar.

## Inventario dinámico, no listado fijo
Las capacidades de un chat cambian con el plugin, permisos, modelo, entorno y versión del servidor. Enumerar funciones realmente expuestas en la sesión y verificar su descripción/esquema antes de llamar. Los identificadores aquí son orientativos porque el MCP puede renombrar herramientas: nunca inventar un argumento por parecido. Consultar además inventariar-skills y el catálogo local actualizado.

## Grupos de herramientas de Control Debian — Sustituto independiente
| Familia observada | Función típica | Verificación / precaución |
|---|---|---|
| debian_laboratorio_iniciar + debian_laboratorio_resultado | operaciones fijas de estado, componentes, InfoJobs y Educamos | ticket, resultado real, fecha; no exponer secretos |
| debian_lab_command_approve_on_desktop | terminal anfitrión Debian del usuario sin root bajo revisión/autorización local | cwd/timeout/exit code y postcondición; no asumir arbitrario ni desatendido |
| debian_host_connection_health / debian_host_runtime_config / debian_host_process_list | diagnóstico saneado de conexión, configuración y procesos | comparar con otra ruta real; no confundir canal histórico con canal conectado |
| debian_terminal_sandbox_* | consola de pruebas limitada | no tiene el HOME completo ni permisos anfitrión |
| debian_project_workspace_* y debian_project_source_* | ficheros/fixtures y lectura de espacio revisado | rutas y límites; no equivalen a acceso libre a / |
| debian_project_text_* | edición textual condicionada en workspace revisado | hash anterior y allowlist; no sustituye edición genérica de código |
| debian_gui_fixture_* y debian_gui_mousepad_* | pruebas gráficas inofensivas | propiedad de ventana, foco y limpieza |
| debian_gui_writer_* y debian_gui_calc_* | pruebas de Writer/Calc con fixtures | verificar contenido; no modificar documentos reales sin pedido |
| debian_gui_selected_* y debian_gui_owned_* | capturas/gestos de ventana seleccionada o propia | algunas rutas pueden rechazar gestos: diagnosticar, no insistir |
| read_file/write_file/start_process y similares | interfaz genérica anunciada en algunos catálogos | puede devolver Operation unavailable or denied; probar solo si alcance documentado |

**Criterio de uso:** primero la función tipada de menor privilegio; después la consulta revisada de usuario. El éxito de una herramienta no equivale al éxito del caso de negocio. No usar nombres de herramientas que no aparezcan en la sesión.

## Herramientas externas al MCP
- **GitHub conectado:** consultar repo/commit/archivo, crear rama/árbol/commit/PR, fusionar con guardas y validar SHA; GitHub público no es bóveda privada.
- **Plugin Creator:** obtener metadata, listar y leer contenido del plugin, actualizar el mismo plugin con release esperada y archivo host-uploaded; verificar postpublicación.
- **Automations ChatGPT:** inspeccionar programación, último resultado y entrega. La ejecución solicitada «ahora» no prueba entrega desatendida.
- **Gmail y calendario cuando estén conectados:** solo acceder si corresponden al encargo, sin reemplazar LAB-AUTH local para un portal donde ya existe un flujo probado. No asumir capacidad de acciones o acceso sin verificar permisos.
- **Navegador conectado y herramientas web:** preferir conectores específicos o API autorizada; para páginas protegidas consultar acceso_webs. Work/Codex son modos con disponibilidad/cuota propias, no poderes que una skill active.
- **Archivos, biblioteca de usuario y documentos:** usar herramientas nativas por tipo (PDF, DOCX, spreadsheet, slides) y leer el archivo original antes de transformar; evitar extraer información privada fuera del alcance solicitado.

## Herramientas instaladas en Debian
- **Python, Git, Bash, systemd de usuario:** verificar ejecutable real, versión y cwd. Scripts locales se ejecutan únicamente cuando el usuario ha encargado esa operación y se ha revisado su alcance.
- **BrowserLearn local 0.1.0 (variante auditada Debian):** `browserlearn-lab` y `browserlearn-lab-browser` para grabación manual de recorridos web en Chromium independiente; datos locales privados, sin servicio permanente ni IA externa. Comprobar `$HOME/proyectos/browserlearn-local/LAB-SEGURIDAD.md` y `acceso_webs/references/browserlearn-laboratorio.md`. Permisos amplios HTTP/HTTPS de la extensión en ese perfil: usar solo con autorización, nunca trasladar el perfil al plugin. **Herramienta local, no MCP anunciado ni skill duplicada.**
- **Firefox ESR, GeckoDriver, AT-SPI, X11, Mousepad, Writer, Calc:** presencia física y permisos GUI se comprueban, no se infieren del README.
- **GNOME Keyring y Credenciales del laboratorio:** solo metadatos y uso local autorizado; los secretos nunca pasan a otras herramientas.
- **Thunderbird LAB-AUTH:** instalación aislada fuera de PATH, perfil OAuth persistente; su presencia no acredita acceso a Gmail actual ni OTP válido.
- **CDC, Igor, Goose, Ollama y otros clientes:** distinguir binario, proceso, modelo, cuota, canal y respuesta real; no instalar o activar modelos remotos facturables por impulso.
- **CUPS/IPP y utilidades multimedia:** identificar dispositivos, colas, drivers y servicios actuales. Una llamada aceptada no acredita salida física o reproducción.

## Herramientas que no deben utilizarse por inercia
Desktop Commander cuando Control Debian está operativo; navegadores o scraping duplicados para una consulta que un colector ya cubre; Groq/Grok/otros APIs cuyo coste por operación no esté autorizado; automatizaciones nuevas para corregir informes con fallos puntuales; descargas de ejecutables y cambios de permisos para saltar bloqueos MCP.

## Criterios de elección
Evaluar legitimidad/autorización, disponibilidad, evidencia de fiabilidad, privacidad, reversibilidad, coste marginal y latencia. Usar recursos locales ya instalados; separar investigación de ejecución definitiva y comprobar cuotas antes de consumir runner/servicio externo.
