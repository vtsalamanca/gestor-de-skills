# Control Debian: protocolo de actuación mediante MCP

## Descubrimiento y preflight
1. Buscar la conexión real denominada **Control Debian — Sustituto independiente** (nombre visible sujeto a cambios). Enumerar las funciones disponibles y sus descripciones/argumentos. Preferir funciones tipadas para minimizar efectos.
2. Para identificar equipo y servicio, usar diagnósticos sanitizados, p. ej. debian_host_connection_health / debian_host_runtime_config o la operación fija debian_laboratorio_iniciar(estado); si retorna ticket, llamar debian_laboratorio_resultado(ticket). Comprobar el resultado, no solo el ticket.
3. Un túnel que responde «inactive» mientras una operación de terminal autorizada funciona exige comparar rutas y procesos concretos: no anunciar desconexión total si hay evidencia de conexión parcial.
4. Cuando se necesite una orden local revisada, usar debian_lab_command_approve_on_desktop únicamente si realmente figura disponible, con usuario sin privilegios, cwd controlado, timeout breve y autorización local efectiva. No declarar que es un shell genérico ilimitado. No imprimir variables secretas, dump de HOME, configuración del llavero ni archivos de sesión.
5. Verificar permisos efectivos del MCP. «Operation unavailable or denied» es un síntoma: obtener el nombre de operación, perfil, ámbito, capa de rechazo y alternativa autorizada; no reiterar idéntico intento ni usar permisos indirectos para saltarse la restricción.

## Capacidades y selección
- **Estado/servicios/procesos:** usar la operación de solo lectura del conector; si no alcanza, comando revisado sobre el propio usuario y comprobación de salida/exit_code.
- **Tarea fija autenticada:** operaciones tipadas infojobs_consultar, infojobs_autenticar, educamos_comprobar, educamos_autenticar cuando existan. Primero reutilizar sesión, luego un intento autorizado; recoger ticket y estado final. Nunca afirmar que un «ready» o URL redirigida equivale a lectura privada verificada.
- **Escritorio:** diagnóstico de ventanas propias, capturas y gestos comprobados cuando el conector los soporte; pruebas sintéticas Mousepad/Writer/Calc preferibles a interaccionar con sitios reales. Evitar adivinar coordenadas y nombres de ventanas. Cerrar **solo** ventanas abiertas por esa prueba.
- **Archivos:** leer en ruta revisada, realizar edición mínima, comprobar contenido/hash; distinguir APIs restringidas de acceso al proyecto y shell aprobado. No usar una función de escritura genérica denegada para inferir que el sistema entero es inaccesible.
- **Terminal sandbox:** no confundir sandbox de prueba limitado con la terminal del host. Respetar no_new_privs, no root, alcance del proceso, revisión de comandos y permisos.
- **CDC o puente GitHub:** alternativas cuando están habilitadas y documentadas, no excusas para duplicar servidores, clonar llaveros o crear túne­les nuevos.

## Secuencia de acción fiable
Preflight → lectura/estado → diagnóstico causal → decisión y autorización → operación acotada → verificación de efecto → limpieza → registro. Antes de un cambio de servicio preservar configuración vigente, verificar sintaxis y tener reversión. Para interfaz gráfica: inventariar ventanas antes y después; no cerrar Firefox o Thunderbird que ya estuviesen abiertos por el usuario.

La homologación histórica de 35/43/56/76/82 herramientas sirve para rastrear avances, **no** certifica que esa cifra esté expuesta en la sesión actual. Si la función no aparece, diagnosticar conexión y catálogo antes de cambiar código. No instalar otro túnel por defecto.

## Casos de fallo y qué significa cada uno
- **Tool missing:** catálogo no montado; comprobar plugin/conector y sesión actual.
- **Permission denied / Operation unavailable:** permiso, política local, perfil o validación concreta; explicar la capa si hay evidencia y nunca inventar que la plataforma fue responsable.
- **Connection down:** estado de túnel, ejecutor y servicio; comprobar con dos observaciones independientes.
- **Ticket sin resultado:** no computar como éxito; consultar resultado o caducidad.
- **Comando exit_code 0 pero sin efecto:** completar la postcondición observable.
- **Interfaz inaccesible:** distinguir DISPLAY/AT-SPI/X11, ventana, sesión bloqueada y portal externo.

## Seguridad
No redefinir «autorización global» como poder para cambiar políticas o eludir controles. No editar ejecutables de seguridad por rutas secundarias. Permiso de operar el laboratorio ≠ permiso de mostrar credenciales, borrar copia única, publicar material privado ni introducir pagos.
