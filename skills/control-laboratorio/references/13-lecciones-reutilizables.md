# Lecciones concretas del laboratorio para no repetir errores

Estas lecciones son **patrones**, no hechos vigentes para siempre. Antes de aplicarlas recuperar el último expediente y estado de código/servicio.

## Acceso remoto y permisos
1. Un MCP puede anunciar 76/82 herramientas localmente mientras ChatGPT ve otro catálogo. Descubrir la sesión real; no instalar versiones paralelas por una discrepancia de inventario.
2. Control Debian no es Desktop Commander. Si la operación tipada existe, emplearla. Desktop Commander queda como excepción realmente justificada, no vía principal.
3. Una autorización local persistente de comandos no elimina las comprobaciones por operación ni convierte un sandbox limitado en shell root. Diferenciar política de plataforma y controles locales con diagnóstico causal.
4. Una operación de ticket sin resultado no se ha completado. Recoger ticket, esperar respuesta autorizada y comprobar postcondición.

## Autenticación y navegación
5. El llavero LAB-AUTH tiene metadatos separados del secreto; que una colección esté abierta no demuestra que la credencial buscada esté allí. No pedir contraseñas a ChatGPT.
6. Thunderbird puede estar instalado en un directorio privado sin estar en PATH. Comprobar el proceso y perfil existentes antes de reinstalar o pedir otro OAuth; un segundo factor Gmail no prueba inicio de sesión en InfoJobs.
7. El lector de InfoJobs debe reconocer la ruta real de candidaturas y el Firefox dedicado; un diagnóstico de login falso puede ser un problema de clasificación de URL, no contraseña.
8. El estado private_read_verified se aplica a una lectura privada concreta con marca temporal; no garantiza que el próximo arranque desatendido se autentique.
9. Webs con 403, CAPTCHA, robots o DOM dinámico requieren la modalidad de acceso permitida; no invertir horas en un bypass ni afirmar que un producto/oferta no existe por bloqueo de consulta.

## Programación y resultados
10. Los temporizadores Debian pueden completar la recolección y ChatGPT seguir sin recibir notificación. Revisar cada eslabón, especialmente autorización de lectura no interactiva y entrega.
11. Educamos distingue detectar adjunto, descargarlo, poder identificarlo y cambiar leído/no leído. Contadores y flags de verificación generales no bastan para afirmar extracción real.
12. Buscar Curro distingue estado de bolsa ATE, provincia, orden y vigencia, y marca las fuentes fallidas como cobertura parcial. No confundir candidaturas con ofertas verificadas.

## Desarrollo y catálogo
13. GitHub guarda código, Debian ejecuta y Bibliotecario explica. Una versión de plugin instalada es un cuarto artefacto distinto; revisar los cuatro antes de cerrar.
14. Un archivo local no rastreado puede contener la mejora más reciente sin estar en GitHub. Fusionar después de pruebas, pero no publicar archivos de credenciales o CV privado.
15. Una copia reconstruida con hashes correctos puede contener todos los ficheros de una revisión y **no** su historial completo; etiquetarla con precisión.
16. La skill nueva no debe copiar el contenido entero de las otras diez: las enlaza y las invoca cuando proceda; los procedimientos largos se conservan en sus ubicaciones canónicas.
17. No dejar 20 ventanas o procesos de pruebas abiertos. Inventario previo y limpieza selectiva posterior; cerrar solo lo propio.
18. Un artefacto ZIP visible en Debian o Windows no es por eso un archivo accesible a Plugin Creator; validar cada frontera y archivo antes de intentar publicar.
19. El respaldo automático u Observador no es registro universal: exigir status saved y revisión releída.
20. «Reiniciar servicio», «reiniciar VM», «recuperar sesión», «funciona la tarea» y «entregó mensaje» son afirmaciones distintas que exigen pruebas distintas.
