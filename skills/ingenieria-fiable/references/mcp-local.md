# Protocolo reutilizable: desarrollo y pruebas locales por MCP

## Evidencia de la experiencia (2026-10-20)
- Desktop Commander Remote 0.3.0 conectado a Windows; Node 24.22.0, Python 3.15 y Git 2.56 disponibles. La conexión depende de que siga ejecutándose el proceso local de Desktop Commander; cerrar PowerShell la interrumpe.
- Acceso a archivos limitado mediante `allowedDirectories=["C:\Proyectos\ChatGPT"]`. **Esto no confina los comandos ejecutados por PowerShell**. `blockedCommands` no constituye sandbox.
- Lectura/escritura MCP, Python local, clonado desde GitHub y batería `C:\Proyectos\ChatGPT\trabajar_local.py` probados. Los resultados son específicos de esta máquina y sesión; volver a verificar disponibilidad y herramientas.
- Repositorios canónicos: `vtsalamanca/Buscar-Curro` y `vtsalamanca/gestor-de-skills`. Evitar repositorios de copia antiguos y otras rutas sin justificar.
- Las pruebas de unittest y análisis sintáctico locales han funcionado; una prueba que exige crear symlink se omitió por permisos de Windows. No presentar ese caso como superado.
- Comprobación de estado Git, hashes SHA-256, `--ff-only` y comprobación remota antes de push utilizadas. No son una barrera de seguridad contra código malicioso.
- Las pruebas se ejecutan bajo la identidad del usuario, con sus permisos y acceso potencial a red: no hay aislamiento estricto demostrado. El procesamiento local no implica cuota ilimitada ni ausencia de costes del servicio MCP.

## Antes de trabajar
1. Recuperar el objetivo, estado de pruebas, commits y autorizaciones previas. Leer `organizaciondeltrabajo` y `ingenieria-fiable` disponibles. Verificar conexión MCP con `list_devices` y revisar `get_config`; nunca asumir que persisten permisos o una sesión.
2. Confirmar presupuesto adicional cero: consultar plan y límites del proveedor, no asumir gratuidad por saldo promocional. No instalar código, activar servicios facturables, iniciar procesos permanentes ni modificar seguridad Windows sin autorización expresa.
3. Preferir carpeta de trabajo expresamente autorizada, con lectura inicial y permisos mínimos. Evitar secretos; no registrar credenciales, cookies ni tokens. No usar `allowedDirectories=[]` (equivale a acceso general).
4. Comprobar origen, rama, estado limpio y trabajo pendiente antes de `fetch`; nunca hacer `reset --hard`, `force push` ni sobrescribir cambios. Actualizar solo con fast-forward y hooks desactivados cuando proceda.
5. Ejecutar solo pruebas locales conocidas, inspeccionadas y con fixtures; bloquear red en la medida posible, sin afirmar aislamiento por modificar `socket.connect` de un proceso Python (subprocesos pueden escapar). Priorizar dependencias existentes, sin instalaciones ni descargas.
6. Capturar código de salida, resultados por caso, omisiones y registros. Comparar hashes SHA-256 y estado Git antes/después; excluir solo residuos temporales conocidos. Revisar `git diff --check`, cuidando CRLF en Windows.
7. Separar *editado*, *probado*, *confirmado localmente*, *sincronizado* y *publicado*. Antes de publicar, verificar de nuevo HEAD remoto frente a base del commit, ejecutar pruebas y no forzar el push; confirmar el SHA remoto tras envío.
8. Si falla la conexión, comprobar el proceso local una vez y recuperar sesiones; no repetir comandos fallidos sin hipótesis. Mantener un registro de las limitaciones pendientes.

## Seguridad especial de archivos comprimidos
- Comprobar rutas absolutas, saltos `..`, separadores Windows y prefijos de unidad. Validar destino real y enlaces simbólicos; probar en Windows y otro entorno compatible cuando sea posible.
- Rechazar archivos sensibles (`.env`, `.pem`, `credentials.json`), nombres incoherentes y archivos desmesurados. Preferir empaquetado determinista con hash y pruebas sintéticas.
- Una comprobación de ruta y la extracción TAR con `filter="data"` reducen riesgos, pero no justifican declarar seguridad total sin auditar enlaces, tipos, límites de tamaño y condiciones de carrera.

## Ruta concreta reutilizable (solo cuando exista)
- `C:\Proyectos\ChatGPT\preparar_proyectos.py`: verifica el estado Git y actualiza mediante avance directo.
- `C:\Proyectos\ChatGPT\ejecutar_pruebas.py`: corre pruebas locales y registra estados y hashes.
- `C:\Proyectos\ChatGPT\trabajar_local.py`: encadena ambos con detención ante fallos.
- Antes de emplear scripts heredados, inspeccionar el contenido y comparar con la versión actual de los proyectos. No incorporar rutas personales ni IDs de dispositivos en instrucciones universales.

## Limitaciones y mejoras futuras
Pendientes: aislar terminal en VM/contenedor sin acceso a credenciales, comprobar symlinks con permisos apropiados, asegurar compatibilidad de scripts, y estudiar inicio opcional del agente local sin ampliación innecesaria de acceso.


## Laboratorio Debian aislado mediante MCP → Windows → SSH (validado 2026-10-21)
**Arquitectura comprobada en un entorno concreto:** herramienta Remote Desktop Commander autorizada en ChatGPT → terminal Windows → OpenSSH con clave de usuario → Debian 13 XFCE en VirtualBox mediante red host-only. El puente de comandos se encapsuló en un lanzador `.cmd` (evita depender de políticas de PowerShell para `.ps1`); se comprobó ejecución SSH y copia SCP sin contraseña. No incluir direcciones privadas, identificadores de dispositivos, claves ni rutas personales en la skill universal: conservarlos solo en documentación local protegida y verificar en cada sesión.

**GUI sin dependencias nuevas:** mediante Python 3 `ctypes` con `libX11.so.6` y `libXtst.so.6`, conexión a `DISPLAY=:0`, extensión XTEST y emisión de movimiento, clic y teclas. Se verificaron eventos y apertura de Mousepad en XFCE. Este mecanismo depende de X11; no presuponer Wayland, sesiones sin DISPLAY ni control de aplicaciones protegidas. Evitar simular credenciales o escribir contraseñas por herramientas.

**Privilegios por autorización presencial:** lanzar desde SSH una terminal gráfica XFCE con un script de alcance mínimo; el usuario introduce la contraseña `sudo` *directamente en Debian*. El script deja un marcador de estado no sensible; ChatGPT comprueba el resultado por SSH. Validado con `sudo -v` y `sudo id -u` (UID 0), resultado `ADMIN_OK`. Revocar caché con `sudo -k`. No guardar contraseñas, usar `sudo -S`, instalar servicios de privilegio permanente ni configurar `NOPASSWD` para evitar la intervención humana.

**Auditoría de red y endurecimiento ejecutados:** VirtualBox con adaptadores host-only, sin NAT ni puente; rutas a destinos IPv4 e IPv6 externos devolvieron `Network is unreachable`. En el anfitrión se observó reenvío IPv4/IPv6 deshabilitado en el adaptador host-only. Portapapeles, drag-and-drop, USB y VRDE deshabilitados; instantánea de recuperación existente. `ss` y `systemctl` revelaron SSH en todas las interfaces, Avahi y CUPS. Se desactivaron servicio y socket de Avahi; CUPS permaneció escuchando solo en localhost. Se aplicó configuración de SSH con `ListenAddress` en la IP host-only, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `PermitRootLogin no`, `PubkeyAuthentication yes`, `AllowUsers` restringido y reenvíos X11/TCP/agente/Unix/túnel desactivados. Validar con `sshd -t` antes de recargar y **comprobar un nuevo acceso SSH después**; ambas pruebas se completaron.

**Secuencia reutilizable segura:**
1. Verificar conexión MCP, identidad del equipo y VM, estado de snapshot, interfaz host-only y acceso SSH por clave. No confundir MCP con permiso para acciones ilimitadas.
2. Para tareas ordinarias, usar SSH/SCP con rutas y argumentos controlados; para GUI X11, comprobar DISPLAY y XTEST y verificar la ventana real, no solo la ausencia de error.
3. Para tareas root, preparar script idempotente, acotado y auditable; ejecutar en terminal gráfica; solicitar exclusivamente contraseña en la VM; leer marcador, salida y estado real; invalidar sudo.
4. Antes de tocar SSH/red, preparar reversión y evitar bloquear la única vía de acceso. Comprobar configuración efectiva, validar sintaxis, recargar (no reiniciar innecesariamente) y abrir una nueva conexión.
5. Para aislamiento, contrastar configuración VirtualBox, rutas del invitado, servicios escuchando, reenvío del anfitrión y mecanismos de integración. No confundir ausencia de ruta con aislamiento absoluto; el anfitrión puede actuar como intermediario.
6. Documentar `VERIFICADO`, `PENDIENTE` y riesgos residuales. No afirmar auditoría de firewall/ICS/NAT o captura de paquetes sin pruebas; en el caso de referencia esas verificaciones exhaustivas quedaron pendientes.

**Coste y alcance:** sin servicios de pago adicionales; requiere Windows encendido, VM arrancada y Desktop Commander conectado. No supone control remoto autónomo si faltan esas condiciones. No exponer claves SSH, direcciones de red internas ni identificadores personales en repositorios públicos.

## Política de acceso remoto ordinario (2026-10-22)
**Dispositivo operativo preferido y único sin autorización excepcional:** `debian-laboratorio`. Que Windows aparezca conectado no constituye permiso para ejecutar allí comandos. La desconexión habitual del agente Windows es intencionada; **no restaurarlo automáticamente**. Solo acceder a Windows tras autorización expresa, delimitando tarea y duración. Las pruebas y empaquetados deben hacerse en Debian, con herramientas existentes y sin instalar dependencias ni modificar seguridad sin permiso. Si Git falta, registrar limitación y utilizar recuperación autorizada desde GitHub, sin simular verificación completa. Comprobar si el agente de Debian sigue dependiendo del proxy del anfitrión: no confundir VM operativa con independencia real del PC. Nunca cortar la vía de recuperación de Debian sin pruebas y autorización.

## Arquitectura transversal definitiva (objetivo y condiciones de migración)
Para todas las tareas locales: ChatGPT orquesta; `debian-laboratorio` ejecuta y conserva los originales; el acceso remoto Windows se cierra al completar el traslado y permanece deshabilitado normalmente. Las excepciones a Windows requieren autorización específica y no pueden deducirse de que el agente esté online. **Drive es transporte auxiliar privado** para ZIP u otros archivos cuando la transferencia directa no sirva; nunca repositorio canónico ni salto obligatorio. La acción `Google Drive.upload_file` exige una referencia `file_uri` compatible, no una ruta `/home/...`; comprobar la transferencia antes de declararla operativa. Mantener documentos temporales bajo revisión y no realizar borrados automáticos. La independencia del agente Debian respecto del proxy/servicios Windows continúa **pendiente de prueba**; no cortar el último acceso de recuperación sin ensayo controlado y aprobación. No activar facturación adicional.
