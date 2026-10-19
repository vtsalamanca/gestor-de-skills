---
name: organizaciondeltrabajo
description: Metodología general predeterminada de planificación y ejecución eficiente. Aplicar al iniciar, retomar, organizar o cambiar de fase de un trabajo no trivial: recuperar contexto y skills, elegir entorno de menor coste, agrupar pruebas, continuar hasta bloqueo real y verificar resultados. Presupuesto adicional cero.
version: 0.2.5
---
# &organizaciondeltrabajo — metodología general

## Alcance y activación
Aplicar proactivamente al iniciar, retomar o cambiar de fase de tareas no triviales, si el entorno permite descubrir esta skill. Esta declaración NO garantiza invocación automática desde todos los chats o proyectos: se complementa con instrucciones personalizadas y de proyecto. Para cuestiones triviales, omitir ceremonia.

**Fuente única de verdad:** `vtsalamanca/gestor-de-skills/skills/organizaciondeltrabajo/SKILL.md`. Esta versión consolida la línea 0.1.0–0.1.6 del repositorio y las mejoras 0.2.0 del plugin. ChatGPT y Codex pueden usar copias empaquetadas o cacheadas, pero deben reproducir este archivo canónico; un Markdown en GitHub no se instala ni se actualiza automáticamente.

## Misión y garantías
Conseguir resultados fiables y verificables con el menor gasto razonable de tiempo del usuario, operaciones manuales, créditos, cuotas y dinero. Presupuesto adicional por defecto **0 €**. Nunca utilizar servicio/API/plugin/ejecutor de pago por uso, aun con saldo promocional, sin comprobar tarifa, saldo y coste estimado y obtener autorización expresa por operación. Si coste desconocido, bloquear. No comprometer calidad, seguridad, legalidad ni verificabilidad por ahorrar.

## Puerta de eficiencia antes de actuar
1. Recuperar objetivo, limitaciones, autorizaciones, estado maestro y decisiones previas; examinar primero resultados, pruebas, archivos y repositorios. Distinguir VERIFICADO, COMUNICADO, HIPÓTESIS, PENDIENTE, BLOQUEADO y DESCARTADO.
2. Descubrir skills y conectores **realmente disponibles** para este entorno, revisar permisos y coste antes de inventar soluciones. No suponer que Chat, Codex y Work comparten capacidades. Reutilizar código/librerías compatibles previa auditoría de licencia, seguridad y mantenimiento.
3. Elegir la ruta de menor **coste total efectivo**, incluyendo minutos, créditos, riesgo y esfuerzo del usuario: (a) razonamiento/inspección en Chat; (b) análisis estático y prueba local o simulada; (c) API/feed oficial público y gratuito; (d) HTTP HTML/JSON autorizado; (e) navegador local/runner cuando sea imprescindible; (f) Codex para programación compleja; (g) Work para interacción gráfica excepcional. Orden adaptable a las necesidades técnicas, no rígido.
4. En proyectos de software, estudiar si una inspección o prueba local resuelve la duda antes de crear workflow. **No usar GitHub Actions como laboratorio iterativo** cuando pruebas locales o análisis en lote den la misma evidencia.
5. Definir entregable, criterios de aceptación, dependencias, seguridad, plan de pruebas y reversión; agrupar las comprobaciones que responden a una misma hipótesis. No generar un commit, workflow y ejecución por una búsqueda simple de texto.
6. Preguntar al usuario solo por autorizaciones o decisiones realmente imprescindibles; evitar ciclos ceremoniales «ya / vale» cuando haya trabajo independiente realizable. Continuar hasta objetivo logrado o bloqueo real.

## Puerta reforzada de descubrimiento y comparación de herramientas (lección Firecrawl)
Antes de implementar una solución nueva, cambiar de herramienta o realizar otra serie de pruebas ante un bloqueo:
1. Consultar **una vez por bloque de trabajo** el inventario actual de skills, plugins, conectores, código, repositorios y herramientas del entorno real (Chat, Codex, Work o local); comprobar su disponibilidad y alcance. Reutilizar inventarios ya válidos, sin búsquedas redundantes.
2. Comparar al menos la solución ya existente y alternativas pertinentes de bajo consumo: API/feed oficial gratuito, HTTP HTML/JSON, librería o conector propio, análisis local, navegador, Firecrawl u otra herramienta especializada *solo como candidata*. Comprobar antes límites, mantenimiento, privacidad, licencia, permisos, tarifas, saldo, estimación de consumo y cobertura.
3. Seleccionar el método por **coste total efectivo** (dinero, créditos, CPU, memoria, ancho de banda, minutos de GitHub Actions, mantenimiento, fiabilidad y tiempo/intervención del usuario), no por comodidad ni popularidad. Herramienta de investigación puede ser distinta del conector de producción; priorizar producción ligera y autónoma.
4. Si una serie de fallos no converge, **detener el procedimiento repetitivo** y revisar la capa afectada, la hipótesis y las alternativas que aún no se evaluaron; agrupar experimentos discriminantes y comparar antes de otra ejecución.
5. Registrar de modo compacto `problema | herramientas disponibles y evaluadas | opción seleccionada | opciones descartadas y motivo | prueba | coste/cuota estimada o medida | nuevo conocimiento reutilizable`. No dar por evaluado algo solo porque figura instalado.
6. Para acceso a webs, autenticación, scraping y desarrollo de conectores, consultar `acceso_webs` cuando esté disponible; sus patrones genéricos prevalecen sobre repetir experiencias específicas de proyectos. Si no está cargada, consultar la fuente canónica o seguir las pautas de esta skill.
**Límite:** descubrir/comparar no implica autorización para ejecutar servicios con tarifas por uso; presupuesto adicional 0 € hasta permiso concreto.

## Distribución de trabajo
- **Chat:** coordinación, contexto, investigación, análisis, decisiones, documentación y consultas mediante conectores disponibles; opción inicial.
- **Análisis local:** inspección, pruebas estáticas, fixtures sintéticos, extracción de datos y depuración sin servicios externos cuando estén disponibles. No prometer acceso a PC si no está autorizado.
- **Codex:** implementación, refactorización y pruebas que justifiquen su cuota; agrupar un encargo coherente.
- **Work:** flujos UI/navegador y operaciones complejas que no tengan alternativa suficiente; no usar por rutina ni cambiar de modo sin intervención del usuario.
- **GitHub:** código, historial, fuente de verdad, integraciones y automatización definitiva; CI puntual tras validación local. GitHub público no significa que los datos escolares, credenciales o logs deban ser públicos. Secreto en repositorio público requiere revisar el código ejecutado y limitar permisos.

## Desarrollo local primero y validación remota selectiva
Cuando exista acceso local autorizado, inspeccionar estado de Git, rama y commit antes de editar; no sobrescribir cambios locales y preferir una única copia enlazada al repositorio. Implementar y probar primero localmente con linters, tests, fixtures, mocks y simulaciones reutilizables. Reservar GitHub Actions u otros runners para evidencia que no pueda obtenerse localmente —entorno, red, permisos, persistencia o integración— y evitar reejecuciones idénticas sin una hipótesis nueva. Registrar qué verificó cada prueba local y remota. La operación diaria definitiva puede seguir en un runner incluido si ése es el diseño acordado; no introducir llamadas a modelos, credenciales, cron ni gasto sin autorización. El trabajo local reduce iteraciones y minutos remotos, pero no implica por sí mismo menor cuota de Codex.

## Autocomprobación de versión al iniciar trabajos
Al comenzar cada **sesión o bloque de trabajo no trivial** en que se utilicen las skills de este repositorio, comprobar **como máximo una vez por sesión de trabajo**, cuando GitHub y la metadata del plugin sean accesibles sin coste adicional, si la fuente canónica en `main` y la release privada instalada coinciden. Priorizar comparar manifiestos/versiones; si difieren o existe incertidumbre material, comparar también contenido/hash antes de publicar. Reutilizar el resultado durante la sesión y no consultar en cada mensaje.
- Si están alineadas, continuar con el trabajo sin interrumpir al usuario.
- Si GitHub es más reciente, intentar en el mismo flujo la publicación bajo demanda mediante la herramienta oficial Plugin Creator, conservando identidad, permisos y control de release; pedir una intervención únicamente si es realmente imprescindible.
- Si falta acceso, el coste no está acreditado, la publicación falla o las sesiones requieren recarga, continuar con la versión disponible cuando sea seguro y comunicar claramente el estado pendiente.
- No actualizar a ciegas ni entrar en bucles autorreferenciales: tras publicar, **una sola verificación** de la release; si falla, detener reintentos hasta obtener una hipótesis nueva.
- No hacer una comprobación remota en tareas triviales ni cuando el usuario prohíba consultas externas. No activar tareas programadas, GitHub Actions ni gastar créditos de Work/Codex para esta revisión.
Esta regla es una instrucción para el asistente que **carga** la skill: no constituye un servicio en segundo plano, no garantiza ejecución en chats donde la skill no esté disponible y no puede hacer que una caché se actualice por sí sola.

## Publicación y sincronización obligatoria de skills
Tras cualquier modificación autorizada de una skill canónica en `vtsalamanca/gestor-de-skills`, incluir en el mismo trabajo la distribución y verificación sin necesitar una segunda solicitud:
1. Comparar `main` con la release del plugin privado ChatGPT/Work y con el marketplace de Codex; identificar diferencias por contenido, no solo por número de versión.
2. Validar estructura, seguridad, cambios, reversibilidad y coste adicional (por defecto 0 €). Incrementar versiones de skill y paquete de forma coherente cuando corresponda.
3. Si las herramientas y permisos disponibles lo permiten, preparar el paquete desde GitHub y actualizar el **mismo plugin privado**, conservando su identidad, con control de concurrencia por ID de release; nunca afirmar que un commit de GitHub actualiza por sí solo ChatGPT/Work.
4. Verificar publicación y contenido de los archivos distribuidos; cuando sea posible comprobar la carga en una sesión nueva y el marketplace Codex. Distinguir `FUENTE_ACTUALIZADA`, `PLUGIN_PUBLICADO`, `CARGA_VERIFICADA` y `PENDIENTE`.
5. Si publicar o comprobar exige otra herramienta, permiso, tarifa desconocida o servicio de pago, no ejecutarlo; comunicar el bloqueo concreto, el siguiente paso mínimo y la versión que continúa activa. Nunca marcar la sincronización como completada sin evidencia.
No prometer ejecución desatendida ni actualización instantánea de sesiones/cache. Esta regla aplica a cualquier skill del repositorio y complementa las instrucciones generales del usuario.

## Flujo de coordinación y aprendizaje
**A. Recuperar:** consultar `ESTADO_PROYECTO.md` o registro equivalente, decisiones y pruebas; resolver contradicciones.
**B. Planificar:** objetivo medible, restricciones, fuentes necesarias, criterios de aceptación y bloques según dependencias. En recolectores auditar fuentes antes de programar: URL, método, cobertura, autenticación, evidencia, estado y limitaciones; no exigir resolver todas si la exclusión está justificada.
**C. Ejecutar:** cambios mínimos y reversibles; agrupar diagnóstico + pruebas; no duplicar entre conversaciones. Si aparece fallo, aislar capa (origen/red/autenticación/extracción/deduplicación/almacenamiento/entrega), buscar causa y probar hipótesis falsable; máximo un reintento ante fallo transitorio salvo nueva evidencia.
**D. Verificar:** distinguir diseñado, guardado, ejecutado, probado localmente y validado extremo a extremo. No afirmar éxito por existir archivo, commit, HTTP 200 o workflow verde sin comprobar el objetivo real. Fecha, versión y evidencia.
**E. Aprender:** registrar causa de repetición o desperdicio, mejora medible y comparación esfuerzo previsto/real; proponer incremento de versión sin alterar silenciosamente criterios esenciales.

## Escalera para recolectores
1. API/feed oficial público gratuito documentado; 2. HTTP autorizado con HTML/JSON/XML; 3. navegador automatizado solo cuando la interacción JavaScript sea imprescindible; 4. agente visual/Work solo excepciones. Registrar evidencia real, reintentos limitados, paginación, cuotas y límites de tiempo/tamaño. No confundir JSON público con API documentada; no eludir controles de acceso.

## Tres conversaciones por proyecto cuando ayuden
`01 · CHAT — Dirección`; `02 · CODEX — Desarrollo`; `03 · WORK — Operaciones`. Al transferir tareas llevar ID, objetivo, estado, rutas, límites, autorizaciones y pruebas; al volver actualizar estado maestro. No es obligación crear hilos nuevos si solo añade fricción.

## Registro mínimo
`ID | Proyecto | Objetivo | Entorno | Estado | Evidencia | Dependencias | Coste autorizado | Siguiente paso`.
Continuar automáticamente al siguiente bloque permitido después de cada hito. Parar únicamente por objetivo terminado, decisión/credencial/autorización necesaria, riesgo, o límite técnico real. No prometer actividad en segundo plano sin tarea programada.

## Ingeniería técnica especializada
Cuando haya programación, fallos, pruebas o despliegues, consultar **`ingenieria-fiable`** y sus referencias para ciclo rojo-verde-refactor, diagnósticos por capas, pruebas y compuerta de verificación. Esta skill coordina la elección de herramientas y recursos; `ingenieria-fiable` profundiza en comprobación técnica, evitando duplicación.

## Caso aprendido: Educamos, octubre 2026
Se realizaron demasiados ciclos manuales de editar Python en GitHub → commit → GitHub Actions → log para localizar partes de JavaScript. Antes de repetir ese patrón: recuperar el APK/código y JS disponible, analizar estáticamente/localmente, agrupar hipótesis y pruebas, reservar GitHub Actions para verificar integración y funcionamiento diario. Considerar tiempo y clics del usuario como recurso; evitar optimizar minutos gratis a costa de esfuerzo humano.

## Historial
- 0.2.5 (19 oct 2026): puerta reforzada para detectar alternativas disponibles antes de programar o repetir diagnósticos; integración metodológica con acceso_webs.
- 0.1.0–0.1.5 (18 oct 2026): protocolo original en `vtsalamanca/Buscar-Curro`; continuidad, auditoría de fuentes, elección HTTP/API y descubrimiento de capacidades.
- 0.1.6 (19 oct 2026): desarrollo y pruebas locales primero; validación remota selectiva y medición del coste total.
- 0.2.0 (19 oct 2026): integración en Gestor de Skills; activación proactiva donde sea posible, puerta obligatoria de eficiencia, preferencia local, caso Educamos y enlace a ingenieria-fiable.
- 0.2.1 (19 oct 2026): unificación de 0.1.6 y 0.2.0; GitHub pasa a ser la fuente única de verdad y las copias empaquetadas deben reproducirla.
- 0.2.2 (19 oct 2026): la fuente canónica se integra en el paquete completo de GitHub y se distribuye mediante su marketplace.
- 0.2.3 (19 oct 2026): publicación y verificación de plugin incorporadas como fase obligatoria de cambios en skills.
- 0.2.4 (19 oct 2026): autocomprobación al iniciar trabajos, una vez por sesión, con actualización bajo demanda y límites antibucle.
