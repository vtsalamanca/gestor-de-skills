# Índice operativo del Gestor de Skills (punto de entrada ligero)

**Vigente:** 2026-11-23 · **fuente:** repo canónico `vtsalamanca/gestor-de-skills`, rama publicada. **Evidencia:** L0 documentos y tests en Debian; NO demuestra activación espontánea en nuevos chats ni ejecución autenticada E2E.

## Algoritmo de entrada (30 segundos, sin cargar manuales enteros)
1. Identificar la tarea y su proyecto exacto; cargar `organizaciondeltrabajo` si no es trivial.
2. Seleccionar una única skill principal en la tabla; para trabajo de Debian usar antes `control-laboratorio`, y para cambios de software añadir `ingenieria-fiable`.
3. Buscar último hito en Bibliotecario por título real y, si la búsqueda es ambigua, pasar el ámbito del proyecto; verificar título e ID antes de hacer `brief`.
4. Abrir únicamente el SKILL.md y la referencia especificada; comprobar la lista `pending_knowledge` antes de tomar como vigente un `next_action` histórico.
5. Ejecutar, verificar efectos y registrar nueva lección con versión, evidencia y `supersedes` explícito. Sin coste extra ni traslado de trabajo al usuario.

## Tabla canónica de enrutamiento
| Skill | Versión empaquetada | Activación principal | Referencia | Situación de la prueba |
|---|---:|---|---|---|
| `organizaciondeltrabajo` | 0.2.27 | Planificar/retomar trabajo no trivial | `skills/organizaciondeltrabajo/SKILL.md` | L0 + escenarios |
| `control-laboratorio` | 0.2.7 | Debian/TPM2/Bibliotecario/servicios | `skills/control-laboratorio/SKILL.md y references/14-guia-rapida.md` | L0/L3; E2E total pendiente |
| `bibliotecario-memoria` | 0.3.10 | Recuperar, registrar, releer | `skills/bibliotecario-memoria/SKILL.md` | L0/L3 recuperación probada |
| `ingenieria-fiable` | sin versión individual | Reparación y pruebas de software | `skills/ingenieria-fiable/SKILL.md y references/actualizar-skills.md` | L0 + escenarios |
| `acceso_webs` | 0.5.7 | Web, sesiones, BrowserLearn | `skills/acceso_webs/SKILL.md` | L0 + escenarios |
| `buscar-comparar-productos` | sin versión individual | Productos, precios, historial público | `skills/buscar-comparar-productos/SKILL.md` | L0 + escenarios |
| `descubrir-skills` | sin versión individual | Buscar alternativas de habilidades | `skills/descubrir-skills/SKILL.md` | L0 |
| `auditar-skills` | sin versión individual | Seguridad/coste/licencia de habilidades | `skills/auditar-skills/SKILL.md` | L0 |
| `crear-skills` | sin versión individual | Diseñar habilidad y tests | `skills/crear-skills/SKILL.md` | L0 |
| `integrar-skills` | sin versión individual | Compatibilidad, plugin y Codex | `skills/integrar-skills/SKILL.md` | L0 |
| `inventariar-skills` | sin versión individual | Inventario de versiones y permisos | `skills/inventariar-skills/SKILL.md` | L0 |

## Enrutamiento obligatorio por intención (mínimos observables)
| Consulta de usuario | Skill principal | Añadir / procedimiento |
|---|---|---|
| actualiza el complemento | `control-laboratorio` | `ingenieria-fiable` → `actualizar-skills.md` vigente |
| publica el plugin sin ZIP manual | `ingenieria-fiable` | `publicacion-autonoma-complemento.md` |
| repara BrowserLearn | `acceso_webs` | `ingenieria-fiable` + referencia BrowserLearn |
| entra en InfoJobs | `acceso_webs` | `control-laboratorio` + LAB-AUTH |
| consulta Educamos | `control-laboratorio` | LAB-AUTH y automatizaciones |
| busca oferta en Amazon | `buscar-comparar-productos` | comprobación de vendedor y precio real |
| continúa el trabajo pendiente | `organizaciondeltrabajo` | `bibliotecario-memoria` → buscar/brief |
| qué hemos aprendido sobre FTS5 | `bibliotecario-memoria` | proyecto + procedencia + actualidad |
| Control Debian da error | `control-laboratorio` | Doctor + diagnóstico por capas |
| necesito una skill nueva | `descubrir-skills` | `auditar-skills`, luego `crear-skills` |
| inventaría herramientas | `inventariar-skills` | autorización específica para escrituras |
| comprueba versiones Codex | `integrar-skills` | marketplace/caché, lectura real |
| redacta pruebas de regresión | `ingenieria-fiable` | tests rojo/verde y postcondición |

## Precedencia y caducidad
- **Vigente**: SKILL.md actual + `actualizar-skills.md` vigente + evidencias verificadas. Un procedimiento viejo nunca reemplaza uno homologado solo porque un buscador devolvió su texto.
- **Histórico**: `actualizar-skills-historico.md`, `historico-operativo.md`, `lecciones-historicas-acceso.md`; consultar solo para investigar incidentes o rollback.
- **Procedencia**: cada corrección debe registrar ruta, commit/version, fecha, prueba, resultado y campo `supersedes` con ruta anterior. Las skills no ejecutan ni garantizan hooks automáticos.
- **Pruebas**: L0 sintaxis/enlaces/índice, L1 selección simulada, L2 lectura real, L3 ejecución autorizada, L4 nuevos chats. No confundir una L1 simulada con selección real del modelo en L4.

## Bibliotecario
Buscar con FTS5 local + prioridad de títulos y parámetro opcional `scope` para filtrar por proyecto (p. ej. `Buscar-Curro`), verificando siempre nombre completo; usar `brief` solo después de resolver ambigüedad. El índice FTS se prepara en memoria y no cambia la base existente. El algoritmo léxico no equivale a una búsqueda semántica.

## Cierre y registro
Si un flujo falla: diagnóstico por capa → solución comprobada → actualización de referencia → marcar anterior como sustituido → prueba de regresión → comprobación de distribución → registro idempotente y relectura.


## Evidencia de nuevas conversaciones y segundo ciclo de mejoras
- El 23/11/2026 el titular aportó informes de **dos conversaciones nuevas**: una validación guiada y otra petición ordinaria de retomar InfoJobs. Ambas declararon selección pertinente y carga 0.4.56. Son **informes facilitados por el usuario**, no trazas MCP independientes accesibles desde el repositorio; valen como indicio L4 acotado, no como ensayo automatizado de 26 casos.
- Banco actual: [26 casos positivos y negativos](eval_cases.jsonl); la herramienta [evaluador L4](../tools/eval_skill_routing.py) calcula precisión, recuperación y falsos positivos solo al recibir observaciones verificables. Sin observaciones indica `not_evaluated`.
- `brief.next_actions` es el historial; `brief.pending_knowledge` es la vista vigente. Cada resolución/sustitución/bloqueo requiere un hito posterior concreto, sin borrar checkpoint.
- Alias de proyecto y asociaciones de archivos son datos locales privados; código canónico en `bibliotecario-memoria/tools/vinculos_contexto.py`. Nunca publicar rutas privadas o correos.
- Reconciliaciones del Supervisor solo con prueba independiente; los `unknown` no se limpian mediante reintento. Copia y restauración de SQLite no certifican restauración VM.
- Procedimientos ampliados: [auditoría de segunda pasada](21-mejoras-revision-20261123.md).


## Cierre de incidentes Educamos y evaluación independiente · 23/11/2026
- El 20 y 21/11/2026 el servicio diario Educamos terminó con job_returned_error y resultado exit-code, verificado en journal de usuario con ventanas temporales concretas. Los dos registros se cerraron como failed_effects_unknown, no como succeeded ni not_applied. Cero reejecuciones y copia previa del Supervisor SQLite.
- El evaluador eval_skill_routing.py distingue procedencia (user_report o verified_tool_trace), versión e independencia de las conversaciones. Los informes previos 0.4.56 no certifican la versión actual. Los 26 casos están redactados, pero no se han ejecutado automáticamente en 26 conversaciones nuevas desde este chat. Prohibido declarar L4 completo basándose en fixtures o informes ajenos.


El evaluador comprueba integridad del JSONL y correspondencia entre llamadas reales listadas y habilidades declaradas, **pero no dispone de firma de procedencia oficial del servicio ChatGPT**. El operador tiene que comprobar que el archivo proviene de un registro auténtico del chat; una huella SHA-256 no distingue material falsificado de material legítimo.

Desde 0.4.59, el evaluador rechaza trazas vacías y reconoce el identificador `skill://` que devuelve la lectura del complemento privado vigente, además del formato anterior. En un caso negativo, la fuente debe acreditar la cobertura del turno completo, aunque no haya lecturas de habilidades. Una captura parcial o el historial de un conector externo solo acreditan los eventos que muestran. Para puntuar conversaciones de una release anterior con el evaluador corregido, indicar su versión con `--version`.
