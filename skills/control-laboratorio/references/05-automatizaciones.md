# Proyectos operativos y automatizaciones: ejecución y entrega

## Principio: cuatro resultados diferentes
Separar **programación**, **ejecución del colector local**, **lectura privada y tratamiento**, **entrega/notificación al destinatario**. Un systemd timer enabled+active acredita agenda, no informe correcto ni entrega ChatGPT. Una tarea Automations enabled no prueba que haya leído un archivo de Debian sin autorización interactiva. run_now puede ejecutar inline en el chat actual; no acredita una ejecución desatendida futura.

Verificar siempre fecha/zona, próxima ocurrencia, run anterior, exit code, informe protegido, cantidad de registros y estado de entrega; mantener la versión de los hechos observados por encima de los prometidos.

## Buscar Curro
- Directorio de código y pruebas: $HOME/proyectos/Buscar-Curro/ (GitHub versionado, sin CV privado). Coordinador local y estados privados: $HOME/proyectos/_gestion/buscar-curro/.
- Temporizador típico: buscar-curro-laboratorio.timer a las 09:00, sujeto a cambios. Servicio buscar-curro-laboratorio.service con preparador opcional de correo InfoJobs y jornada local. La tarea de ChatGPT lee posteriormente un informe saneado; su hora y contenido deben comprobarse en Automations, no asumirse.
- Fuentes: ATE JCCM consulta privada, convocatorias/documentos públicos, ETTs, fuentes sociales, InfoJobs candidaturas. Separar origen, fecha, provincia, condición de bolsa, estado y número de orden sin inferir datos no presentes.
- No convertir resultados de búsqueda sin comprobar en «oferta nueva verificada». No anunciar «no hay ofertas» si fuentes relevantes tuvieron error o bloqueo; usar cobertura parcial.
- Las consultas privadas (ATE/InfoJobs) solo se consideran verificadas si llegan a los registros correctos en la sesión autenticada. No ejecutar candidaturas ni aceptar llamamientos sin autorización específica.
- Para prueba diaria: comprobar estado de timer, último servicio, logs saneados y cache; no repetir scraping o login solo porque la notificación ha fallado. Mantener límites de red, tiempo y reintentos; no repetir el currículum si no ha cambiado.

## EducamosCLM
- Proyecto: $HOME/proyectos/educamos-puente/. Coordinador: educamos_diario.py; colector de mensajes y adjuntos con adaptadores locales existentes.
- Temporizador local típico: educamos-diario-laboratorio.timer a las 13:45. Tarea de ChatGPT del informe sobre las 14:00, si sigue habilitada. Verificar realidad en systemd y Automations.
- Puntos de prueba: autenticación, mensajes visibles, identidades adecuadas, adjuntos detectados, descarga verificada cuando corresponda, marcas de leído y estado final, privacidad escolar. No confundir «adjuntos verificados como revisados» con «archivos descargados».
- No alterar leídos/no leídos en pruebas salvo una selección autorizada y reversible. Si la sesión falla, registrar el tramo afectado y preservar el estado existente.

## Otros trabajos y flujos
- **CDC / comunicación entre chats:** distinguir repositorio GitHub privado, receptor local de eventos y puente vivo; no suponer que mensajes viajan automáticamente entre chats solo por un README.
- **Tutorial multimedia y audiolibros:** los contenidos, nombres, servicios de acceso remoto y reproducción deben recuperarse en el proyecto específico; respetar actualizaciones de denominación y enlaces verificados. No lanzar servicios adicionales para una comprobación documental.
- **Comparación de compras:** delegar buscar-comparar-productos; stock/precio/garantía reales, histórico público solo cuando aporta valor, sin construir base histórica propia ni costosos rastreos masivos.
- **Impresión/escáner y herramientas:** el catálogo de laboratorio indexa componentes, pero las pruebas físicas requieren evidencia distinta de una orden CUPS/IPP aceptada.
- **Actualizaciones de software:** comprobar dependencias, servicios afectados, coste, rollback, mantenimiento y posible impacto en automatizaciones antes de instalar.

## Diagnóstico de incumplimiento de una tarea
Seguir la cadena: timer/programador → servicio iniciado → precondiciones (llavero, sesión gráfica, perfiles) → consulta de fuente → extracción → almacenamiento privado → resumen saneado → lectura ChatGPT → entrega. Identificar el primer eslabón que falló. Corregir ese eslabón con prueba aislada, sin reiniciar todo el flujo a ciegas. La falta de autorización interactiva en un chat desatendido es problema de arquitectura de entrega, no una prueba de que el colector está roto.

## Criterios de completitud
Informe entregado, fechado, sin secretos, con cobertura, errores y enlaces verificados; el run real tiene estado concluido y evidencia de recepción. El siguiente ciclo programado se conserva sin duplicar tareas ni cambiar horarios injustificadamente.
