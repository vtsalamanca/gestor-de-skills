# Recuperación, reversión y copias de seguridad

## Qué significa «tenemos copia»
No llamar copia integral a un checkout Git, ZIP de skills, archivo de estado o snapshot parcial. Una recuperación del laboratorio puede requerir VM Debian, sistema de archivos, configuraciones systemd, código Git, base SQLite del Bibliotecario, credenciales del llavero, perfiles de navegador autorizados, datos privados, dependencias locales y conexión MCP. Esos elementos tienen controles y destinos distintos; algunos no pueden exportarse ni restaurarse sin el titular.

## Inventario antes de recuperar o borrar
Para cada respaldo anotar: origen y destino, fecha UTC/local, versión, alcance, soporte físico, tamaño, hash/manifest, método de restauración, permisos, autenticación necesaria y resultado de prueba de lectura. La mera existencia de un ZIP en Windows no confirma que pueda restaurar Debian. Una copia GitHub pública excluye por diseño datos privados y servicios.

Si el usuario pide limpiar: comparar inventario con uso real, verificar al menos una copia alternativa legible, aclarar qué elementos son únicos y solicitar autorización de borrado concreta. No conservar duplicados indefinidos por miedo ni destruirlos con limpieza indiscriminada.

## Capas de recuperación
1. **Skills y complemento:** repositorio gestor-de-skills, manifiestos y paquete exacto del commit publicado; release privada recuperable si el proveedor lo permite; comprobar versión y hash.
2. **Código de proyecto:** repositorios Git y cambios locales no rastreados, ramas de rollback, pruebas y README operativo. Un snapshot de archivos de repo privado puede coincidir con un árbol sin contener todo el historial.
3. **Bibliotecario:** SQLite y documentos originales, con integridad/backup y revisión real; no reconstruirlo solo desde una conversación.
4. **Aplicaciones y sesiones:** configuraciones de servicios y ejecutables locales. Credenciales/llavero/Thunderbird/Firefox no deben copiarse a GitHub ni a un ZIP público. Su recuperación necesita un procedimiento privado autorizado; no comprometer secretos para hacer un backup «completo».
5. **Equipo/VM/host:** respaldos offline/medios físicos y estado de VirtualBox/Windows, distintos de repositorios. Después de restaurar, verificar control remoto y reconexión antes de considerar operativo.
6. **Programación y entrega:** tareas Automations de ChatGPT y timers systemd tienen configuración independiente; restaurar código no restaura por sí mismo horarios, notificaciones ni permisos de la plataforma.

## Runbook de retorno tras incidente
A. Estabilizar y observar antes de modificar. B. Identificar última versión buena por pruebas y hashes. C. Seleccionar alcance mínimo de restauración, preservando datos recientes. D. Validar medio y permisos. E. Restaurar en ubicación alternativa o mediante operación atómica y reversible. F. Probar sintaxis, servicios, API/MCP y flujos privados solo con autorización. G. Verificar ausencia de duplicados, referenciar el backup y registrar readback en Bibliotecario. Nunca inventar rollback universal ni borrar la única copia.

## Rechazo por riesgo
Si faltan medio de recuperación, autorización para respaldo imprescindible, integridad comprobada o acceso al equipo, detener la operación irreversible y mantener servicios originales. No mover llavero ni tokens a otra máquina por copia de comodidad.
