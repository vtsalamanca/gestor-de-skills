# Igor, Goose, Ollama, CDC y puentes entre entornos

## Roles y límites
- **Control Debian:** vía de ejecución autorizada del chat hacia Debian. Preferirla para operaciones tipadas, terminal revisada y lectura de estado. No necesita una IA local para entrar a Educamos o usar LAB-AUTH cuando el MCP y el adaptador ya funcionan.
- **Igor:** nombre funcional del ayudante local y canal de encargos. Comprobar el estado real de igor-canal.path, servicios asociados, cola, logs saneados, herramientas permitidas y resultados antes de delegar.
- **Goose:** agente local que puede usar modelos remotos o locales según configuración activa. No asumir que «Goose instalado» implica que su aplicación Desktop funciona, que tiene permiso root o que puede navegar el escritorio.
- **Ollama/Qwen:** modelos locales sujetos a RAM, disponibilidad del servicio/modelo y capacidad para usar herramientas. La inferencia local no sustituye permisos, perfiles autenticados ni verificaciones.
- **Groq u otros proveedores:** pueden tener cuota gratuita, pero nunca activar facturación, usar saldo promocional ni invocar APIs tarifadas sin consultar límites y autorización explícita. No leer archivos secrets.yaml ni publicar configuración privada.
- **CDC:** comunicación de tareas/hitos entre procesos o chats por rutas autorizadas; distinguir gateway, registro de mensajes, entrega efectiva y respuesta. Un checkpoint no es envío automáticamente consumido en otra conversación.
- **Puente GitHub:** alternativa de continuidad histórica, con repositorio privado y receptor de eventos. Preservar si ya está configurada; no sustituirla por un túnel nuevo ni destruir su respaldo sin evaluación.

## Enrutamiento inteligente
Preguntar: ¿la tarea exige razonamiento/agente o solo ejecutar una función conocida? Para estado, logs, lectura de Informe y autenticación documentada, Control Debian + script es más directo que Goose. Para programación compleja o decisiones secuenciales, comparar Chat/analítica local, Codex, Goose/Ollama y Work por permiso, cuota, tiempo, privacidad y fiabilidad. Preferir herramientas sin nueva instalación ni coste. La decisión de usar un agente no autoriza órdenes peligrosas o navegar por cuentas sin consentimiento.

## Gestión de procesos
Antes de intervenir, usar inventario de servicios y directorios reales. Confirmar la diferencia entre proceso vivo, instalación, configuración, canal escuchando, encargo aceptado y trabajo concluido. Para rutas persistentes, probar reconexión tras reinicio cuando el usuario lo solicite y exista una recuperación fiable; un simple status no es prueba de persistencia.

## Integración con otras habilidades
organizaciondeltrabajo planifica; ingenieria-fiable prueba; bibliotecario-memoria recuerda; acceso_webs selecciona navegador/portal; control-laboratorio compone la secuencia sin duplicar código. No generar múltiples asistentes/servicios para suplir un permiso que el MCP realmente deniega: diagnosticar la barrera y mantener controles.

## Evidencia completa
Regresar con quién recibió el encargo, versión y canal, inicio y final reales, salida o artefacto, comprobación, gasto/cuota, pendientes. Cuando una delegación se queda «pending», no afirmar que se completó.
