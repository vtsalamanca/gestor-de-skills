# Inventario verificado: acceso web y autenticación (27/10/2026)

Fuente canónica: vtsalamanca/gestor-de-skills, habilidad inventariar-skills.
Es un inventario de capacidades observadas, NO un listado de permisos otorgados.
Nunca incluir contraseñas, cookies, tokens, IDs de usuario, capturas privadas.

| Herramienta | Plataforma / función | Evidencia y estado a 27/10/2026 | Límites / permisos | Coste adicional |
| --- | --- | --- | --- | --- |
| Remote Desktop Commander | Debian local; comandos y acceso a archivos autorizados desde Chat | VERIFICADO, equipo debian-laboratorio online en la sesión | Sujeto a autorización, políticas y disponibilidad; no usar host Windows como ruta por defecto | 0 € observados; cuota no certificada |
| Firefox ESR + Xfce | Navegación gráfica Debian | VERIFICADO: InfoJobs Developers y área privada, Wallapop | Autenticación no se infiere de ventana visible | 0 € |
| Firefox WebDriver BiDi / Node | Control DOM navegador local | VERIFICADO_EN_ORIGEN: 1 candidatura InfoJobs con sesión existente, guardada como informe privado | Puerto 127.0.0.1 temporal, cerrar, no exportar cookies ni abrir servicios remotos | 0 € |
| XTest, xwininfo, xprop, xfce4-screenshooter | Control y comprobación X11 | VERIFICADO en Debian | Capturas contienen datos personales; borrar artefactos transitorios | 0 € |
| GNOME Keyring/Secret Service + libsecret/GI | Colección privada de secretos Debian | VERIFICADO: desbloqueo, entradas y lectura local InfoJobs sin revelarlas | Sin aislamiento estricto entre procesos del usuario | 0 € |
| Aplicación GTK local almacen.py | Guardar/verificar credenciales por servicio | VERIFICADO para InfoJobs; selector de Wallapop añadido, nueve tests locales correctos | Claves Wallapop no verificadas; no demuestra login web | 0 € |
| Firefox password manager | Almacenar sesión y opcionalmente contraseñas del perfil Firefox | Sesión InfoJobs VERIFICADA; contraseña guardada en perfil específico NO VERIFICADA | Es distinto de GNOME Keyring | 0 € |
| API InfoJobs Developers + OAuth | Acceso oficial consentido a candidaturas | DOCUMENTADO + cliente local con pruebas sintéticas; registro de apps BLOQUEADO (mensaje en portal 27/10/2026) | No dispone aún de Client ID, autorización real, costo API ni token | Pendiente de acreditar |
| Solicitud de acceso a InfoJobs (Gmail) | Pedir habilitación de app | MENSAJE ENVIADO desde Gmail; respuesta/autorización NO VERIFICADA | Canal de atención no confirmado como responsable de Developers | 0 € |
| Wallapop web | Identificación por Google, Apple o email; registro/verificación observados | FORMULARIO OBSERVADO; autenticación automática NO PROBADA | No mezclar contraseña federada con cuenta propia; MFA requiere titular | 0 € |
| HTTP Python (urllib) + acceso directo desde Debian | Páginas públicas, cabeceras y respuesta | GET InfoJobs/Developers 200; endpoint API privado sin token 401; HEAD o POST pueden variar | No confundir 200 con datos ni 405 con contraseña inválida | 0 € |
| GitHub + Actions + Plugin Creator | Versionar skills, empaquetado y release privado | HISTÓRICAMENTE VERIFICADO puente ZIP Action→Plugin Creator; por revalidar en cada release | GitHub ≠ complemento publicado ≠ habilidad cargada en chat; no incluir secretos | Cuotas por confirmar; no activar pago |

## Actualización de alcance (29/10/2026)
Este inventario conserva las observaciones del 27 de octubre. Las capacidades acreditadas desde entonces —Open Computer Use, Mozilla Firefox DevTools MCP, GeckoDriver, Codex CLI, CDC, GitHub Actions por eventos, Piper y la ausencia de ejecutor sin Codex— están documentadas con versión, cuota, riesgo y prueba real en [inventario del control de Debian (29/10/2026)](inventario-control-debian-2026-10-29.md). No confundir la cuota consumida de Codex con el coste marginal de ejecutar el runner autohospedado.

## Registro de decisiones y límites
1. Reutilizar acceso_webs y su referencia técnica; NO crear skill duplicada control-navegador sin necesidad funcional distinta.
2. Distinguir «colección presente», «entrada presente», «lectura local correcta», «sesión existente», «login nuevo» y «OAuth autorizado». Las pruebas del primer conjunto NO validan las últimas.
3. InfoJobs: información leída en sesión autorizada, una candidatura observada; registrar apps actualmente deshabilitado y solicitud de autorización enviada, no aceptada.
4. Wallapop: soporte en formulario local, pero las credenciales y la sesión Wallapop no han sido verificadas desde el llavero.
5. Mantener Windows como anfitrión de VM, nunca como carpeta activa ni almacén de secretos del proyecto Buscar Curro.
6. Preferir herramienta autorizada de menor coste total: API oficial → HTTP permitido → DOM Firefox temporal → control gráfico en último lugar; el método usado para investigar puede diferir del de producción.

## Fuentes comprobables
- vtsalamanca/Buscar-Curro: INTEGRACION_INFOJOBS_LLAVERO_DEBIAN_2026-10-27.md, OAUTH_INFOJOBS_OFICIAL_2026-10-27.md, infojobs_browser_bidi.mjs, infojobs_consulta_debian.py, infojobs_oauth_oficial.py y tests.
- Debian local: /home/labgestor/proyectos/_gestion/credenciales-laboratorio/almacen.py y test_almacen.py. No publicar contenido del llavero.
- Referencia técnica transversal: acceso_webs/references/sesiones-navegador-llavero-oauth.md.

## Plantilla para próximas herramientas
Nombre | versión | fuente canónica | plataforma | fecha | licencia | permisos | coste marginal | casos de uso | prueba real | resultado | límites | riesgo | reversible | propietario.

Estados: DOCUMENTADO, PROBADO_SINTETICO, VERIFICADO_EN_ORIGEN, VERIFICADO_EXTREMO_A_EXTREMO, BLOQUEADO, DESCONOCIDO, RETIRADO. Revisar antes de cada uso, no asumir conexión permanente.