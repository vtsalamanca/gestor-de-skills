# Git y publicación del Gestor de Skills: recuperación sin credenciales locales

Este procedimiento complementa el protocolo canónico `skills/ingenieria-fiable/references/actualizar-skills.md`.

1. En Debian, `git config --local user.name 'vtsalamanca'` y `git config --local user.email 'vtsalamanca@users.noreply.github.com'` configuran **solo** la identidad de commit. No otorgan autenticación.
2. Si `git push` por HTTPS falla por credenciales ausentes, **no repetir ni solicitar tokens**: publicar con el conector oficial de GitHub (rama, actualizaciones, PR y merge). No modificar configuración global de Git.
3. Tras el merge, `git fetch origin main`, revisar `git status --short`, conservar copias o rama de respaldo de cambios locales y solo entonces `git merge --ff-only origin/main`. Si hay divergencia, reconciliar sin sobrescribir otros cambios.
4. Ejecutar `python3 -m unittest discover -s tests -p test_package_plugin.py` y empaquetar desde el SHA confirmado con `scripts/package_plugin.py`. Usar inventario dinámico: nueve habilidades a 24-10-2026.
5. Publicar en el plugin privado existente mediante Plugin Creator, con `expected_release_id` leído inmediatamente antes. Comprobar después versión, contenido, nueve skills, privacidad y nuevo release ID. Sin postlectura, **no declarar publicación terminada**.
6. La aparición de instrucciones en un chat nuevo es una prueba distinta: consignar `CARGA_NO_PROBADA` hasta comprobarla.

Nunca almacenar credenciales en los documentos, ni confundir el repositorio GitHub con la base SQLite de memoria de los proyectos.
