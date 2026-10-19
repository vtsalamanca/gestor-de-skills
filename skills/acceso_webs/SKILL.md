---
name: acceso_webs
description: Investiga estrategias autorizadas de acceso a sitios web, autenticación y sesiones, extracción eficiente y diseño de conectores reutilizables; prioriza bajo consumo computacional y presupuesto adicional cero.
version: 0.2.0
---
# acceso_webs — acceso, extracción y conectores eficientes

## Propósito
Metodología transversal de investigación de fuentes web, autenticación autorizada, extracción y diseño de conectores. Generaliza el aprendizaje acumulado en proyectos anteriores sin incorporar dependencias, rutas o supuestos exclusivos de una web. La habilidad original «autenticarse» no fue localizada; no se afirma una migración íntegra.

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

## Estrategia universal para portales, sesiones y aplicaciones web

**Principio:** generalizar mecanismos, no rutas, nombres de botones, códigos de error ni peculiaridades de una plataforma. No asumir que lo observado en un proyecto funcionará en otros: plantear hipótesis y validarlas con una prueba mínima.

### Árbol de diagnóstico reutilizable
1. **Recuperación:** identificar evidencias, capturas, versión de código, rutas ya examinadas, errores y resultados anteriores. Reutilizar y sanear los datos; no repetir búsquedas o ejecuciones.
2. **Contexto de acceso:** distinguir sesión existente de inicio de sesión, pestaña de navegador, WebView, navegador remoto, cliente HTTP y runner. Verificar continuidad de la sesión autorizada antes de reiniciarla. Conectividad de red, sesión autenticada y autorización de datos son propiedades diferentes.
3. **Interfaz adaptativa:** ante controles aparentemente ausentes, comparar viewport, modo móvil/escritorio, DOM accesible, scripts y navegación responsiva, sin concluir de inmediato que falla la autenticación.
4. **Identidad y redirecciones:** verificar el circuito permitido de login/federación, renovación de sesión, expiración, redirecciones y restricciones CSRF. Usar acceso interactivo del titular y mecanismos oficiales; no exportar cookies ni tokens a entornos de terceros.
5. **Transporte y contenido:** distinguir DNS/red, HTTP, redirecciones, documento HTML, carga JavaScript, peticiones autorizadas y extracción del dato final. HTTP 200 verifica una respuesta, no la presencia del dato ni que una API esté habilitada.
6. **Extracción:** comprobar el dato objetivo, campos, paginación y cobertura, formatos de archivo, MIME, tamaño, apertura, duplicados y errores parciales. Validar cada formato y acción por separado; no generalizar éxitos.
7. **Pruebas con hipótesis:** aislar la capa que falla; conservar un conjunto mínimo de evidencias saneadas y crear fixtures locales sin datos reales. Agrupar pruebas y ejecutar una sola validación remota cuando realmente haga falta; repetir únicamente con hipótesis nueva.
8. **Operación eficiente:** una vez demostrado el método, construir un conector mínimo, incremental, con caché, límites y métricas. Preferir las vías más ligeras, estables y autorizadas que recuperen la información completa.

### Patrón de elección por coste total
- **Primera elección:** reutilización de resultados/sesiones autorizadas, exportaciones oficiales, feeds y API documentadas.
- **Segunda:** HTTP directo permitido a HTML/JSON/XML, con consultas incrementales, caché y paginación controlada.
- **Tercera:** inspección puntual de DOM/JavaScript/tráfico mediante herramientas de diagnóstico, sin transformar una API interna no documentada en contrato.
- **Cuarta:** navegador o WebView automatizado cuando la interacción o el JavaScript sean imprescindibles; mantener contexto y evitar reiniciar cada consulta.
- **Quinta:** agentes visuales, servicios especializados o plataformas remotas solo si la alternativa más ligera no basta, con consumo y autorización verificados.

### Criterios verificables de finalización
No aceptar «se abre la página», «el botón es visible», «HTTP 200» o «workflow verde» como prueba del objetivo final. Confirmar registros esperados, integridad, cobertura real, tratamiento de adjuntos, resultados de las acciones y trazabilidad de errores. Distinguir evidencia comprobada de conjetura. Documentar mecanismo, coste por consulta, número de iteraciones, límites, fallos conocidos y forma de recuperación.

### Transferencia de aprendizaje
Tras resolver cualquier sitio: convertir las observaciones en reglas neutrales, registrar antipatrón → causa → diagnóstico mínimo → corrección → prueba → coste; guardar los detalles específicos en documentación del proyecto, no en esta skill. Se conserva el antecedente que motivó esta política (una pasarela educativa basada en WebView, con navegación de sesión, diferencias móvil/escritorio, fallos de formatos y exceso de iteraciones remotas), **sin imponer su arquitectura a portales distintos**.

## Construcción de conectores reutilizables
Definir contrato de entrada/salida, esquema de campos, procedencia/fecha, errores tipificados, reintentos, checkpoints e idempotencia. Aislar adaptadores por portal y compartir transporte HTTP, validación, normalización y observabilidad. Incluir tests con fixtures sin secretos, ejemplos sintéticos, condiciones de suspensión y alternativa manual autorizada.
La operación diaria debe poder ejecutarse con recursos gratuitos cuando sea viable y sin depender del servicio usado para investigar el portal.

## Evidencias y criterio de verificación
Para cada sitio registrar: fuente | URL | mecanismo | autenticación | paginación/cobertura | campos | consumo por ejecución | herramientas evaluadas | restricciones | prueba y fecha | confianza | próximo paso.
Estados obligatorios: HIPÓTESIS, DOCUMENTADO, PROBADO LOCALMENTE, VALIDADO EN ORIGEN, VALIDADO EXTREMO A EXTREMO, BLOQUEADO. No declarar cobertura total si las páginas o respuestas no se comprobaron exhaustivamente.

## Ejemplos y lecciones
- **Buscar-Curro:** evaluar extracción HTTP y paginación con pruebas controladas antes de probar navegador o Firecrawl; para Eurofirms/Randstad y portales con paginación desconocida conservar expresamente el nivel de cobertura demostrado. Comparar Firecrawl como herramienta *candidata*, nunca asumir acceso, gratuidad ni capacidad de API interna.
- **Aplicaciones con autenticación federada:** distinguir sesión, interfaz responsiva y extracción de contenido; reutilizar contexto autorizado y evitar pruebas remotas repetitivas.
- **Subastas:** favorecer datos públicos oficiales estructurados y trazabilidad de anuncios/documentos frente a navegación intensiva.

## Aprendizaje y distribución
Al resolver un problema, registrar estrategia validada y métricas, añadir un caso reproducible genérico y extraer patrones a la skill; evitar guardar detalles operativos sensibles del sitio o credenciales. Mantener este repositorio como fuente canónica. Después de cambios, validar, versionar y publicar en el mismo plugin privado y marketplace de Codex cuando existan herramientas/permisos, sin confundir commit con despliegue.
