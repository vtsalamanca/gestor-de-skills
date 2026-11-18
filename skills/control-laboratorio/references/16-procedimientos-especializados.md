# Procedimientos especializados y recuperación de manuales existentes

La habilidad principal coordina y **localiza** procedimientos, no sustituye todas las aplicaciones con instrucciones genéricas. Las referencias siguientes indican qué buscar antes de volver a programar un adaptador o servicio.

## Control gráfico y edición de documentos
Buscar en Control Debian funciones tipadas de ventana, captura, gesto y fixtures (Mousepad, Writer, Calc). Prueba segura: ventana sintética → acción → inspección de contenido → limpieza del objeto propio. Para tareas de producción usar herramientas específicas de creación/edición de PDF, documentos, hojas o presentaciones; no convertir un documento editable en imagen si se exige estructura. Las pruebas históricas de un gesto no demuestran control universal de todas las ventanas.

## Navegadores y acceso a webs complejas
Consultas públicas: modalidad ligera gratuita (fuente oficial, HTML, JSON, API sin pago); si una web aplica JS, 403 o autenticación, revisar acceso_webs y su catálogo de modalidades. Para portales del usuario usar LAB-AUTH en Debian, no una sesión supuesta de navegador del chat. Pruebas con perfil temporal, sin secretos y sin rebote de URLs inseguras. Solo si la página exige interacción real usar el navegador autorizado existente.

## Educamos y empleo
Los dos proyectos tienen colectores y coordinadores específicos. Recuperar siempre última documentación del proyecto y revisiones del Bibliotecario antes de cambiar selectores, campos, adjuntos, filtros o periodicidad. Distinguir datos personales de estado público. Comparación de resultados por fecha y hash, no por impresión de que «hay más mensajes».

## Impresora, escáner y otros periféricos
Consultar catálogo local de herramientas y proyecto de Control Debian. Separar detección USB/red, cola CUPS, formatos soportados, renderizado y salida física; si falta evidencia física no declarar impresión completada. Evitar permisos genéricos y cambios de firewall. Para nueva impresora, documentar modelo exacto, piezas consumibles y compatibilidad desde fuente actual.

## Tutorial multimedia y audiolibros
El proyecto tiene nombre vigente **Tutorial**; no usar denominaciones históricas como nombre actual sin verificar. Recuperar configuración, catálogo y enlaces locales antes de crear un servidor nuevo. Para acceso móvil, verificar ruta, conectividad local o privada, formato y reproducción real en dispositivo; evitar publicar archivos privados por URLs abiertas. No asumir que un enlace en Debian es accesible en móvil.

## Windows, Debian virtualizado y portátiles
La VM y el host Windows son entornos distintos. Antes de trabajar en el host, verificar conector real y autorización sobre esa máquina; Control Debian no otorga acceso automático a Windows. No cambiar virtualización, SSH, túneles, red, almacenamiento o snapshot sin conocer el camino de recuperación. Usar la configuración real de VirtualBox y su plan de respaldo. Las versiones de Windows y del portátil pueden variar; no fijarlas como condición de la habilidad.

## Recursos, limpieza y backups
Seguir 06-escritorio-y-mantenimiento y 12-recuperacion: inventariar antes de borrar; no acumular copias temporales indefinidas; no borrar una copia única o un perfil autenticado sin verificar respaldo y autorización. Tras pruebas, cerrar ventanas propias, limpiar archivos temporales propios y conservar todo lo que afecte al usuario.

## Investigación y compras
Delegar buscar-comparar-productos; comparar precios reales, disponibilidad, envío, garantía y especificaciones con fuentes verificables. Consultar histórico en terceros cuando aporta valor al Black Friday, sin construir base de datos propia ni hacer un rastreo costoso. La función del laboratorio es ofrecer un método reproducible, no congelar precios.

## Alta de una nueva capacidad
Inventariar lo ya instalado, comprobar si hay skill o herramienta existente, evaluar alternativas y cuota, auditar origen, crear adaptación limitada, probar fixture y caso real autorizado, versionar y registrar. No convertir cada necesidad nueva en un plugin, bot, servicio o túnel permanente.
