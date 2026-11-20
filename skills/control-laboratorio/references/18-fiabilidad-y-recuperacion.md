# Fiabilidad del laboratorio: Doctor y Supervisor (sin nuevos agentes)

## Motivo y límites
Un error de respuesta MCP NO demuestra que la acción no ocurriera: el servidor pudo crear un fichero, lanzar Firefox o guardar un cambio. La regla es observar la postcondición y NO repetir automáticamente los efectos ambiguos. Esta política coincide con el debate de idempotencia en el protocolo MCP y en ingeniería de workflows duraderos.

Doctor y Supervisor se ejecutan mediante Python estándar y SQLite; no acceden a secretos, no navegan, no modifican permisos y no reparan servicios automáticamente. Son herramientas internas y reutilizables, NO sustituyen las 81 herramientas del MCP ni observan los mensajes internos de ChatGPT.

## Doctor: diagnóstico en un comando
Código: `skills/control-laboratorio/tools/laboratorio_doctor.py`.

`python3 skills/control-laboratorio/tools/laboratorio_doctor.py --save`

Comprobaciones de solo lectura: integridad del informe y sus evidencias SHA-256, servicios principales, presencia real del hijo Node.js revisando `/proc/.../cmdline` (no inferir por `comm=node`), temporizadores, antigüedad de sus últimos disparos, resultado y antigüedad de la última ejecución de servicios Buscar Curro/Educamos, estado Git y documentación obsoleta.

Salida JSON con `status: ok|warning|error`. El resultado se guarda solamente al solicitar `--save`, en `~/.local/state/control-laboratorio/doctor-ultimo.json`, sobreescrito atómicamente con permisos privados. No crece un historial duplicado. La ausencia de alerta externa NO acredita que la máquina esté encendida. `--no-systemd --home DIR` sirve exclusivamente para fixtures.

**Limitaciones:** un timer activo no prueba que su acción terminara; un servicio terminado correctamente no prueba que ChatGPT entregara notificaciones ni que Educamos contenga nuevos mensajes. `full_vm_restore=unknown` hasta ensayar restauración integral real, por separado y con autorización.

## Supervisor: gestionar resultados inciertos
Código: `skills/control-laboratorio/tools/supervisor_operaciones.py`. Base privada SQLite `~/.local/state/control-laboratorio/operaciones.sqlite3`. Registrar únicamente claves opacas y SHA-256 de solicitud/justificante; nunca argumentos, contraseñas, mensajes ni contenido de documentos.

Antes de una operación con efectos:
1. Elegir clave estable por operación lógica y calcular SHA-256 de la solicitud validada localmente.
2. `python3 .../supervisor_operaciones.py begin --key CLAVE --kind write --request-sha SHA256`
3. Ejecutar la operación revisada **solo** si devuelve `started`.
4. Comprobar el efecto por otro canal fiable; `complete --key CLAVE --proof-sha SHA256` solo con justificante verificable.
5. Si la respuesta se perdió, `unknown --key CLAVE` y **detener** cualquier nuevo efecto hasta reconciliar con un justificante real.
6. Si se verificó que ya se aplicó: `reconcile --key CLAVE --outcome applied --proof-sha SHA256`. Si se demostró que NO se aplicó: `--outcome not_applied`, y solo una nueva invocación explícita `begin ... --allow-reconciled-retry` permite reintentar.

Un segundo `begin` para un trabajo `running` o `unknown` devuelve `requires_reconciliation`, código de salida 3. Mismo identificador con SHA distinto devuelve `fingerprint_conflict`. `already_succeeded` nunca vuelve a ejecutar la operación. El supervisor NO envuelve automáticamente las llamadas de cualquier chat: el flujo llamante tiene que usarlo expresamente.

## Integración supervisada: EducaMos y Buscar Curro
El módulo `skills/control-laboratorio/tools/supervision_diaria.py` se activa
mediante drop-ins de usuario versionados en `deploy/systemd`. Una clave
`daily:educamos:AAAA-MM-DD` o `daily:buscar-curro:AAAA-MM-DD` representa
una jornada local. Las dos unidades conservan sus timers y el trabajo se
ejecuta una sola vez por fecha y versión del script principal.

Para Buscar Curro el antiguo `ExecStartPre=-` de Thunderbird queda dentro
de la transacción supervisada; su error de salida sigue siendo consultivo,
como antes. Los programas originales y las credenciales NO se modifican.
La ejecución solo se acredita si el proceso retorna 0 y un informe privado
nuevo tiene fecha de la jornada, estado esperado y permisos restrictivos.
El Supervisor conserva hash del informe y ningún cuerpo escolar o correo.

Un segundo lanzamiento después de fallo incierto no vuelve a abrir mensajes
ni repetir fuentes. Si el proceso terminó y el informe se escribió antes de
perder la respuesta, el Supervisor lo reconcilia con su SHA. Si falta prueba
de efecto, la jornada queda bloqueada para intervención/diagnóstico y la
siguiente fecha dispone de clave diferente. Una salida parcial de Buscar Curro
es válida solo si el coordinador original devuelve 0 y estado `parcial`.

**Roll-back:** quitar exclusivamente las dos unidades
`10-supervisor.conf` de `~/.config/systemd/user/{nombre}.service.d/` y
aplicar `systemctl --user daemon-reload`. No borrar la SQLite: contiene
justificantes y debe poder inspeccionarse. No activar pruebas reales durante
la configuración. Pruebas sintéticas: `test_supervision_diaria.py`.
La recuperación y supervisión no acreditan entrega de avisos de ChatGPT.

## Recuperación y pruebas
Pruebas sintéticas: `python3 -m unittest discover -s tests -p 'test_supervisor_operaciones.py'` y `test_laboratorio_doctor.py`. La prueba SQLite restaura una copia en directorio temporal y verifica `PRAGMA integrity_check`; **no** es una restauración de Debian, perfiles Firefox, llavero ni archivos escolares.

Para una reparación real: identificar la capa, leer Doctor, consultar Bibliotecario, analizar logs acotados, probar en fixture, preparar reversión, modificar solo el componente afectado, verificar efecto y regresar a estado limpio. No activar `WatchdogSec=` sin que el propio servicio implemente `sd_notify(WATCHDOG=1)` correctamente; si no, systemd reiniciará un servicio sano por diseño.

## Fuentes metodológicas (referencia, no dependencias)
- MCP: especificaciones sobre herramientas, errores y claves de idempotencia.
- GitHub `obra/superpowers`: depuración sistemática y verificación final, sin instalar código ni hooks ajenos.
- Prefect: persistencia, caché y reintentos (estudiados, no instalados).
- Foros `r/selfhosted`: prueba de restauración y último éxito observable, no solo estado de timers.
- Foros `r/devops`: efectos duplicados después de timeouts.

No usar servicios facturables, infraestructura compleja de terceros ni automatizaciones globales para resolver un problema que cabe en dos scripts estándar.
