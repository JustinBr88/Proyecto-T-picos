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
| 11 | 2026-10-27 | — | Justin | Seguridad | Claude Code | Activar los controles de seguridad de GitHub | Alertas de Dependabot, escaneo de secretos con bloqueo de push y CodeQL (configuración por defecto). No activó los PR automáticos de Dependabot porque se abren contra `main` y se saltearían `develop` | Aceptado | Pestaña *Security* del repo |
| 12 | 2026-10-27 | 0 | Justin | Infraestructura | Claude Code | Dockerizar la app para levantar todo con `docker compose up` | `Dockerfile` (usuario sin root), app en `compose.yaml` con puertos sólo en localhost, `seed-db --if-empty` con test primero, y `docker compose watch` en vez de bind mounts (el disco D no se comparte). Detectó y corrigió un problema de permisos de `/app` al correr pytest en el contenedor | Aceptado | PR #1 |
| 13 | 2026-10-27 | — | Justin | Documentación | Claude Code | Versionar el grafo de graphify para que todo el equipo lo actualice | Versiona `graphify-out/` salvo los archivos locales, registra el *merge driver* de graphify en `.gitattributes`, excluye `static/libs/` con `.graphifyignore` y documenta cómo actualizarlo | Aceptado. Lo pidió Justin: la IA lo había excluido del repo | PR #1 |
| 14 | 2026-10-27 | 0 | Justin | Revisión | Claude Code | Verificar si el Caso 0 estaba completo antes de arrancar el Caso 2 | Encontró: PR #1 y PR #8 mergeados sin revisión, 6 commits fuera de `develop`, issue #2 abierto sin criterios marcados, CA0.1 (clon limpio) sin probar y la rama del Caso 2 todavía con el código original | Se abre un PR nuevo con los commits faltantes y revisión de Ana y Beth | Este PR |

---

## Respuestas incorrectas de la IA

| # | Fecha | Qué propuso la IA | Por qué estaba mal | Cómo se detectó | Corrección |
|---|---|---|---|---|---|
| 1 | 2026-10-27 | En el SPEC (CA2.5), usar la opción `beforeShowDay` de *bootstrap-datepicker* para pintar los días ocupados del calendario | El archivo `static/libs/bootstrap-datepicker.js` en realidad es **Eonasdan bootstrap-datetimepicker** (otra librería, con el nombre de archivo engañoso), que no tiene `beforeShowDay`. La IA asumió la librería por el nombre del archivo sin abrirlo | Al leer la cabecera de la librería durante la migración (la propia IA, antes de escribir código del Caso 2) | CA2.5 reescrito con las opciones reales (`disabledDates`, `minDate`) |
| 2 | 2026-10-27 | En el SPEC (BUG-2), "evaluar si el endpoint se usa; si no, eliminarlo", sin haberlo verificado | La IA no había comprobado quién usa el endpoint. **Ver #4**: su "corrección" posterior también estaba mal | — | Ver #4 |
| 3 | 2026-10-27 | Plantear la migración a Python 3 como un cambio de sintaxis (`print`) | Faltaban incompatibilidades reales: un `TabError` por mezcla de tabs y espacios, y flask-restful roto con Flask 3 (punto 6 del registro) | Compilando el código con Python 3.12 y con una prueba aislada de flask-restful | Corregido en `7f4bfc2` y `54d23b4` |
| 4 | 2026-10-27 | Afirmar que `PUT /api/reservation/<id>` (BUG-2) era el endpoint que usa el frontend y que el flujo "Actualizar reserva" estaba roto | La IA leyó `url: '/api/reservation/:reservation_id'` en la factory y supuso que el id iba en la URL. AngularJS `$resource` no pone en la URL los parámetros del cuerpo de un PUT: el frontend llama a `PUT /api/reservation`, que funcionaba bien | Al probar el flujo en el navegador y mirar las peticiones de red | SPEC y docstrings corregidos; se agregó un test para el endpoint que el frontend usa de verdad. **Lección: verificar con una prueba real, no sólo leyendo el código** |
| 5 | 2026-10-27 | Excluir `graphify-out/` del repositorio "porque contiene rutas locales" | Sólo 2 archivos chicos tenían rutas de la PC; el grafo, la caché y el manifiesto son portables. Excluirlo impedía que el equipo lo compartiera y actualizara | Justin preguntó por qué no estaba en el repo; se verificó archivo por archivo | Se versiona todo salvo `.graphify_python` y `.graphify_root` |
| 6 | 2026-10-27 | Afirmar "todo está subido al PR #1" después de hacer push de Docker, el grafo y docs | El PR #1 ya estaba mergeado: esos 6 commits quedaron en la rama, fuera de `develop` y de `main`. La IA no consultó el estado del PR antes de afirmarlo (incluso editó la descripción de un PR cerrado) | Al verificar el Caso 0 en GitHub antes de arrancar el Caso 2 | PR nuevo con los commits faltantes. **Lección: consultar el estado real (PR, rama) antes de afirmar que algo quedó subido** |

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
| 7 | 2026-10-27 | Arrancar el Caso 2 desde `develop` sin esperar la revisión de los commits faltantes del Caso 0 | Justin | La migración ya está en `develop`; lo que falta (Docker, grafo) no bloquea el calendario y se trae con `git merge` cuando se apruebe |
