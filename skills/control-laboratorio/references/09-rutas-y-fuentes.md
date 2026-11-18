# Directorio de fuentes canónicas (rutas son referencias, comprobar existencia)

## Principio de recuperación
Usar $HOME solo como raíz del usuario Debian autorizado, no como una orden para buscarlo indiscriminadamente. Verificar con herramientas de solo lectura que la ruta existe, comprobar fecha/versión y no asumir acceso si el MCP carece de la capacidad. El manual local tiene precedencia sobre un ejemplo histórico solamente en lo que acredita; el proceso activo tiene precedencia sobre ambos.

| Componente | Entrada de documentación o código que conviene inspeccionar | Evidencia adicional |
|---|---|---|
| Gestor de Skills | $HOME/proyectos/gestor-de-skills/skills/ y scripts/package_plugin.py | git status / SHA, tests, release Plugin Creator |
| LAB-AUTH | $HOME/proyectos/_gestion/credenciales-laboratorio/LAB-AUTH.md | adaptador local, metadatos de llavero, sesión privada verificada |
| JCCM/ATE | $HOME/proyectos/_gestion/credenciales-laboratorio/ate_*.py | estado personal real, fuente oficial y fecha |
| InfoJobs | $HOME/proyectos/Buscar-Curro/infojobs_*.py | Firefox dedicado, lector privado, fecha, pruebas |
| Buscar Curro jornada | $HOME/proyectos/_gestion/buscar-curro/ | service/timer, informe privado y público saneado |
| Educamos | $HOME/proyectos/educamos-puente/educamos_diario.py | timer, estado de mensajes, adjuntos descargados |
| Bibliotecario | $HOME/bibliotecario-piloto/interfaz_chat.py | registro SQLite, revision y brief releído |
| Control Debian | $HOME/proyectos/tutorial-generico/control-debian/ | conector MCP visible, servicio efectivo y catálogos |
| Catálogo herramientas | $HOME/utilidades/CATALOGO - Herramientas del laboratorio.md | confrontar fecha y servicios vivos |
| CDC / puente chats | $HOME/proyectos/comunicacion-chats/ y receptor Github del laboratorio | mensajes/confirmaciones, servicio y repositorio privado |
| Procedimientos Goose | $HOME/proyectos/_gestion/procedimientos/ | instalación real, servicio/cliente y pruebas |
| Resguardo de habilidades | $HOME/proyectos/gestor-de-skills/ y respaldo separado cuando exista | hash, licencia, versiones y restauración probada |

El listado **no** autoriza recorrer ni copiar todo $HOME, y puede evolucionar. No incluir rutas que contengan secretos en resultados públicos. No registrar nombres de usuario, cookies, OTP ni atributos identificativos de menores.

## Chequeos seguros orientativos
- Verificar identidad: comando local autorizado id -un, hostname sanitizado o herramienta de estado; un nombre de servicio sólo identifica una intención.
- Git: git status --short, git rev-parse HEAD, git ls-remote origin refs/heads/main; si hay riesgo de datos confidenciales, mostrar solo nombres de archivos, no diffs completos.
- systemd: systemctl --user is-active, is-enabled, show o list-timers para la unidad concreta; no reiniciar por el mero hecho de consultar.
- Biblioteca: buscar → brief → abrir documento local → readback tras un hito; nunca escoger expediente por coincidencia de una palabra aislada.
- Tarea: ejecutar diagnóstico de estado del coordinador antes de iniciar recolección; leer último informe en modo saneado y fecharlo.
- Plugins: consultar metadata y archivos efectivos, no confiar en el número de versión comunicado en un chat anterior.

## Cuándo un documento es histórico
Cuando su fecha es anterior a un cambio posterior del Bibliotecario, código o servicio; cuando indica v7/38 herramientas pero el servidor actual se identifica como v8.x; cuando da una ruta que ya no existe; cuando registra «diseñado» pero un ensayo posterior validó o descartó ese diseño. Citarlo solo como antecedente. Nunca corregir a ciegas un servicio activo siguiendo un README antiguo.

## Clasificación de evidencia
- CONFIRMADO: prueba directa con postcondición y momento/versión.
- VERIFICADO EN PRUEBA: fixture o simulación, no producción.
- PARCIAL: una fuente o fase falló o datos incompletos.
- PENDIENTE: procedimiento disponible sin validación de fin a fin.
- BLOQUEADO: autorización, coste, permisos o limitación técnica identificados.
- DESCARTADO: alternativa menos fiable o innecesaria; conservar motivo.
