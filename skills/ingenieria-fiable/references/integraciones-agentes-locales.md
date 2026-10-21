# Lecciones de integración ChatGPT, Work, Codex y escritorio (octubre de 2026)

## Resultado comprobado
- Desktop Commander MCP permitió ejecutar órdenes en Windows y, mediante SSH con clave ya autorizada, ejecutar `id` en Debian-Laboratorio de VirtualBox (usuario labgestor). Es una capacidad real de esta sesión, no un canal de mensajes persistente.
- En el prototipo local Chat/Work/Codex se validaron solicitudes con identidad por rol, revisión optimista, aprobación humana separada, GET de bandeja y POST de respuesta. Hubo pruebas completadas con resultados WORK_EVENTO_OK, WORK_API_OK y CODEX_API_OK.
- Un PR de GitHub llegó a desencadenar una ejecución de Work en una prueba; otro PR posterior NO la desencadenó, pese a que la automatización tenía instrucciones para ello. Una instrucción que dice «si llega un PR» no crea por sí misma una suscripción a eventos.
- Un panel Tkinter leyó SQLite y presentó respuestas existentes automáticamente; esto **no** implica entrega espontánea al chat actual. Una tarea programada ofrece una notificación futura, no inyección directa en la conversación abierta.
- En Windows `codex` no estaba en PATH (Node/npm sí); en Debian tampoco se localizó `codex`. Acceso a Codex dentro de ChatGPT no prueba disponibilidad de Codex CLI en el sistema.
- La máquina Debian-Laboratorio quedó comprobada en ejecución, red host-only 192.168.56.0/24, SSH con autenticación de clave y sin reenvío SSH. No confundir conexión remota con integración de producto o activador.

## Protocolo reutilizable
1. Definir la arquitectura por tramos: origen/activación, ejecución, persistencia del resultado, notificación y entrega a la conversación. Acreditar **cada tramo por separado**, con prueba de extremo a extremo.
2. Distinguir permiso humano, identidad de servicio y suscripción real al evento; verificar la existencia de esta última en la configuración del proveedor.
3. Usar un identificador de tarea único, validación exacta de destinatario/proyecto/revisión/estado, operación idempotente y comprobación de respuestas; impedir ejecuciones duplicadas.
4. Separar «respuesta pegada manualmente» de «resultado emitido por el ejecutor autenticado»; no elevar la primera a prueba de ejecución.
5. Cerrar un experimento infructuoso: desactivar las automatizaciones, conservar lecciones en la skill canónica y retirar programas, tokens y bases de datos de prueba, preservando proyectos independientes.
6. Evitar añadir scripts, interfaces, automatizaciones o instalaciones antes de demostrar que resuelven el requisito central; medir coste de herramientas, cuota, tiempo humano y carga de mantenimiento.
7. No almacenar credenciales en reportes ni repositorios; nunca versionar secretos, claves SSH, tokens, conversaciones privadas ni bases de datos operativas.
8. Para Linux virtualizado, comprobar primero VirtualBox/SSH existentes; no abrir nuevas redes, habilitar portapapeles compartido ni rebajar seguridad si el acceso ya funciona.

## Lección principal
**El puente técnicamente funcional entre procesos no garantiza que ChatGPT pueda lanzar Work/Codex ni recibir una respuesta en el chat sin intervención.** Expresar siempre la capacidad demostrada y la que sigue sin demostrarse. Evitar repetir este experimento si no aparece una API o un activador oficial verificable.

Contexto: prototipo descontinuado voluntariamente a petición del usuario. Esta referencia conserva conocimiento general, sin datos secretos ni identificadores privados.
