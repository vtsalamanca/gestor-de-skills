# Controles de permisos y gasto para Codex, Goose y MCP

`tools/preflight_agentes.py` analiza sin red campos conocidos de configuración de Codex y Goose. No lee ni muestra credenciales. Distingue `unspecified` de falta de seguridad; detecta explícitamente sandbox peligroso, aprobaciones desactivadas, red habilitada, modo Goose autónomo y proveedor externo. **No mide gasto real ni el estado efectivo de permisos MCP**.

    python3 skills/control-laboratorio/tools/preflight_agentes.py

`tools/arranque_seguro_agentes.py` proporciona un arranque **opcional**, sin sustituir los comandos anteriores ni lanzar nada sin `--execute` desde terminal interactiva:

    python3 skills/control-laboratorio/tools/arranque_seguro_agentes.py codex
    python3 skills/control-laboratorio/tools/arranque_seguro_agentes.py goose --model modelo_local_instalado

Codex: requiere auth `chatgpt`, elimina variables de claves API habituales, exige `workspace-write`, aprobación `on-request` y red del sandbox deshabilitada. Goose: fuerza proveedor Ollama local, `GOOSE_MODE=approve`, host loopback y límites de turnos; **bloquea** si falta Ollama local. Un perfil seguro solo protege los arranques que pasan por él; ejecutar `codex` o `goose` directamente lo elude. No modificar ajustes globales ni autorizar servicios de pago por uso. La cuenta ChatGPT podría consumir cuotas del plan al consultar modelos, que no son una autorización para facturación API.

MCP: comprobar herramientas reales, permisos de lectura/escritura, autorizaciones, idempotencia y postcondiciones. No desactivar límites de Control Debian ni exponer secretos. No inferir coste real a partir del texto de un manifiesto. Usar estas comprobaciones como preflight, no como certificación absoluta.

Fuentes: documentación oficial de configuración de Codex y Goose (modo `approve`, permisos y proveedores). Auditoría local con fixtures y sin modelos externos. Presupuesto adicional 0 €.
