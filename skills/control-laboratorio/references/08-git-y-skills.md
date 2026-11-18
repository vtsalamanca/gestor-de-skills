# Git, GitHub, distribución de skills y coherencia entre copias

## Jerarquía de sistemas
- **GitHub** conserva el código y su historial; no contiene todo Debian ni credenciales, datos privados, SQLite, perfiles de Firefox o configuración de sistema.
- **Debian** ejecuta y modifica el software; su copia puede tener cambios no versionados y ramas divergentes. No declarar sincronización sin comparar SHA, árbol Git y archivos sin seguimiento.
- **Complemento privado ChatGPT** es una release distribuida aparte; actualizar GitHub no actualiza la release instalada automáticamente.
- **Bibliotecario** registra razón de cambios, pruebas y pendientes, pero no reemplaza Git ni realiza backup integral.

## Repositorios y alcance
El repo oficial de las skills es vtsalamanca/gestor-de-skills. Buscar-Curro, Educamos, Subastas-Toledo y el puente privado prueba-work-puente-local son proyectos diferentes. La carpeta de Debian $HOME/proyectos/gestor-de-skills/ es el checkout de trabajo de skills. El catálogo de repositorios y su estado debe consultarse de nuevo en la conexión GitHub y en Debian. El puente privado puede contar con una instantánea verificada de archivos sin historial remoto completo: no llamar «clon íntegro» a esa condición.

## Actualizar código sin perder trabajo
1. Comprobar repositorio, branch, HEAD, origin/main, estado de index/worktree, archivos no rastreados, submódulos y tamaño; usar GitHub y Git local para comparar.
2. Si existe divergencia, estudiar ambos cambios. Conservar un punto de recuperación antes de rebases/merges; no efectuar reset --hard ni force push.
3. Desarrollar en rama o worktree de prueba, ejecutar pruebas conocidas sin red, revisar diff --check y privacidad. No sobreescribir código local operativo antes de pasar pruebas.
4. Publicar por el conector GitHub autenticado en el chat cuando Debian carezca de credenciales HTTPS; crear rama, commit/PR, verificar SHA y fusionar solo tras validación. No introducir un token GitHub en un script o en el chat.
5. Sincronizar Debian mediante fetch y avance directo/reconciliación protegida; comprobar HEAD local = remoto y que la funcionalidad y los datos privados locales permanecen.
6. Registrar cambios materiales con revisión del Bibliotecario y rollback. No confundir «código alineado» con funcionamiento desatendido o entrega por el programador.

## Ciclo de vida de skills (usar las diez habilidades, no reinventarlas)
- **descubrir-skills:** consultar capacidades existentes y alternativas antes de programar.
- **auditar-skills:** revisión estática de origen, scripts, dependencias, privilegios, secretos, inyección, coste y licencia.
- **crear-skills:** estructura Agent Skills (frontmatter, SKILL.md corto, referencias y tests).
- **inventariar-skills:** conteo, versiones, duplicados, catálogos y autorización para respaldar.
- **integrar-skills:** compatibilidad por plataforma y publicación del plugin; no asumir que un repositorio se auto-instala.
- **ingenieria-fiable:** plan, regresión, pruebas estáticas/sintéticas, postcondiciones y rollback.
- **organizaciondeltrabajo:** continuidad y cierre con presupuesto marginal cero.
- **bibliotecario-memoria:** revisión idempotente y readback.
- **acceso_webs:** método para navegar cuando una skill exige consultar páginas, llavero y OAuth.
- **buscar-comparar-productos:** compras con precios reales, envíos y rebajas contrastadas desde fuentes públicas, sin histórico propio.

## Actualización segura del complemento privado
Leer el procedimiento CANÓNICO skills/ingenieria-fiable/references/actualizar-skills.md y sus referencias postpublicacion-plugin.md y publicacion-sin-credenciales.md desde el commit realmente vigente. En particular:
- Misma identidad de plugin privado, usuario y release actual; **no crear uno nuevo**.
- Añadir la nueva skill al conjunto de empaquetado y a versiones de manifiesto de Codex/marketplace; aumentar versión semántica y actualizar README.
- Pruebas del repo y paquete determinista hecho desde SHA exacto; sin archivos privados ni marketplace dentro del ZIP del publicador.
- Preferir GitHub Actions en runner público estándar, solo bajo condiciones de cuota ya verificadas; obtener artefacto por conector y comparar hashes. Ninguna publicación automática sin aprobación.
- Actualizar plugin existente con expected_release_id y archivo host-uploaded verificable; el ZIP en Debian no equivale a archivo accesible al publicador.
- Releer lista y contenido de archivos publicados, comprobar la nueva habilidad y referencias, privacidad y release. La recarga en chat nuevo y la disponibilidad de Codex se comprueban aparte.

## No publicar
Perfiles de Firefox/Thunderbird, estados e informes privados, CV, tokens, .env, variables secretas, endpoints con firmas, credenciales, logs escolares, cookies, documentos de menores, base SQLite. Documentos públicos deben usar ejemplos sintéticos y rutas de usuario genéricas ($HOME). El público no necesita saber claves, hostnames privados, ID reales de tareas ni direcciones de red.
