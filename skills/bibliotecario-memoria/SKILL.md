---
name: bibliotecario-memoria
description: Guardado y recuperación de hitos en Debian para ChatGPT, compatible con agentes que puedan ejecutar Remote Desktop Commander.
version: 0.3.0
---
# Bibliotecario — protocolo ligero y compatible con Free

**Únicas dependencias en ejecución:** Remote Desktop Commander (si está disponible en la cuenta), Python 3 estándar y SQLite en `debian-laboratorio`. No depende de Codex, Work, GitHub, Plugin Creator ni servicios de pago.

Ruta: `/home/labgestor/bibliotecario-piloto/interfaz_chat.py`. Enviar JSON por entrada estándar mediante una ejecución de Python en Debian.

- Leer estado breve: `{"action":"brief","work":"6011f9967885"}`.
- Recuperar información completa: `{"action":"resume","work":"6011f9967885"}`.
- Guardar de una vez: `{"action":"record_and_brief","work":"6011f9967885","operation_id":"id-unico-y-estable-del-hito","label":"Chat de seguimiento","entries":[{"kind":"decision","text":"Decisión tomada"}]}`.

`record_and_brief` crea sesión y revisión dentro de una transacción, tolera concurrencia y devuelve `write` y `context` actualizado. No hay que obtener ni mantener sesión o revisión para guardar. No reutilizar `operation_id` para otro contenido.

Guardar decisiones, resultados **realmente** verificados, fallos, restricciones y próximos pasos; omitir secretos y transcripciones completas. No alterar otros proyectos, habilitar purgas ni utilizar GitHub como intermediario de memoria.

**Límite:** una habilidad no recibe por sí sola eventos de todos los mensajes ni cierres de ChatGPT. La invocación depende de que el agente aplique estas instrucciones. Una publicación no demuestra carga espontánea en Free o Plus.
