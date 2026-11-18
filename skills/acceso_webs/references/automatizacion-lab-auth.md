# Acceso web autenticado en procesos programados: ejecución y entrega

Patrón genérico de continuidad: **origen web → ejecutor local → informe privado → lector MCP → notificación ChatGPT**. No sustituye instrucciones o consentimiento de cada portal. Caso de aprendizaje: reparaciones EducamosCLM e InfoJobs del 18/11/2026 en Debian.

## Preflight por capas
1. Confirmar equipo, conectividad MCP, usuario, escritorio X11 (si hace falta), proceso y permisos concretos; no equiparar «conector disponible» a «terminal permitida». La operación genérica `start_process` puede responder `Operation unavailable or denied` mientras una operación tipada del mismo conector funciona.
2. Separar lector de datos, autenticador y notificador. Primero reutilizar caché o sesión válida; solo un inicio nuevo legítimo si la sesión falló y existe autorización, con límites de intentos y enfriamiento tras errores.
3. Para programas con buzón OAuth2, detectar el ejecutable real también fuera de `PATH` y verificar proceso, perfil exclusivo, identidad y canal de correo antes de declarar la dependencia ausente. Un `dpkg` negativo no prueba que no exista una instalación privada.
4. Enumerar procesos de navegador y perfilar sus ventanas. Evitar lanzar un segundo Firefox cuando hay un perfil dedicado existente; verificar el mismo perfil tanto en el autenticador como en el lector de accesibilidad. Si hay dos formularios/ventanas ambiguas, diagnosticar y cerrar solo ventanas propias de ensayo, sin matar sesiones ajenas.
5. MFA autorizado: código recién recibido leído y escrito **solo en el dispositivo titular** a través de interfaz verificada, sin devolver OTP/cookies/tokens al modelo ni exponerlos en argumentos/logs. No sortear CAPTCHA ni insistir tras error.

## Ejecución programada fiable
- El sistema local programado (p. ej. `systemd --user`) hace una **sola** recogida: hora, identidad, permisos, exclusión mutua, tiempos límite y persistencia privada. El notificador ChatGPT consume un archivo de salida vigente y no ejecuta de nuevo el recolector.
- La lectura debe usar herramienta tipada y de **solo lectura** con contrato de estado, fecha, procedencia, cobertura, errores y conteos, sin permisos interactivos en ejecución desatendida. `debian_lab_command_approve_on_desktop` probado en un chat interactivo **no acredita** que una tarea programada pueda aprobarlo.
- No crear Work ni abrir un navegador de nube para presentar un informe local; no prometer que una instrucción textual controle el modo del producto. Si una tarea no dispone de acceso MCP desatendido, informar `ENTREGA_PENDIENTE` y no inventar resultados.
- Separar cinco pruebas: **temporizador activado**, **proceso realmente ejecutado**, **archivo privado actualizado**, **lectura MCP sin intervención**, **entrega programada en conversación**. Un informe completo generado en Debian no acredita que el chat lo haya recibido.
- Si hay lectura de mensajes escolares, apertura puede marcarlos leídos. Si un proceso termina ambiguamente, no reejecutarlo solo para producir un informe. Zero adjuntos descargados no acredita descarga exitosa de un adjunto real. Si falla una fuente, cobertura parcial ≠ ausencia de resultados.

## Diagnóstico y alcance de evidencia
Caso 18/11: el recolector local Educamos había generado informe completo (3 mensajes, 0 descargas), mientras el aviso de ChatGPT falló por terminal genérica. Una operación local tipada recuperó sesión; se preparó un timer separado de recogida y un aviso que lee el resumen. La entrega futura sin intervención seguía pendiente de acreditar.

Caso 18/11 InfoJobs: un Thunderbird privado estaba instalado y funcionando pero ausente de `PATH`; el lector y autenticador utilizaban perfiles Firefox diferentes. Una vez detectados, se cerró solo el Firefox duplicado de prueba y se comprobó de nuevo la sesión local. Una autenticación legítima y una lectura posterior dieron `private_read_verified` con una candidatura. Esto **no** demuestra persistencia tras reinicio ni ejecución programada futura.

## Contrato de cierre reutilizable
Por cada tarea registrar en privado: fecha y zona horaria, origen, versión local, temporizador, resultado del script, informe, lectura MCP, notificación, si hubo intervención humana, motivos de fallos y próxima verificación. Para la habilidad pública, guardar solo el patrón y pruebas saneadas, nunca datos personales, rutas privadas específicas, credenciales ni mensajes de terceros. Si el modo desatendido no está probado, marcarlo PENDIENTE, no RESUELTO.

