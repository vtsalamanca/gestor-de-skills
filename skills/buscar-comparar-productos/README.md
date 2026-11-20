# Buscar y comparar productos (v0.3.6, Debian)

Habilidad con **ejecutor real**, no solo instrucciones. Incluye `SKILL.md`, `tools/buscar.py` y pruebas `tests/test_buscar.py`.

## Uso

```bash
cd /home/labgestor/proyectos/gestor-de-skills/skills/buscar-comparar-productos
python3 tools/buscar.py --perfil general --producto "despertador digital" --presupuesto 50
python3 tools/buscar.py --perfil portatil-gaming --presupuesto 900 --max-fichas-por-tienda 9
python3 -m unittest discover -s tests -v
```

Resultados en `reports/*.json` y `reports/*.md`.

## Resultado real de desarrollo (17/11/2026)

- Portátiles (primer ensayo a tres tiendas): 74 productos deduplicados en listados, 27 fichas directas verificadas y 5 candidatos pendientes; 0 ofertas calificadas como comprables al no confirmar envío total y garantía.
- Despertadores: 61 candidatos deduplicados, 10 fichas comprobadas, 10 candidatos pendientes de transporte/garantía.
- Tiendas con extracción real: Amazon, El Corte Inglés, MediaMarkt y PcComponentes (esta última mediante recuperación visual X11 `acceso_webs` después del 403; sin extracción automática para Fnac).
- PcComponentes, validación 18/11: 36 ofertas descubiertas en HTML de Firefox, dos fichas verificadas (940,60 € y 999 €), una navegación transitoria no confirmada que funcionó en la repetición aislada.
- Las comprobaciones de navegador gráfico, cesta, código postal y garantía del vendedor quedan fuera; no se afirma cobertura universal.
- Dependencias: Python 3 y paquete `requests` ya instalado. Sin servicios de pago ni consultas a modelos externos. 56 pruebas locales superadas.

Los archivos de reportes son observaciones temporales, **no inventario actualizado permanentemente**. Para un precio vigente, ejecutar de nuevo.

## Recuperación visual de PcComponentes

El comando `buscar-productos` consulta HTTP primero y, al no conseguir contenido utilizable de PcComponentes, utiliza automáticamente `skills/acceso_webs/tools/navegador_visual.py`, que controla Firefox ESR **convencional** de la sesión X11 del usuario, valida URL y propietario, copia HTML renderizado y permite visitar fichas a través del adaptador `pccomponentes_adapter.py`. No elimina el 403 de HTTP ni copia cookies, y no asegura stock/envío/garantía que no hayan sido comprobados. No se crean tareas programadas ni compras.

Validación 18/11/2026: búsqueda RTX 5050, 36 resultados PcComponentes, dos precios confirmados en fichas y un fallo transitorio documentado; búsqueda general «despertador digital», 113 productos totales y precio comprobado en PcComponentes de 12,60 €. 44 pruebas locales.

## Modalidades genéricas de acceso

En cada búsqueda se consulta `acceso_webs/tools/selector_metodos.py`. El transporte HTTP tiene preferencia cuando entrega productos; si resulta insuficiente y hay sesión gráfica autorizada, se elige `M50_NAVEGADOR_VISUAL` sin copiar cookies. Los extractores de cada tienda permanecen en el consumidor. Una página vacía se registra como fallo, no como catálogo agotado.

## Comprobar historicos sin ralentizar la busqueda
Modo normal: enlaces a comparadores, cero consultas extra. Bajo demanda: anadir --consultar-historico-web (hasta dos consultas breves a PCComTracker); para Amazon usar el grafico gratuito de Keepa. No se mantiene base SQLite, precios pasados propios ni un observador programado. Se considera historico no verificado cuando la web no entrega datos comparables.

## Fuentes historicas indirectas
El informe incluye enlaces generados a Google con before: y a Wayback Machine, ademas de Keepa, PCComTracker e idealo. Cero solicitudes extra para esos enlaces. Los resultados antiguos deben verificarse antes de considerarlos evidencia; las fechas de Google no son capturas. No se incorpora scraping automatico de Google.

## Descuentos comerciales
El informe no considera «Black Friday», «Gran oferta» o un porcentaje tachado prueba de ahorro: exige precio anterior fechado del mismo modelo para acreditar rebaja; sin ello muestra `DESCUENTO_HISTORICO_NO_VERIFICADO`. La comparación de precios actuales permanece independiente y no consulta históricos sin petición explícita.
