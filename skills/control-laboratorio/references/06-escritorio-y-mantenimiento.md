# Escritorio, procesos, servicios y limpieza del laboratorio

## Mantenimiento conservador
Antes de abrir ventanas, iniciar procesos o modificar servicios, inspeccionar estado y propietarios. Para servicios propios del usuario, preferir systemctl --user status/show/list-units/list-timers. Verificar unit file efectivo y ExecStart real, no confiar en el nombre del acceso directo. No tocar servicios root/system sin solicitud y autorización específicas. Comprobar si la sesión gráfica XFCE existe, DISPLAY, XAUTHORITY y D-Bus cuando una operación GUI no encuentra ventana.

## Política de ventanas
- Inventario previo: aplicación, identificador, proceso, perfil y finalidad si es discernible.
- Usar ventana ya existente cuando es seguro; de lo contrario crear una ventana o perfil temporal señalado como propio.
- Para pruebas visuales preferir Mousepad/Writer/Calc de fixture. Validar foco y gesto por respuesta observable, no por éxito del comando.
- Inventario posterior y limpieza: cerrar solo **ventanas que esta prueba abrió**. No cerrar el Firefox del usuario, Thunderbird persistente ni sesiones personales, aunque sean muchas.
- Restaurar cambios de prueba en documentos, archivos y estados leídos/no leídos cuando se haya autorizado prueba reversible.
- Si no está claro quién creó una ventana, dejarla y reportarla, no destruir datos por mantener el escritorio despejado.

## Mantenimiento y reinicio
- Diagnosticar por separado fallo de reinicio normal, reconexión del MCP, bloqueo de sesión e inactividad. Una reconexión tras servicio restart no demuestra reinicio completo de Debian.
- Si hay necesidad real de reinicio, confirmar medio de recuperación autónomo, salvaguardar trabajo, preparar comprobación postarranque y evitar bloquear única ruta remota. No ejecutar reboot durante una auditoría documental.
- El túnel de Control Debian puede tener política Restart=on-failure y estado active; esa configuración no garantiza ruta funcional desde ChatGPT. Probar operación tipada y retorno.
- Guardar logs saneados mínimos; nunca imprimir variables de entorno privadas, argumentos con tokens, cookies, archivos de perfiles, secrets.yaml, keyring o correos.

## Orden y almacenamiento
- Diferenciar código canónico, estados privados operativos, documentos del Bibliotecario, artefactos de pruebas, temporales, paquetes de publicación y backups. No arrastrar ZIPs, informes duplicados y worktrees sin motivo.
- La limpieza se basa en inventario por antigüedad, tamaño, uso real, autor, retención y recuperación. NUNCA borrar carpetas de respaldo, instantáneas Windows/VirtualBox, perfiles o scripts solo porque parezcan obsoletos.
- Al finalizar una prueba, eliminar los temporales propios y comprobar si dejó procesos abiertos; conservar respaldos verificados y ramas que protegen cambios ajenos. No hacer borrados masivos o destructivos por defecto.
- Antes de cualquier limpieza irreversible exigir autorización específica, verificación de copia útil y enumeración concreta del alcance. No improvisar un «garbage collector» autónomo.

## Ficheros y transacciones
Editar con revisión de la fuente, comprobación de hash/versión y cambio mínimo. Usar escritura atómica cuando proceda; validar sintaxis antes de activar servicio. Para Git, preservar no versionados y cambios existentes, no aplicar reset --hard ni push --force. Para libros, hojas o documentos, preferir herramientas nativas especializadas y comprobar el artefacto resultante, no sustituirlo por imagen.

## Evaluación de éxito
Servicio active significa proceso en marcha, no función útil. Comando exit_code 0 significa retorno del programa, no necesariamente efecto final. Una interfaz E2E precisa leer la ventana/documento/estado correcto. Archivos equivalentes requieren hash y ubicación, no solo nombre.
