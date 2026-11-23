# Lecciones históricas de acceso web (no sustituyen el flujo vigente)

Consultar primero acceso_webs/SKILL.md y control-laboratorio/20-indice-operativo.md. La mención histórica a Windows/SSH o navegadores no concede permisos ni obliga a reutilizar ese mecanismo.

## Red de laboratorio aislada y acceso web (lección MCP-Debian, 2026-10-21)
En un entorno Debian host-only sin ruta externa, **no interpretar la falta de Internet como fallo de autenticación, DNS o scraping**. Comprobar primero `ip route`, `ip -6 route` y la ruta al destino, sin realizar reintentos web inútiles. Separar conectividad del anfitrión Windows y del invitado Debian. Si una investigación exige obtener información externa, preferir un conector web autorizado en ChatGPT o una descarga selectiva desde Windows con inspección de procedencia, licencia, tamaño y seguridad antes de trasladar archivos a Debian mediante SCP; no habilitar NAT, puente, proxy o reenvío sin autorización específica y nueva auditoría.

El control local mediante MCP → Windows → SSH es una **vía de ejecución**, no un método de autenticación web ni una capacidad de red adicional. No transportar cookies, contraseñas, tokens ni sesiones del navegador hacia la VM. Distinguir siempre aislamiento de red observado, acceso a servicios locales y posibilidad de reenvío por el anfitrión. Protocolo técnico en `ingenieria-fiable/references/mcp-local.md`.

## Conectividad entre entornos: lecciones comprobadas (octubre de 2026)

Además de acceso a páginas, aplicar el diagnóstico por capas cuando intervengan VM, anfitrión, navegador, aplicación, agente remoto o MCP. Evidencia ampliada: `/home/labgestor/utilidades/conectividad-comunicacion/documentacion/LECCIONES_VERIFICADAS_CONECTIVIDAD_2026-10-25.md` (referencia local opcional, no requisito para usar esta skill).

- **Infraestructura:** separar interfaz de red, NAT/red privada, DNS, proxy de entorno, transporte y servicio. Una respuesta CONNECT 403 de un proxy heredado no prueba que Internet esté caído. Antes de cambiar red o reiniciar, aislar la capa y conservar una vía de recuperación; un timeout breve no prueba fallo persistente.
- **Capacidad por cliente:** detectar realmente herramientas y autorizaciones de la cuenta y plataforma. No extrapolar acceso entre ChatGPT, navegador, Work, Codex, Free, Plus, Android, Voz Live o nodos remotos. Una VM accesible depende de que siga funcionando su anfitrión.
- **Eventos vs. visualización:** conectividad SSE/websocket, estado del servidor y revisión actualizada no garantizan que la interfaz haya representado el cambio. Verificar por separado transporte, aplicación, contenido visible, audio y persistencia, con pruebas negativas y reversión.
- **Pilotos seguros con navegador:** favorecer perfiles temporales, contenido sintético, permisos mínimos, endpoints loopback y control de captura desactivado de origen. Una prueba satisfactoria con Chrome headless y extensión aislada NO acredita capturas en cuentas reales, otros navegadores o dispositivos.
- **Autonomía real:** instrucciones de una skill no equivalen a hooks, suscripciones de eventos ni ejecución tras finalizar una sesión. Los hooks requieren un host compatible y pruebas específicas; no asumir captura de conversaciones ChatGPT por un hook de otro cliente.
- **Diseño MCP:** distinguir adaptador y lógica de negocio, servidor/transporte MCP y cliente/presentación. La invocación y la devolución de datos estructurados deben comprobarse en el cliente real; no asumir capacidades de voz, PiP o panel visual por presencia del servidor.
- **Reproducibilidad y conservación:** transferir contexto entre agentes autorizados mediante documento versionado, ruta comprobable, inventario y pruebas; una ruta compartida no concede acceso. Registrar estado, licencias, permisos, costes, restricciones y evidencia. Las comprobaciones de sintaxis no sustituyen las funcionales.

### Resultado exigible
Para cualquier mecanismo nuevo, producir matriz `infraestructura | sesión/permiso | transporte | contrato | dato | interfaz | persistencia | recuperación`; anotar por elemento `no probado / probado localmente / probado extremo a extremo / bloqueado`. Evitar activar capturas, servicios persistentes, ampliar privilegios o almacenar credenciales sin autorización explícita.


## Navegador local, almacenes de claves y autorización OAuth (27/10/2026)

Leer el procedimiento transversal en [sesiones, navegador, llavero y OAuth](sesiones-navegador-llavero-oauth.md) antes de integrar cuentas con un navegador o almacenar credenciales. Separa y verifica individualmente red, proceso, sesión autorizada, entradas del almacén, lectura en memoria, inicio de sesión nuevo, consentimiento OAuth, datos privados, persistencia y seguimiento. No confundir éxito de un nivel con el siguiente.

**Aprendizajes probados:** Firefox ESR en Debian controlado mediante WebDriver BiDi solo en loopback (conexión temporal, DOM y cierre del puerto); X11 visual en caso necesario; GNOME Keyring/Secret Service con colección dedicada y permisos restrictivos; lectura local de entradas mediante resultado booleano, sin mostrar secretos. El login mediante contraseña y el flujo OAuth precisan pruebas independientes y cumplimiento de las condiciones oficiales del proveedor. Las comprobaciones de lectura de sesión, login nuevo y OAuth deben registrarse por separado en el proyecto del servicio.

**Orden de adopción:** contrato oficial y autorización (OAuth si procede) → conexión ligera permitida → navegador local con sesión consentida → interacción gráfica puntual. No usar APIs internas, traslado de cookies, contraseña de otro servicio ni automatización para sortear MFA o el bloqueo del registro de desarrolladores.

Inventario versionado de herramientas, estados, pruebas y límites en [inventariar-skills](../../inventariar-skills/references/inventario-acceso-web-2026-10-27.md). Ante discrepancia entre documento y plataforma, actualizar evidencia y mantener estado NO_PROBADO o BLOQUEADO hasta comprobar.
