# LAB-AUTH — ruta preferente para autenticación web local autorizada

## Propósito y activación
Esta referencia complementa la metodología general de `acceso_webs` y la [recuperación visual](recuperacion-visual.md). **Si una página exige inicio de sesión**, comprobar primero si existe una sesión válida y un conector oficial. Cuando el usuario haya autorizado el acceso desde el laboratorio Debian y esté realmente disponible la herramienta local **LAB-AUTH**, recuperarla antes de crear otro script de login. LAB-AUTH no forma parte de la skill distribuida: es software del dispositivo, con sus permisos y adaptadores propios. No asumir que está instalado en otros equipos, cuentas o chats.

## Recuperación del procedimiento existente
1. Consultar los conectores/MCP realmente activos y comprobar que Control Debian puede consultar el expediente del Bibliotecario. Buscar el expediente **«Acceso web y llavero seguro del laboratorio Debian»**, comprobar título y leer su última revisión (nunca asumir un número fijo).
2. Leer el manual local `LAB-AUTH.md`, `LAB-AUTH-HERRAMIENTA.md` y el código/catálogo de adaptadores del proyecto «Credenciales del laboratorio» en Debian antes de usarlo. La versión inicial comprobada el 15/11/2026 es **LAB-AUTH 0.1.0**; otras versiones deben validarse de nuevo.
3. Confirmar que `~/.local/bin/lab-auth` existe, que el entorno gráfico y el MCP permiten ejecutar y que el portal exacto está registrado en `lab_auth/adapters.py`. No proporcionar URLs arbitrarias ni credenciales en argumentos. Si no está disponible, usar navegación normal y procedimientos oficiales, o pedir la intervención necesaria; no simular autenticación.
4. Reutilizar una sesión autorizada si ya es válida. Distinguir acceso público, sesión recuperada, prueba de formulario e **inicio de sesión completo realmente verificado**.

## Decisión y comandos (sólo por acceso local autorizado)
- `lab-auth list`: inspección del catálogo sin conexión.
- `lab-auth status <portal>`: consulta de metadatos de disponibilidad local de credenciales; no debe mostrar su contenido.
- `lab-auth probe <portal>`: prueba del formulario con valores sintéticos, sin leer claves ni enviar login; validar dominio y selectores.
- `lab-auth login <portal>`: **únicamente cuando el titular haya pedido o aprobado el inicio de sesión concreto**. El motor recupera usuario y contraseña dentro de Debian desde GNOME Keyring, envía una sola vez al dominio permitido y comprueba la señal de éxito. No devolver secretos, cookies, tokens ni HTML privado al chat.

Actualmente se conocen los adaptadores `jccm`, `educamos` e `infojobs`. **Al 15/11/2026**, el motor LAB-AUTH tiene E2E de login comprobado en **JCCM**; EducamosCLM e InfoJobs tienen sondeos reales de formulario, pero NO un nuevo login completo homologado en este motor. Las pruebas históricas de scripts independientes no convierten el estado del motor en E2E.

## Para incorporar un portal nuevo
Definir un adaptador explícito y revisado, con dominio oficial permitido, campos/selectores específicos, redirecciones admitidas, autenticación verificable y pruebas sintéticas sin credenciales. No reutilizar por adivinación un adaptador de otra web. Si exige CAPTCHA, MFA, verificación de identidad o consentimiento, detener el login automático y utilizar las opciones oficiales con intervención del titular. No modificar almacenes de secretos, instalar un servicio persistente ni crear automatizaciones sin autorización.

## Integración con la navegación visual
Cuando la web pública está bloqueada a HTTP o a WebDriver, comparar primero con un Firefox gráfico normal autorizado; **no tratar el error 403 como falta de autenticación**. Si existe login legítimo, determinar por separado la compatibilidad de la ventana/sesión visual y del motor LAB-AUTH (cuyo navegador temporal no garantiza compartir sesión con el Firefox normal). No exportar cookies para unir ambos contextos ni declarar que una página autenticada en un proceso sirve automáticamente en otro. Si la sesión es temporal, operar y verificar dentro de su propio contexto o usar la navegación oficial autorizada.

## Pruebas y estado de salida
- Dato público o sesión previa válida: evitar login innecesario.
- Portal reconocido: `list`, `status`, `probe` no deben revelar secretos ni enviar formulario; `login` requiere petición del titular y verificación posterior.
- Portal desconocido: pedir/revisar adaptador, dominio y consentimiento; no adivinar ni introducir contraseñas en el chat.
- Fallo o rechazo del portal: registrar causa (MFA, CAPTCHA, selectores, red, autorización, 403, sesión caducada) sin insistencia ni bypass.
- Distinguir `SONDEO_OK`, `LOGIN_VERIFICADO`, `SESIÓN_EXISTENTE`, `PENDIENTE_HOMOLOGACIÓN` y `BLOQUEADO`.
- Conservar solo resultados sanitizados y fecha/versión en el expediente local, según autorización. Los manuales y evidencias permanecen en Debian; GitHub público contiene **únicamente** este procedimiento genérico, nunca claves ni datos personales.

**Alcance:** esta skill describe qué hacer y cuándo; no ejecuta el login por sí misma. Su capacidad depende del MCP conectado, permisos actuales, herramientas locales y autorización del titular.
