---
name: acceso_webs
description: Investiga estrategias autorizadas de acceso a sitios web, autenticación y sesiones, extracción eficiente y diseño de conectores reutilizables; prioriza bajo consumo computacional y presupuesto adicional cero.
version: 0.1.1
---
# acceso_webs — acceso, extracción y conectores eficientes

## Propósito
Skill evolutiva que incorpora el conocimiento previamente trabajado bajo el concepto «autenticarse», ampliándolo a investigación de fuentes web, formas de acceso, extracción, diseño de conectores, autenticación y reutilización documentada. El archivo original «autenticarse» no ha sido localizado y **no se afirma haber migrado su contenido íntegro**. Recuperarlo cuando aparezca, comparar y fusionar sin sobrescribir hallazgos.

## Activación
Aplicar cuando haya que investigar un portal, comprender cómo obtener datos, iniciar o mantener acceso legítimo, diseñar un conector, corregir scraping/paginación o mejorar un recolector existente. Coordinar con `organizaciondeltrabajo` e `ingenieria-fiable`.

## Restricciones
- Presupuesto adicional por defecto **0 €**. No ejecutar servicios, APIs ni plugins de pago por uso, incluso con créditos promocionales, sin conocer tarifa, saldo y coste estimado y autorización explícita para esa operación. Si coste incierto, no ejecutar.
- No eludir controles de acceso, CAPTCHA, MFA, bloqueos, permisos ni salvaguardas; respetar privacidad, legalidad y condiciones aplicables. Nunca almacenar credenciales, cookies, tokens o datos personales sensibles en skills, GitHub, logs o ejemplos.
- No confundir una página visible con cobertura completa, ni un resultado HTTP 200 con extracción correcta. Diferenciar documentación oficial, observación, inferencia e hipótesis.
- No habilitar tareas programadas ni conexiones externas persistentes sin autorización.

## Puerta previa de eficiencia
1. Recuperar los conectores, procedimientos y fallos previos, código, estado del repositorio y evidencias para evitar repetir trabajo.
2. Inventariar herramientas **realmente disponibles** (conectores propios, GitHub, Python/HTTP, navegador, Firecrawl u otros) y comparar capacidad, límites, privacidad, fiabilidad, mantenimiento, tarifas, cuota y **consumo computacional**.
3. Elegir el método más ligero que satisfaga los criterios: a) datos oficiales exportables / feed / API pública gratuita y permitida; b) peticiones HTTP de HTML, JSON o XML accesibles; c) análisis selectivo de páginas y JavaScript; d) navegador automatizado para interacción imprescindible; e) herramientas/agentes de investigación o extracción especializados solo cuando den ventaja comprobable y coste autorizado.
4. Priorizar estrategias incrementales: caché validada, ETag/Last-Modified, intervalos prudentes, campos mínimos, paginación acotada, deduplicación, límites de tamaño/tiempo, lotes y reintentos limitados con backoff. Medir peticiones, páginas, tiempo de CPU, memoria, tráfico, minutos runner y esfuerzo humano.
5. Antes de escribir un conector nuevo, comprobar si existe un método o biblioteca reutilizable, y si una inspección local o una captura única de respuestas resuelve la duda.

## Investigación de acceso a una web
Documentar URL de origen, dominio, rutas, estructura, enlaces, mapa de sitio, filtros, parámetros, paginación, contenido estático/dinámico, cambios observados, autenticación necesaria, límites y evidencia. Las API internas observadas en herramientas de desarrollo no se consideran API públicas documentadas: verificar permiso, estabilidad, mantenimiento y seguridad antes de usarlas.

Separar las capas: descubrimiento de URLs, obtención, autenticación/sesión, parseo, normalización, deduplicación, persistencia, informes y alertas. Diagnosticar cada fallo en su capa y no repetir pruebas sin hipótesis nueva.

## Autenticación y sesiones — conocimiento recuperado de Educamos
- En Educamos Puente se trabajó con WebView Android y sesiones autenticadas de EducamosCLM; conservar y reutilizar **una sesión válida dentro de su contexto autorizado** puede reducir accesos repetidos.
- Antes de automatizar, verificar duración de sesión, expiración, cambios de dispositivo, redirecciones, CSRF y renovación ordinaria de credenciales.
- Distinguir lo que el usuario comunicó o se investigó de lo efectivamente probado. No afirmar que el procedimiento WebView funciona universalmente.
- Priorizar OAuth, interfaces oficiales y autorización interactiva del titular cuando existan; evitar guardar secretos o copiar sesiones entre usuarios/dispositivos sin garantías.

## Caso de referencia prioritario: pasarela Educamos Puente / EducamosCLM (octubre de 2026)

**Objetivo de conservación:** no repetir el coste en tiempo humano, ejecuciones de GitHub Actions, inspecciones de JavaScript y experimentos de navegación que exigió el proyecto. Esta sección conserva evidencia histórica resumida, sin credenciales ni datos escolares identificativos. Antes de cambiar el método, recuperar código, APK, resultados y diagnósticos ya existentes.

### Evidencias históricas comunicadas como comprobadas
- **Navegación dentro de una misma pestaña autenticada:** EducamosCLM → Seguimiento Educativo → Mensajería → «Todos» permitió leer cinco mensajes completos y marcar su lectura, con confirmación desde el portal. Fallar al enumerar pestañas **no significa** necesariamente perder acceso; la continuidad de pestaña/contexto fue una clave.
- **WebView Android con vista de escritorio:** configurar ancho de escritorio de aproximadamente 1280 px reveló secciones que la vista móvil de aproximadamente 373 px ocultaba, incluida navegación hacia mensajería. La presencia de enlaces o botones **no confirma por sí sola** la apertura o extracción de mensajes.
- **Pasarela Android:** se comunicaron recuperaciones de texto y detección de adjuntos en una versión 0.16, así como la descarga de un PDF de 133278 bytes. La descarga de un DOC falló. No extrapolar un éxito parcial a otros formatos ni al funcionamiento extremo a extremo.
- **Prueba de conectividad desde GitHub a Cerbero:** una petición HTTP devolvió 200 y contenido HTML sin formularios; esto acredita conectividad, **no** que funcione un inicio de sesión por HTTP, una API interna o un endpoint de mensajes.

### Incidencias y explicaciones alternativas que no debemos volver a pasar por alto
- En vista móvil pueden quedar ocultos controles; comprobar diseño responsivo, estado del DOM, cambios JavaScript y diferencias entre interfaces antes de atribuirlo a permisos.
- Errores JavaScript (por ejemplo TypeError relacionado con `filter`), respuestas 404 y fallos de consola no prueban por sí solos que el usuario no esté autenticado: correlacionar URL, estado de sesión y contexto de ejecución.
- Distinguir: navegador/sesión ya autorizados, WebView con su propio almacén de sesión, conectividad de GitHub Actions y endpoints internos. **No asumir que compartir red equivale a compartir autenticación**.
- Rutas observadas históricamente como `/s/home`, `/back/...` y redirecciones de Cerbero son **pistas incompletas**, no contratos de API ni recomendaciones para invocar endpoints no verificados.

### Procedimiento mínimo reutilizable
1. **Recuperar evidencia existente:** versión exacta del APK/código, estado de navegación, logs depurados y pruebas; verificar antes de volver a instrumentar. No ejecutar un APK no auditado ni extraer secretos.
2. **Probar primero continuidad de contexto:** dentro de la pestaña/sesión autorizada, localizar ruta visible a mensajería y confirmar contenido real; evitar reiniciar acceso cuando la sesión sigue válida.
3. **Si faltan controles:** contrastar modo móvil/escritorio y anchura del WebView; documentar una captura y estructura DOM saneadas. No repetir muchos experimentos sin hipótesis concreta.
4. **Diferenciar las capas:** acceso inicial y federado, persistencia de sesión, redirección, carga dinámica, visualización, lectura, descarga de adjunto y marcado; validar cada una por separado.
5. **Para automatización:** priorizar UI/WebView autorizado que ya funciona o interfaz oficial estable; evaluar HTTP solo con evidencia de que recupera datos reales dentro de un mecanismo permitido. No convertir un 200 de login en «API validada».
6. **Para archivos:** verificar contenido, tamaño, tipo MIME, nombre y apertura; probar PDF/DOC por separado y no atribuir éxito a todos los adjuntos.
7. **Para diagnóstico:** recopilar una sola vez la evidencia mínima sanitizada (URL sin parámetros sensibles, códigos, tipo de contenido, contador de elementos y trazas reducidas); después analizar localmente y en lote, sin ciclos repetitivos commit → runner → log.
8. **Para integración:** crear pruebas locales con fixtures falsos, probar bajo condiciones controladas y reservar una validación remota única para incertidumbres propias de red, sesión o entorno. Repetir solo ante nueva hipótesis.
9. **Para cerrar:** exigir recuperación de mensajes correctos, cobertura verificable, metadatos/adjuntos procesados según requisito, y evidencia real de las acciones de lectura; publicar solo resultados necesarios, nunca datos personales.

### Pendientes no demostrados
No constan como verificados un API HTTP directa de mensajería, la recuperación de cookies entre dispositivos, el endpoint final reutilizable, el funcionamiento general de un extractor externo ni un diagnóstico técnico completo del APK `Educamos_Puente_16.apk`. Investigar solo cuando sea necesario, con una prueba concreta y coste contrastado.

### Registro de coste y aprendizaje
En cada alternativa anotar **peticiones, minutos de ejecución, iteraciones, intervención humana, tasa de éxito y coste monetario/cuota**; si no hay cifras fiables, marcar «no medido». Registrar siempre qué estrategia quedó descartada y por qué, para impedir que futuras sesiones repitan la misma investigación.

## Construcción de conectores reutilizables
Definir contrato de entrada/salida, esquema de campos, procedencia/fecha, errores tipificados, reintentos, checkpoints e idempotencia. Aislar adaptadores por portal y compartir transporte HTTP, validación, normalización y observabilidad. Incluir tests con fixtures sin secretos, ejemplos sintéticos, condiciones de suspensión y alternativa manual autorizada.
La operación diaria debe poder ejecutarse con recursos gratuitos cuando sea viable y sin depender del servicio usado para investigar el portal.

## Evidencias y criterio de verificación
Para cada sitio registrar: fuente | URL | mecanismo | autenticación | paginación/cobertura | campos | consumo por ejecución | herramientas evaluadas | restricciones | prueba y fecha | confianza | próximo paso.
Estados obligatorios: HIPÓTESIS, DOCUMENTADO, PROBADO LOCALMENTE, VALIDADO EN ORIGEN, VALIDADO EXTREMO A EXTREMO, BLOQUEADO. No declarar cobertura total si las páginas o respuestas no se comprobaron exhaustivamente.

## Ejemplos y lecciones
- **Buscar-Curro:** evaluar extracción HTTP y paginación con pruebas controladas antes de probar navegador o Firecrawl; para Eurofirms/Randstad y portales con paginación desconocida conservar expresamente el nivel de cobertura demostrado. Comparar Firecrawl como herramienta *candidata*, nunca asumir acceso, gratuidad ni capacidad de API interna.
- **Educamos:** investigar WebView y conservación de sesiones existentes con consentimiento, evitando almacenar secretos y evitando iteraciones de GitHub Actions como laboratorio.
- **Subastas:** favorecer datos públicos oficiales estructurados y trazabilidad de anuncios/documentos frente a navegación intensiva.

## Aprendizaje y distribución
Al resolver un problema, registrar estrategia validada y métricas, añadir un caso reproducible genérico y extraer patrones a la skill; evitar guardar detalles operativos sensibles del sitio o credenciales. Mantener este repositorio como fuente canónica. Después de cambios, validar, versionar y publicar en el mismo plugin privado y marketplace de Codex cuando existan herramientas/permisos, sin confundir commit con despliegue.
