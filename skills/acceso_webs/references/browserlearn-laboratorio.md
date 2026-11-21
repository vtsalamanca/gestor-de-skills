# BrowserLearn en el laboratorio Debian — grabación local de procedimientos web

## Qué es y cuándo elegirlo
**BrowserLearn** es una aplicación de terceros de código abierto (licencia MIT), NO una herramienta expuesta directamente por el MCP Control Debian ni una nueva skill independiente. Código original: https://github.com/droidmaximus/browserlearn. La instalación examinada del laboratorio utiliza BrowserLearn 0.1.0, revisión original `a5a2bfa` y cambios **locales** en la rama `lab/privacidad-local`, commit `4f1ef61` (21/11/2026). **Comprobar la instalación y el commit reales antes de usarla; pueden cambiar.**

Úsalo cuando la tarea requiera **aprender un recorrido humano repetible por una página** para convertirlo en un procedimiento local y, previa revisión, exportarlo a Playwright. No usarlo para consultas HTTP simples, una extracción ya automatizada o como sustituto del adaptador de un portal. La grabación no implica por sí misma que la reproducción sea correcta ni que una sesión autenticada pueda reutilizarse.

## Dónde está, sin duplicar instalaciones
- Proyecto local Debian: `$HOME/proyectos/browserlearn-local` (Git independiente, no incluido en este repositorio de skills).
- Comando de arranque: `$HOME/.local/bin/browserlearn-lab start`.
- Lanzador de Chromium separado: `$HOME/.local/bin/browserlearn-lab-browser`.
- Datos y configuración privados: `$HOME/.local/share/browserlearn-lab/private` (directorio 0700, configuración 0600).
- Navegador de prueba independiente: `$HOME/.local/share/browserlearn-lab/browsers`.
- Manual más reciente de esa instalación: `$HOME/proyectos/browserlearn-local/LAB-SEGURIDAD.md`.

**Estas rutas son referenciales.** Confirmar disponibilidad y ejecutables con una herramienta local autorizada; leer `LAB-SEGURIDAD.md` y los manifiestos reales antes de iniciar. Ni ChatGPT ni Codex reciben el binario o las sesiones por instalar este plugin. No copiar bases de datos, perfiles, llavero, cookies o credenciales al GitHub público ni al complemento privado.

## Flujo operativo manual y seguro
1. Verificar conexión Control Debian, usuario y proceso. Buscar primero si hay un servidor existente en `127.0.0.1:7420`; no iniciar uno duplicado.
2. Abrir una terminal autorizada en Debian y ejecutar `browserlearn-lab start`. El panel incluye un enlace/código privado de emparejamiento: **nunca transcribirlo al chat, logs públicos ni al repositorio**.
3. Desde el escritorio Debian, abrir en otra terminal `browserlearn-lab-browser`, que usa **otro perfil de Chromium**, sin compartir las sesiones de Firefox/Chrome habituales. Conceder los permisos de la extensión en ese perfil cuando Chrome los solicite.
4. Entrar manualmente a la web para la que exista autorización. BrowserLearn puede operar en páginas HTTP/HTTPS de distintos dominios, pero su extensión tiene permisos globales de sitios; **iniciar la grabación de forma deliberada pulsando Record y detenerla con Stop**. Evitar grabar datos personales innecesarios. No superar CAPTCHA ni MFA automáticamente.
5. Comprobar el procedimiento guardado, la navegación y las acciones; verificar que los datos identificativos o secretos fueron saneados. La opción `BROWSERLEARN_STRICT_REDACTION=1` oculta los valores tecleados y hay patrones para DNI/NIE/IBAN españoles, **pero no garantiza ocultar nombres y datos existentes en DOM, URL, títulos o capturas**. Ante contenido confidencial, no exportarlo a una IA.
6. Si procede, probar el flujo exportado contra un sitio ficticio o entorno de pruebas antes de uso en una cuenta real. La reproducción puede ejecutar clics, formularios y envíos: exige autorización separada para la acción concreta. LAB-AUTH gestiona el inicio de sesión autorizado; BrowserLearn no es un gestor de credenciales.
7. Cerrar Chromium y detener el proceso de BrowserLearn. Verificar que el puerto 7420 ha quedado libre y que no se dejaron ventanas o servicios propios abiertos.

## Límites, permisos y coste
- **Local, sin proveedor de IA configurado** en la instalación auditada. Su servidor escuchó únicamente en `127.0.0.1:7420`; una petición sin autenticación devolvió HTTP 401. Una web visitada sí recibe el tráfico normal del navegador.
- Versión con permiso de extensión `http://*/*` y `https://*/*` dentro del perfil separado: **capacidad amplia de lectura e interacción**, aun cuando no haya grabación activa; no usar esta extensión en el perfil personal ni presumir inocuidad por ser local.
- No configurada como servicio de inicio automático ni como conector MCP disponible en ChatGPT/Codex. Si se solicita conexión MCP posterior, auditar la configuración, el acceso y sus capacidades antes de habilitarla.
- No enviar grabaciones a proveedores de IA externos ni habilitar tareas programadas por defecto. Presupuesto adicional: **0 €**.
- Pruebas registradas en Debian el 21/11/2026: núcleo 214, servidor 49, extensión 18 incluidas grabaciones de formularios sintéticos con Chromium aislado (**281 pruebas**). No prueban que funcione en todas las webs, páginas con restricciones, ni sesiones privadas reales.

## Diagnóstico y reversión
- Si la web no carga o no permite grabar, determinar si es un permiso de Chrome, página interna, extensión, navegador, servidor, autenticación o bloqueo de sitio. No resolverlo copiando perfiles con cookies o alterando permisos del MCP.
- En errores de grabación, comprobar primero el estado y los registros privados saneados; no repetir una acción con efectos sin comprobar si se completó.
- Si una actualización modifica el manifiesto de permisos, scripts o dependencias, detener y auditar el diff; conservar Git y la versión compilada que funciona. Retroceder solo tras comprobar grabaciones y dependencias propias.
- El repositorio `gestor-de-skills` registra **cómo elegir y usar** BrowserLearn; no reproduce su código ni lo instala en otro ordenador. Para otras máquinas se requiere instalación y auditoría separadas.
