# Arquitectura y fuentes de verdad del laboratorio

## Sistema completo (modelo lógico, no un inventario congelado)
ChatGPT (interfaz de coordinación) → conector Control Debian autorizado → Debian/XFCE y aplicaciones → adaptadores locales y servicios → resultados saneados. El Bibliotecario SQLite registra hitos y enlaces a fuentes; GitHub versiona código; el complemento privado distribuye habilidades. Algunas automatizaciones ChatGPT consultan resultados del colector Debian. CDC e Igor son vías alternativas o complementarias, nunca sustitutos presumidos del MCP.

La VM Debian y el anfitrión Windows cumplen papeles distintos; una herramienta conectada a Debian no demuestra acceso a Windows. El túnel de Control Debian y el ejecutor remoto pueden tener estados diferentes: comprobar ruta real y no inferir conectividad desde un único indicador. Los controles de autorización local pueden requerir intervención presencial incluso con el servicio activo.

## Jerarquía de evidencia por componente
1. **Estado vivo**, observado por herramienta adecuada: identidad del host, procesos, servicios, sesión, temporizadores, último informe y hora, árbol Git, readback.
2. **Código ejecutado y configuración efectiva** en Debian, estudiados sin volcar secretos: unit files de systemd, entrypoints, adaptadores, pruebas y registros saneados.
3. **Bibliotecario**: revisión posterior verificable para recuperar el porqué, incidencias previas y pendientes, pero no sustituye la prueba operativa.
4. **GitHub canónico**: fuente para el historial del código versionado, releases y comprobación de diferencias; los directorios privados de operación no pertenecen a repositorios públicos.
5. **Skills, catálogos y manuales**: guías reutilizables con fecha; una guía antigua no confirma configuración actual.

El índice de herramientas local y los expedientes del Bibliotecario no son bases duplicadas del estado vivo. Referenciar los originales; actualizar solo cuando el usuario autorice el lote y el resultado esté verificado.

## Subsistemas
- **Control Debian — Sustituto independiente:** MCP preferente para consultas, acciones tipadas, terminal local autorizada, ventanas y procesos; túnel y servicio systemd de usuario. Exponer los límites de cada herramienta, no un permiso abstracto «todo».
- **LAB-AUTH:** credenciales en GNOME Keyring, perfiles privados de Firefox/WebDriver y adaptadores por sitio; JCCM/ATE, Educamos e InfoJobs poseen flujos distintos. Thunderbird independiente permite correo OAuth y, si procede, OTP local.
- **Proyectos funcionales:** Buscar Curro (ATE, fuentes públicas, candidaturas), Educamos (mensajes/adjuntos), Tutorial multimedia, impresión/escáner, utilidades, compras, catálogo y bibliotecas.
- **Bibliotecario:** SQLite, interfaz local, documentos y Observador; registra hitos sin copiar conversaciones completas ni secretos.
- **CDC/Igor/agentes:** mensajería entre procesos/chats, ejecución local, Goose y Ollama cuando la función esté disponible; comprobar servicios/modelos/credenciales antes de atribuir autonomía.
- **GitHub:** repositorios y workflows; fuente de código público y repositorio privado de puente. Mantener separado del perfil autenticado, respaldos integrales y datos escolares.
- **ChatGPT Automations:** programador y entrega, diferentes de los temporizadores Debian; cada eslabón se audita independientemente.

## Criterios de actualidad
El laboratorio ha cambiado de número de herramientas, nombre de túnel y rutas internas repetidas veces. No fijar un número de herramientas MCP como verdad permanente. Consultar el catálogo de herramientas expuesto EN ESTE CHAT, la configuración efectiva de Debian y los últimos hitos del Bibliotecario. Si divergen, explicar la divergencia. El catálogo de octubre puede servir como historia, nunca como confirmación de noviembre.

## Límites de la skill
Una skill no instala conectores, no obtiene una máquina desatendida, no ejecuta un workflow, no sincroniza GitHub automáticamente ni lee el llavero por sí misma. Requiere herramientas efectivamente conectadas, autorización válida y evidencia. No usar supuestos de otro chat como prueba de disponibilidad actual.
