# LAB-AUTH: autenticación local, navegadores y sesiones

## Fuente y modelo de confianza
El manual vivo principal es $HOME/proyectos/_gestion/credenciales-laboratorio/LAB-AUTH.md y las referencias de acceso_webs, especialmente su protocolo genérico de autenticación y navegación. Antes de actuar, leer versión y fecha del manual local y contrastar con el adaptador actual; muchas referencias históricas documentan estados parciales superados después.

Arquitectura: ChatGPT solicita una operación autorizada → Control Debian ejecuta procedimiento local → adaptador oficial por portal → GNOME Keyring guarda secretos y entrega su uso solo al proceso local → Firefox/WebDriver o AT-SPI interactúa y valida → informe mínimo saneado. **No hay motivo para obtener contraseña/OTP en el chat**. La herramienta de lectura de metadatos de llavero NO revela contenido.

## Decisión por fases
1. Portal y finalidad legítima exactos, URL HTTPS oficial, autorización del titular y alcance (leer, cambiar, inscribir). No enviar candidaturas, aceptar llamamientos ni marcar correos como leídos salvo petición explícita o tarea previamente autorizada.
2. Consultar el expediente del Bibliotecario, última sesión comprobada, adaptador y llavero. Preguntar únicamente si falta intervención real: desbloqueo local, consentimiento nuevo, factor multifactor o modificación sustancial.
3. Reusar la **sesión dedicada** si su propia página verifica identidad y datos privados. Un perfil existente, proceso Firefox activo o URL guardada no basta.
4. Si la sesión no vale, comprobar metadatos de credencial y estado de colección; usar el procedimiento oficial único. No recrear OAuth Gmail ya autorizado ni instalar Thunderbird otra vez sin prueba de ausencia.
5. Sondear formulario y dominio sin secretos; verificar nombres, campos y estado. Leer secretos localmente únicamente en el proceso permitido; rellenar, comprobar localmente, realizar un envío permitido y verificar contenido privado. Captcha o MFA no resuelto significa detenerse y clasificar.
6. Extraer solo el dato solicitado; informe de estado y timestamp, nunca HTML completo ni sesión. Regresar con estado VERIFIED / PARTIAL / UNVERIFIED y causa concreta. Limpiar ventanas y perfiles **creados por la prueba**, no el perfil persistente autorizado.

## Adaptadores conocidos
- **JCCM/ATE, Portal Personal Laboral:** procedimiento de $HOME/proyectos/_gestion/credenciales-laboratorio/ate_*.py; la entrada privada de bolsa debe verificarse por el registro personal, no por el PDF público ni la etiqueta de estado de una llamada. El llavero LAB-AUTH puede estar en colección «Credenciales del laboratorio»; confirmar origen actual en metadatos, no asumir que «Login» sigue siendo necesaria.
- **EducamosCLM:** $HOME/proyectos/educamos-puente/ y coordinador educamos_diario.py; distinguir autenticación, lectura de mensajes, adjuntos realmente descargados, estado leído/no leído y creación de resumen. Un contador de adjuntos 0 no demuestra que se haya extraído un fichero.
- **InfoJobs:** $HOME/proyectos/Buscar-Curro/ y $HOME/proyectos/_gestion/credenciales-laboratorio/. El lector accesible exige un navegador Firefox dedicado con perfil propio y la página de candidaturas; el sondeo puede devolver private_read_unverified si el navegador no está listo. Recuperar sesión antes de iniciar login nuevo. Las rutas /candidate/my-infojobs.xhtml y /candidate/applications/list.xhtml son ambas candidatas reales: no asumir que la segunda es error.
- **MFA mediante correo:** Thunderbird LAB-AUTH puede estar instalado fuera de PATH, bajo $HOME/.local/opt/lab-auth-thunderbird/ y con perfil en $HOME/.local/share/lab-auth-mail-profile. Detectar el ejecutable y los procesos reales, no deducir ausencia por command -v. Un Gmail OAuth2 autorizado en Thunderbird no implica que el navegador Firefox esté autenticado. El lector de OTP debe comprobar emisor/fecha y no mostrar el código; un solo intento y límites de reintentos.

## Perfiles y limpieza
Distinguir Firefox habitual del usuario, perfil LAB-AUTH persistente, perfil temporal sintético y Firefox del agente. No reutilizar cookies de otro propósito ni transferir archivos de perfil. No abrir múltiples sesiones durante la misma prueba. Los procesos de prueba que uno abre deben cerrarse tras la verificación; NO eliminar perfiles persistentes o finalizar procesos anteriores sin identificar su titular.

## Resultados mínimos fiables
reportar site, timestamp local y UTC cuando sea útil, metodo, session_reused, authenticated_verified, data_verified, attachment_count_verified si corresponde, estado, reason, next_action sin secretos. OTP_received no equivale a login_verified. login_verified no equivale a application_read_verified. No actualizar Bibliotecario con una conclusión más fuerte que la observación.

## No hacer
No eludir CAPTCHA ni límites de sitio; no utilizar contraseñas en URLs, argumentos de comando, git, GitHub, logs, pantalla del chat o tareas programadas. No configurar credenciales generales sin autorización. No guardar tokens en habilidades. No inventar navegación al recibir 403: consultar acceso_webs y diagnosticar permisos, red, protección, consentimiento o JavaScript.
