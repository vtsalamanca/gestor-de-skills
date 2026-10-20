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
