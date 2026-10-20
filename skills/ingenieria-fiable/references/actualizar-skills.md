# Actualización de habilidades mediante MCP (bajo demanda)

Disparador: solo cuando se modifique una skill, no en cada conversación.

1. Confirmar repositorio canónico, permisos, versiones y release ID. Detenerse ante divergencias.
2. Editar skill y referencias, actualizar versiones del paquete, manifiestos y pruebas.
3. Utilizar MCP local autorizado para pruebas, empaquetado y verificación de integridad.
4. Sincronizar GitHub solo tras pruebas y verificación de rama, sin forzar el push.
5. Generar ZIP desde un commit exacto y validar contenido y hashes.
6. Actualizar el mismo complemento privado mediante Plugin Creator cuando sea posible transferir el paquete, utilizando el release ID vigente; no crear otro.
7. La ruta Windows de Desktop Commander no es directamente un archivo adjunto a ChatGPT. Cuando no exista transferencia admitida, solicitar únicamente el ZIP.
8. Leer archivos de la release publicada y verificar versión, skills y contenido; no confundir publicación con carga en sesiones antiguas.
9. Detenerse ante costes, permisos o riesgos no autorizados. No crear tareas recurrentes ni comprobar actualizaciones en cada conversación.

Lección observada: Gestor de Skills 0.4.11 se actualizó en el mismo complemento privado con un ZIP adjunto y se verificó leyendo archivos de su release.
