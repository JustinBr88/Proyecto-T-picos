# AI Development Log

Registro del uso de IA en el proyecto. Se completa **durante** el desarrollo, no al final. No hace falta anotar cada prompt: sólo los que afectaron significativamente al desarrollo.

**Herramientas usadas**

| Herramienta | Modelo | Quién la usa |
|---|---|---|
| Claude Code (app de escritorio) | Claude Opus 5.5 | Justin |

> Al sumar una herramienta, agregala a esta tabla.

---

## Registro

| # | Fecha | Caso | Quién | Actividad | Herramienta | Qué se solicitó | Resultado | Decisión humana | Evidencia |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-27 | — | Justin | Análisis | Claude Code | Verificar el enunciado contra el repo del equipo | Detectó que el repo estaba vacío y armó el checklist de las 10 restricciones | Aceptado | — |
| 2 | 2026-10-27 | — | Justin | Análisis | Claude Code | Analizar la app base elegida (opción 3) | Detectó que es Python 2 + AngularJS (no "Python 3 / JS sin framework" como dice la tabla del enunciado), que no tiene datos ni tests, y el bug de solapamiento de fechas (BUG-1) | Aceptado. El equipo mantiene la opción 3 | `docs/SPEC.md` §1 |
| 3 | 2026-10-27 | 4, 5 | Justin | Requisitos | Claude Code | Proponer las 2 historias de usuario adicionales | Propuso "Seguridad de credenciales" y "Gestión de habitaciones" | Aceptadas por Justin; pendiente validar con el equipo | `docs/SPEC.md` §3 |
| 4 | 2026-10-27 | — | Justin | Planificación | Claude Code | Redactar la especificación y el plan de fases | SPEC con criterios de aceptación y plan de 6 fases | Pendiente de revisión del equipo | `126eb6c` |
| 5 | 2026-10-27 | 0 | Justin | Código | Claude Code | Migrar a Python 3 y reorganizar las carpetas | Migración en commits separados: sintaxis, reorganización por capas, seed, Docker y tests | Pendiente de revisión (PR del Caso 0) | rama `feature/caso-0-migracion` |
| 6 | 2026-10-27 | 0 | Justin | Debug | Claude Code | Comprobar flask-restful con Flask 3 antes de seguir | Prueba aislada: los GET con `reqparse` devuelven 415 y `type=list` corrompe la lista de habitaciones. Se corrigió declarando la `location` de cada argumento | Aceptado | `54d23b4`, `tests/integration/test_smoke.py` |
| 7 | 2026-10-27 | 0 | Justin | Infraestructura | Claude Code | Preparar MySQL para desarrollo | Como la PC no tenía MySQL instalado, propuso Docker Compose con valores por defecto que coinciden con `config.py` | Pendiente de confirmar con el equipo (decisión abierta de la Fase 0) | `ced47b8` |
| 8 | 2026-10-27 | 0 | Justin | Testing | Claude Code | Correr los tests de integración con Docker | Detectó que la carpeta montada en el contenedor llegaba vacía (Docker Desktop no compartía el disco D), que los tests ocultaban ese error como *skipped* y que los comandos CLI fallaban desde los tests. Corrigió los tres: 34/34 en verde | Aceptado | `7255a33` |
| 9 | 2026-10-27 | 0 | Justin | QA | Claude Code | Probar en el navegador login, búsqueda, reserva, actualización y cancelación | Los cinco flujos funcionan. Encontró BUG-6 (error del frontend original en "Actualizar reserva") y que su propia afirmación sobre BUG-2 era falsa (respuesta incorrecta #4) | BUG-6 queda pendiente para el equipo | `docs/SPEC.md` §1 |
| 10 | 2026-10-27 | — | Justin | Gestión | Claude Code | Crear issues, etiquetas y ramas en GitHub y proteger `main` | Issues #2–#7 generados desde el SPEC, etiquetas `caso-N`, `ia-incorrecta` y `ia-rechazado`, rama `develop` y ramas de cada caso. Asignó por error todos los issues a Justin; lo corrigió dejando sólo los suyos | Aceptado | Issues #2–#7 |
| 15 | 2026-10-27 | 2 | Justin | Análisis | Claude Code | Analizar el código del Caso 2 antes de modificarlo | Verificó en el código de la librería (v4.15.35) que `disabledDates()` existe, que `dp.update` se dispara **después** de redibujar y que `disabledDates()` redibuja (borra las marcas): por eso se repinta tras cada llamada. Detectó que **crear** una reserva no validaba disponibilidad | Aceptado: se agregó la validación en la creación | `30a12c9` |
| 16 | 2026-10-27 | 2 | Justin | Testing | Claude Code | Tests primero para el solapamiento y el endpoint | 20 tests unitarios y 15 de integración escritos antes del código. Al correrlos contra el código original confirmaron BUG-1: de 4 formas de solapamiento sólo detectaba una | Aceptado | `6326cd0`, `30a12c9` |
| 17 | 2026-10-27 | 2 | Justin | Código | Claude Code | Endpoint `/api/availability` y calendario con días llenos y parciales | Backend y frontend del Caso 2; 70 tests en verde | Aceptado | `fe999cc` |
| 18 | 2026-10-27 | 2 | Justin | QA | Claude Code | Probar el calendario en el navegador | Funciona: el 18/12 en Miami (lleno) no se puede elegir, el cambio de mes y de locación recargan sin refrescar. Encontró 3 problemas: los días pasados se pintaban y parecían elegibles (corregido), casi todos los días salen "parcial" con los datos de prueba, y el check-out salta al mismo día del check-in (código original) | Primero corregido; los otros dos, pendientes de decisión | PR del Caso 2 |

---

## Respuestas incorrectas de la IA

| # | Fecha | Qué propuso la IA | Por qué estaba mal | Cómo se detectó | Corrección |
|---|---|---|---|---|---|
| 1 | 2026-10-27 | En el SPEC (CA2.5), usar la opción `beforeShowDay` de *bootstrap-datepicker* para pintar los días ocupados del calendario | El archivo `static/libs/bootstrap-datepicker.js` en realidad es **Eonasdan bootstrap-datetimepicker** (otra librería, con el nombre de archivo engañoso), que no tiene `beforeShowDay`. La IA asumió la librería por el nombre del archivo sin abrirlo | Al leer la cabecera de la librería durante la migración (la propia IA, antes de escribir código del Caso 2) | CA2.5 reescrito con las opciones reales (`disabledDates`, `minDate`) |
| 2 | 2026-10-27 | En el SPEC (BUG-2), "evaluar si el endpoint se usa; si no, eliminarlo", sin haberlo verificado | La IA no había comprobado quién usa el endpoint. **Ver #4**: su "corrección" posterior también estaba mal | — | Ver #4 |
| 3 | 2026-10-27 | Plantear la migración a Python 3 como un cambio de sintaxis (`print`) | Faltaban incompatibilidades reales: un `TabError` por mezcla de tabs y espacios, y flask-restful roto con Flask 3 (punto 6 del registro) | Compilando el código con Python 3.12 y con una prueba aislada de flask-restful | Corregido en `7f4bfc2` y `54d23b4` |
| 4 | 2026-10-27 | Afirmar que `PUT /api/reservation/<id>` (BUG-2) era el endpoint que usa el frontend y que el flujo "Actualizar reserva" estaba roto | La IA leyó `url: '/api/reservation/:reservation_id'` en la factory y supuso que el id iba en la URL. AngularJS `$resource` no pone en la URL los parámetros del cuerpo de un PUT: el frontend llama a `PUT /api/reservation`, que funcionaba bien | Al probar el flujo en el navegador y mirar las peticiones de red | SPEC y docstrings corregidos; se agregó un test para el endpoint que el frontend usa de verdad. **Lección: verificar con una prueba real, no sólo leyendo el código** |
| 7 | 2026-10-27 | En la skill `fancyhotel-testing`, ejemplo con `from fancyhotel.db.rooms import overlaps` (lógica pura dentro de `db/`) | Contradice la regla de capas de la propia skill backend: `db/` sólo habla con MySQL. La IA escribió el ejemplo sin contrastarlo con sus propias reglas | Al diseñar el Caso 2 | Lógica pura en `fancyhotel/availability.py`; ejemplos de las skills corregidos |

---

## Cambios de la IA rechazados

| # | Fecha | Caso | Qué propuso la IA | Por qué se rechazó |
|---|---|---|---|---|
| — | | | | |

> Si rechazás algo en una revisión de PR, anotalo aquí y enlazá el comentario del PR.

---

## Decisiones humanas

| # | Fecha | Decisión | Quién | Justificación |
|---|---|---|---|---|
| 1 | 2026-10-27 | Usar la app base de la opción 3 (thegrucoder/Hotel-Reservation-System) | Equipo | Pareció la más sencilla y rápida de las cuatro |
| 2 | 2026-10-27 | Reparto de roles por caso (Dev / Reviewer / QA rotando) | Equipo | Lo pide el enunciado; cada integrante pasa por los tres roles |
| 3 | 2026-10-27 | Aceptar las historias propuestas para los Casos 4 y 5 | Justin | Se integran con los Casos 1 y 3; pendiente de confirmar con Ana y Bethel |
| 4 | 2026-10-27 | Aprovechar la migración para reorganizar las carpetas y que el proyecto sea fácil de entender | Justin | Facilita el trabajo en paralelo de la Fase 2 (menos conflictos en un archivo único) |
| 5 | 2026-10-27 | Agregar la rama `develop` para integración y dejar `main` sólo para versiones estables; crear de antemano las ramas de cada caso | Justin | Que `main` quede limpio y siempre entregable |
| 6 | 2026-10-27 | Agregar skills de proyecto (backend, frontend, testing, docs, git) versionadas en el repo | Justin | Que Ana y Bethel trabajen con las mismas convenciones al clonar |
