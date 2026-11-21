# Inventario operativo individual de herramientas de Control Debian

## Finalidad
Esta referencia conduce al **inventario local completo**, separado del manual metodológico: una ficha por cada operación MCP anunciada en el catálogo del chat, con nombre, descripción declarada, categoría, posible efecto, fecha y estado de prueba. No confundir «el conector expone 81 herramientas» con «las 81 están probadas y autorizadas».

**Fuentes locales** (no subir a GitHub):
- $HOME/utilidades/control-laboratorio/inventario-mcp.md: vista legible con una fila por operación.
- $HOME/utilidades/control-laboratorio/inventario-mcp.json: datos estructurados.
- $HOME/utilidades/control-laboratorio/herramientas-expuestas.tsv: captura de nombres y descripciones visibles en un chat.
- $HOME/utilidades/control-laboratorio/evidencias.json: verificaciones reales limitadas a un caso y fecha.

**Código versionado**: $HOME/proyectos/gestor-de-skills/skills/control-laboratorio/tools/inventario_herramientas.py. Solo requiere Python estándar, no realiza llamadas remotas ni lee llaveros.

## Prioridad de evidencia en otro chat
1. **Descubrimiento actual:** consultar primero las funciones y contratos efectivamente expuestos en la conversación presente. Un archivo de Debian puede describir otra sesión o versión.
2. **Inventario local:** recuperar fecha de captura, número de herramientas, SHA-256 de origen, grupos y limitaciones. Preferir consulta de la herramienta buscada frente a volcar la lista entera.
3. **Comparación:** detectar herramientas nuevas, eliminadas o renombradas; descripciones y argumentos podrían cambiar aunque persista el nombre. Una cifra histórica del servidor NO garantiza herramientas visibles en ChatGPT.
4. **Verificación operativa:** para actuar, usar la herramienta de menor privilegio, revisar su contrato, ejecutar solo la operación autorizada y verificar su postcondición. Registrar únicamente ese alcance de prueba.
5. **Actualización:** cuando sea necesario renovar el inventario, capturar desde la sesión realmente conectada los nombres exactos y las descripciones visibles, sin inventar nombres desde prefijos. Preparar TSV UTF-8: nombre, tabulador, descripción en una línea por herramienta.
6. **Comparación previa:** ejecutar generador en modo de lectura, comprobar recuento, duplicados, altas, bajas y resumen; grabar con --write tras validación. Para bajas inesperadas, detener; usar --allow-removals solo si están justificadas. No programar un cron ni ejecutar comprobaciones masivas para mantenerlo.

## Consulta habitual sin modificaciones
- Abrir el Markdown local y buscar el nombre concreto.
- Para ver recuento y fecha sin exponer el inventario completo, consultar las claves captured_at y total de inventario-mcp.json mediante Python o jq disponible.
- Si Debian o MCP no está accesible, informar del bloqueo y recuperar documentación general en GitHub; no afirmar que ese inventario es actual.

## Generación reproducible (presupuesto adicional 0 €)
Desde el repositorio Debian del Gestor de Skills, usar:

    python3 skills/control-laboratorio/tools/inventario_herramientas.py --input "$HOME/utilidades/control-laboratorio/herramientas-expuestas.tsv" --output-dir "$HOME/utilidades/control-laboratorio" --captured-at "FECHA-REAL-ISO8601-CON-ZONA" --expected-count NUMERO_OBSERVADO

El comando anterior es una plantilla: reemplazar hora y número por datos **realmente observados** en esta captura, no copiar fechas antiguas. Sin --write solo produce diagnóstico. Añadir --write después de validarlo para emitir inventario-mcp.json y inventario-mcp.md con reemplazo atómico y permisos privados. Puede añadirse --evidence RUTA_JSON para enlazar exclusivamente pruebas acreditadas.

El programa compara con la captura anterior y rechaza vacío, duplicados, nombres inválidos, recuentos incongruentes y bajas no autorizadas. No genera respaldos acumulativos; la fuente Git conserva el generador y las pruebas.

## Evidencias separadas de la visibilidad
evidencias.json usa schema_version: 1 y un objeto checks indexado por nombre real de herramienta. Cada prueba lleva result (verificada / parcial / fallida), checked_at (ISO8601 con zona) y scope (qué operación y postcondición se comprobaron). Ejemplo: verificar estado de Debian **no** valida escritura genérica, gestos gráficos ni autenticación privada.

La relectura de un resultado con ticket puede acreditar la consulta tipada. Un error de transporte o denegación no equivale a funcionalidad inexistente. Las verificaciones no autorizan nuevos usos ni sustituyen los permisos de la sesión.

## Evaluación de eficiencia MCP (no destructiva)

El script propio `skills/control-laboratorio/tools/eficiencia_mcp.py` analiza el inventario JSON anterior sin conectarse a servicios ni tocar la configuración. La estimación `name_description_proxy_tokens` se calcula únicamente a partir de la longitud de nombre y descripción dividida entre cuatro. **No es el consumo real de tokens ni incluye esquemas JSON, prompts de sistema ni contexto de ChatGPT**; se utiliza para priorizar revisiones, no para justificar costes o desconexiones.

Ejemplo de lectura, con el inventario existente (no actualiza datos):

    python3 skills/control-laboratorio/tools/eficiencia_mcp.py --inventory "$HOME/utilidades/control-laboratorio/inventario-mcp.json"
    python3 skills/control-laboratorio/tools/eficiencia_mcp.py --inventory "$HOME/utilidades/control-laboratorio/inventario-mcp.json" --format json

Uso opcional observado: JSON local **saneado**, generado explícitamente a partir de una sesión conocida, con `{"schema_version":1,"scope":"sesion observada","complete":false,"counts":{"read_file":2}}`. El campo `complete` solo puede ser verdadero si la cobertura de llamadas de ese ámbito es demostrable. Si está ausente o es falso, las herramientas no mencionadas son **desconocidas**, no «nunca usadas». El informe no guarda datos ni habilita permisos, y no interpreta como prescindible una herramienta de contingencia.

Revisar un grupo muy extenso no equivale a desinstalarlo: distinguir conectores de recuperación y operaciones críticas, confirmar contratos y medir el coste real solo con métricas oficiales disponibles. No modificar auto-connect ni herramientas MCP sin aprobación diferenciada. Código y tests del análisis son propios: no se incorpora código de terceros ni una nueva skill separada.

## Seguridad y alcance
- La lista representa únicamente el conector Control Debian; no inventariar aquí todos los conectores de ChatGPT ni los paquetes instalados en Linux.
- Nunca incluir cookies, tokens, contraseñas, OTP, datos de menores, CV, direcciones privadas, argumentos sensibles ni configuraciones completas.
- No usar las funciones genéricas del conector como vía lateral para permisos denegados. No afirmar que todas están homologadas porque se ve su nombre.
- El inventario no reinicia servicios, cambia el MCP, crea permisos, activa API de pago, sincroniza el plugin ni observa continuamente el chat.
- Los programas y servicios Debian siguen en el catálogo local general; el documento de familias de la skill sirve para elegir el grupo de función.

## Aceptación y vuelta atrás
Comprobar 1 registro por nombre efectivamente anunciado, integridad SHA del TSV, fecha con zona, recuento, permisos 0600 de JSON/Markdown, tabla legible y ausencia de duplicados. Ante error no reemplazar el inventario previo; corregir la captura y volver a comprobar. Mantener en GitHub solo código genérico y guías, sin publicar el snapshot del usuario.
