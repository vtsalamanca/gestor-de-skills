# Panel de homologación L4

Genera un HTML privado y autónomo con el banco canónico. Abre el archivo en un navegador local. El filtro distingue casos pendientes, pilotos sin traza, observaciones de otra versión y casos verificados.

```sh
python3 scripts/panel_l4.py --version 0.4.59 \
  --attempts /ruta/privada/pilotos-debian.jsonl \
  --output /ruta/privada/panel-l4.html
```

Los pilotos admiten las claves `caso` y `ref` (URL autenticada `https://chatgpt.com/c/…`). El panel conserva el enlace privado y omite el texto de las respuestas y las trazas.

Cuando exista una fuente autorizada, cotejar conversación nueva, turno, versión, lecturas y cobertura completa en el registro original. Normalizar los datos al formato de `eval_skill_routing.py` y añadir `--reviewed-observations /ruta/privada/observaciones.jsonl --trace-root /ruta/privada/trazas`. Un archivo íntegro acredita lo que contiene. La cobertura del turno, incluida la ausencia de lecturas en los negativos, debe estar acreditada en la fuente original. Conservar las trazas fuera del repositorio.

El panel mide solo lecturas revisadas de la versión objetivo. Un piloto o el registro de una versión diferente aumenta el número de ejecuciones, pero no cambia precisión ni recuperación. El generador funciona fuera del complemento; usarlo no modifica las habilidades ni requiere publicar una nueva versión.
