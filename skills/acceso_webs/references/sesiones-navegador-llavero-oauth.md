# Acceso web avanzado: navegador local, llavero y OAuth
Consolidación 27/10/2026. Evidencia: Debian + Buscar Curro. Patrones reutilizables, sin secretos.

## Matriz de verificación por capas

| Nivel | Comprobación | NO demuestra |
| --- | --- | --- |
| Red | DNS, ruta, proxy, TCP/TLS, HTTP y método GET | Sesión privada |
| Navegador | Proceso Firefox y ventana X11 | Usuario autenticado |
| Sesión | Área privada y cuenta reconocidas en DOM | Login nuevo mediante contraseña |
| Llavero | Colección separada, desbloqueada, permisos | Credenciales presentes |
| Entradas | Un usuario y una clave para el servicio concreto | Lectura real de valores |
| Lectura | Proceso local recupera secretos en memoria y devuelve booleano | Acceso web exitoso |
| Inicio nuevo | Navegador con perfil sin cookies entra legítimamente | Todos los permisos |
| Datos | Registros privados correctos y campos mínimos | Cobertura completa |
| Persistencia | Archivo privado reabierto y permisos verificados | Seguimiento automático |
| Producción | Flujo de extremo a extremo repetible | Otro cliente/host soportado |

Estados: DOCUMENTADO, PROBADO_SINTETICO, VERIFICADO_EN_ORIGEN, VERIFICADO_EXTREMO_A_EXTREMO, BLOQUEADO, NO_PROBADO, RETIRADO. No ascender de nivel sin prueba.

## A. Firefox en Debian mediante WebDriver BiDi

- Verificar primero host vivo, sesión gráfica, navegador y perfil exclusivo; conservar la sesión existente. Ante prueba de contraseña nueva usar un perfil temporal limpio, no cerrar la sesión válida.
- Firefox ESR soportó un agente de WebDriver BiDi con puerto de depuración temporal exclusivamente en 127.0.0.1:9222. Un cliente Node local conectó por WebSocket a /session y utilizó session.new, browsingContext.getTree, browsingContext.navigate y script.evaluate. Verificado en este entorno, NO garantizado en otros.
- Restringir origen a dominio HTTPS exacto, no confiar en enlaces arbitrarios, no leer DOM ajeno. Confirmar indicadores de área privada y registros; esperar cargas asíncronas sin interpretar pantalla vacía como cero candidaturas.
- Cerrar sesión del protocolo, proceso temporal y puerto; restaurar Firefox ordinario. Inspeccionar realmente que no queden sockets escuchando. Los puertos de depuración de navegador son sensibles incluso en loopback.
- X11 disponible para control y diagnóstico con xwininfo, xprop, xfce4-screenshooter y XTest (libX11/libXtst). Las capturas pueden contener datos personales: eliminarlas y no subirlas al repositorio ni pasarlas como logs.
- Resultado real comprobado en Buscar Curro: lectura y guardado de 1 candidatura InfoJobs desde Firefox ya autenticado. NO se demostró inicio nuevo mediante contraseña, ni acceso OAuth funcional, ni automatización continua.

## B. GNOME Keyring y Secret Service

- Colección de secretos independiente «Credenciales del laboratorio»; no mezclar con el llavero predeterminado Login. Directorio privado 700, archivo de llavero 600; Python del sistema con gi.repository.Secret/libsecret, sin librería criptográfica propia.
- Esquema con service y field; validar servicio autorizado y cardinalidad exactamente una de usuario y una de clave. Nunca reutilizar contraseñas de otro servicio ni buscar globalmente en todas las colecciones.
- Introducción de claves SOLO por ventana local Debian. No transportar por argumento CLI, variable de entorno, fichero plano, GitHub, chat, logs, capturas, portapapeles ni plugins ajenos.
- Separar: existencia de colección, desbloqueo, entradas, lectura en memoria, login en sitio y sesión privada. Cada paso exige comprobación independiente. Mostrar solo resultado booleano de la lectura.
- Verificado: entradas InfoJobs y recuperación correcta mediante app local sin imprimir secretos. Wallapop está añadido como servicio independiente al selector, pero NO se ha demostrado contraseña Wallapop almacenada ni autenticación mediante llavero.
- Límite real: procesos de la misma cuenta Linux con llavero desbloqueado pueden solicitar secretos. No equivale a aislamiento por aplicación. Una cuenta que entra con Google no admite su contraseña Google como si fuera clave independiente de Wallapop.
- El titular completa códigos MFA, verificaciones de correo, CAPTCHA y consentimiento oficial; no eludir salvaguardas.

## C. OAuth y condiciones del proveedor

- Investigar reglas/condiciones antes de automatizar login. Si el proveedor exige OAuth 2.0 para una aplicación propia, preferir autorización consentida y NO rellenar la contraseña del candidato por una integración desarrollada por nosotros.
- Separar Client ID y Client Secret de aplicación, código de autorización, access token, refresh token y cookie de navegador. Scopes mínimos, redirección/callback, state y PKCE si están admitidos; verificar expiración y revocación. Secretos solo en almacén privado.
- Portal InfoJobs Developers autenticado mostró el 27/10/2026: «The registration of new apps is currently unavailable». Cliente OAuth local preparado y probado con datos sintéticos, pero no hay Client ID/Secret real ni tokens: acceso OAuth NO VERIFICADO y registro BLOQUEADO. Una petición de habilitación por email está ENVIADA, no autorizada.
- Wallapop mostró login por Google, Apple o email y paso de registro/verificación. No hay prueba de sesión Wallapop iniciada por el llavero. No convertir creación de cuenta en login involuntario.
- Una API documentada no implica que el registro, el permiso o el coste estén disponibles. No usar una API interna observada como sustituto sin autorización.

## D. Diagnóstico y economía

- HEAD 400/405 no prueba que GET esté bloqueado; contrastar método, ruta, redirección, TLS, sesión, tiempo de carga, DOM y permisos. Un CONNECT 403 de proxy heredado no significa que toda la VM carezca de red.
- Distinguir host Windows, VM Debian, cliente HTTP, Firefox, sesión OAuth, credencial guardada y API: ninguna de esas capas se hereda automáticamente.
- Si el sistema remoto de ejecución rechaza una orden, eso no acredita rechazo de contraseña por el portal. Documentar bloqueo de la capa real, sin reintentar compulsivamente.
- Ante hipótesis nueva, agrupar pruebas locales sintéticas y una sola verificación real controlada; no grabar secretos, no hacer cambios de red ni activar procesos permanentes sin autorización.
- Para cada integración: origen, tipo de permiso, prueba, fecha, coste, tasa de peticiones, cobertura, error, reversión y siguiente acción. Separar interfaz, transporte, datos, autorización y persistencia.

## Contratos de referencia, específicos de proyecto

- Repositorio vtsalamanca/Buscar-Curro: infojobs_browser_bidi.mjs, infojobs_consulta_debian.py, infojobs_oauth_oficial.py y pruebas; ninguna ruta contiene credenciales.
- Debian privado: /home/labgestor/proyectos/_gestion/credenciales-laboratorio/almacen.py. Ruta opcional y local, NO dependencia obligatoria de la habilidad.
- Catálogo versionado complementario: inventariar-skills/references/inventario-acceso-web-2026-10-27.md.

## Criterio de cierre

Producir matriz «infraestructura | sesión | credenciales | consentimiento | transporte | DOM | dato | archivo | seguimiento | recuperación», con estado y evidencia POR CASILLA. No declarar un login por haber leído una contraseña; no declarar autorización OAuth por haber redactado el cliente.