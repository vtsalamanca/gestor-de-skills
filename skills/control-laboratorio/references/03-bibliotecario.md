# Bibliotecario, contexto y continuidad entre conversaciones

## Reanudación correcta
1. Buscar por **título real** del trabajo (por ejemplo «Acceso web y llavero seguro del laboratorio Debian», «Buscar-Curro — rediseño», «Homologación MCP Debian» o «Gestor de Skills»); no tomar una coincidencia incidental como expediente correcto.
2. Obtener breve/revisión más reciente, decisiones, restricciones, pasos verificados y próximos pendientes. Seguir el enlace o ruta al documento operativo para contrastar si aún existe y si se modificó.
3. Confrontar fecha y postcondición: «se creó», «se instaló», «se probó sintéticamente», «se verificó acceso privado», «se ejecutó sin presencia» y «se entregó informe» son evidencias distintas.
4. Continuar a partir de esa evidencia y evitar repetir autenticaciones, pruebas o descargas ya acreditadas. Solicitar intervención solo ante un requisito material real.

## Interfaz local existente
La interfaz JSON del Bibliotecario se encuentra en $HOME/bibliotecario-piloto/interfaz_chat.py. Su esquema actual conocido admite action=find con title, action=brief con work, action=resume y action=record_and_brief con work, operation_id, label y entries. No suponer que una función de MCP llamada «bibliotecario» está disponible en todos los chats.

Ejemplo conceptual, nunca con IDs inventados:
- Buscar expediente y confirmar título.
- Leer brief y revisión N.
- Registrar operation_id estable, solo si procede: entries tipo verified_result, decision, constraint, next_action o note, con descripción no sensible, fechas, comandos relevantes, hashes y rutas de documentos.
- Confirmar write.status saved/duplicate y revisión; releer brief; comprobar que el hito aparece en N+1, no declarar guardado por el mero envío.

No copiar código OTP, cookies, contraseñas, mensajes de menores, NIF, currículum ni claves en texto de los hitos. Los resúmenes son índices semánticos, no volcados de sesiones.

## El Observador no es memoria automática universal
Observador de proyectos y observador de resguardos son servicios específicos. Su estado activo **no demuestra** que hayan registrado todos los mensajes de chat, que cada modificación de archivo se haya convertido en checkpoint o que se haya propagado a otro chat. Validar persistencia mediante lectura de la revisión.

## Hitos y permisos
Registrar tras cada fase material, publicación, cambio de fuente o incidente que deban recuperarse. Para cambios de habilidades/herramientas, respetar la autorización previa de catalogación/resguardo declarada en inventariar-skills. Un lote explícitamente aprobado autoriza sus pasos concretos sin solicitar otra vez permiso por cada fase. No crear expedientes duplicados ni insertar notas en una historia o expediente ajeno.

## Salida de continuidad
Documento canónico modificado o localizado, expediente y revisión real, resultado verificable, riesgo/limitación, rollback y siguiente acción. Si falla escritura o lectura: REGISTRO_PENDIENTE o REGISTRO_NO_VERIFICADO, con la causa; no inventar éxito.
