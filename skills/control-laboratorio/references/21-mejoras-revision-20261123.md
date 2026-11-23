# Segunda auditoría y mejoras implantables · 23/11/2026

## Prioridades verificadas
1. Operaciones `unknown` del Supervisor: no repetir la jornada. `supervisor_revision.py` revisa justificantes con el algoritmo de fecha/SHA/propiedad de `supervision_diaria.inspect` y solo cambia a `applied` si la prueba es válida; sin archivo histórico se mantienen `unknown`. No hay reconciliación `not_applied` automática.
2. La memoria ya tenía checkpoints, pero los `next_action` anteriores seguían apareciendo vigentes. `knowledge_status.py` añade **estado explícito** (`open|blocked|resolved|superseded`) con evidencia posterior del mismo proyecto; `superseded` exige un `next_action` posterior y los antiguos sin revisar no se presumen vigentes, idempotencia y trazabilidad. El esquema se añade a la SQLite privada solo al registrar una transición autorizada. `pending` lee bases antiguas sin mutar esquema.
3. `vinculos_contexto.py` permite ámbito por alias confirmado. El índice local `vinculos.py` mantiene asociaciones de **rutas** con expedientes y jamás copia los contenidos. La evidencia `GeckoDriver` + ámbito `BrowserLearn` se evalúa contra alias, no contra título literal; si no hay alias confirmado, no se amplía la búsqueda.
4. Banco evaluativo positivo/negativo con `eval_cases.jsonl` y `eval_skill_routing.py`. Debe alimentarse con observaciones **reales y verificables** de nuevos chats; `not_evaluated` por defecto, sin tratar tests del router documental como decisiones del modelo.
5. `mcp_sesion_diagnostico.py` separa estado systemd, contadores acotados de errores del journal y error observado en el cliente. El diagnóstico no cierra sesiones, reinicia servicios, ni deduce la causa exacta sin traza.
6. Versiones de manifiestos sincronizadas; test dinámico en vez de anclado a 0.4.56; documentación de `codex plugin add` para marketplace local.
7. `ensayo_restauracion.py` verifica recuperación **aislada** de SQLite con `integrity_check`. No certifica VM. Restaurar una VM real en otro anfitrión exige acceso al host, destino aislado, espacio y parada/reversión controlada; nunca sobreescribir el equipo operativo.

## Seguridad y observabilidad
- Las credenciales, informes escolares, cookies, logs detallados y rutas de archivos privados no se empaquetan ni se suben a GitHub.
- Conservar alteraciones del proyecto TPM2 pendientes; no tocar BrowserLearn con cambios de trabajo existentes.
- El estado de tareas antiguas no se reescribe. Marcar "resuelto" requiere un `verified_result` probado de fecha/revisión posterior; mantener trazabilidad del hito.
- La entrega del plugin requiere commit canónico, empaquetado desde SHA exacto, preflight, actualización con `release_id` esperado y postflight byte a byte. Sesiones ChatGPT abiertas pueden conservar caché.


## Despliegue local reversible
`skills/bibliotecario-memoria/tools/deploy_local_bibliotecario.py` compara módulos, rechaza versiones desconocidas y por defecto solo ejecuta `--dry-run`; `--apply` requiere autorización para el lote, crea backup privado y no reinicia servicios. La base de datos original se respalda con la API SQLite `backup()` y `quick_check` antes de cualquier migración aditiva. Para rollback, restaurar solo archivos modificados desde ese backup y restaurar una SQLite a partir de una copia aislada validada, nunca mientras otros servicios escriban.

Las asociaciones `vinculos.py` se realizan por prefijo de proyecto confirmado y guardan únicamente rutas, no los contenidos. Su configuración concreta pertenece al Bibliotecario privado y no se publica. La tabla `work_aliases` almacena alias por expediente; consultas no pueden inferir alias no confirmados.


## Cierre posterior de operaciones y niveles de evidencia
failed_effects_unknown: se sabe por systemd que el proceso devolvió error, pero se ignora si la automatización alcanzó efectos parciales. Es distinto de unknown (sin cierre) y not_applied (ausencia de efectos demostrada). La huella SHA queda en proof_sha para trazabilidad; no significa SHA de éxito. No reutilizar esa huella para pasar inspect.
eval_skill_routing.py distingue user_report de trazas, comprueba la versión y la independencia de las conversaciones. Sin acceso a nuevas conversaciones, el resultado es parcial/no evaluado, nunca L4 aprobado.
