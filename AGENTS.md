# Guía para agentes de IA — Fancy Hotel

Instrucciones para cualquier asistente de IA que trabaje en este repositorio (Claude Code, Codex, Cursor, Copilot, etc.).

## Contexto

Proyecto universitario: Feature Sprint con IA sobre un sistema de reservas existente. **Se evalúa el proceso**: cómo se usa la IA, cómo se valida, qué se corrige y qué se rechaza. Antes de cambiar código, leé [docs/SPEC.md](docs/SPEC.md) (casos, criterios de aceptación y bugs conocidos) y [docs/FASES.md](docs/FASES.md).

## Reglas para el agente

1. **Analizá antes de modificar**: leé los archivos que vas a tocar y verificá las APIs de las librerías en su código o documentación. No supongas por nombres de archivo (ver AI_LOG, respuesta incorrecta #1).
2. Mantené la arquitectura: `fancyhotel/api/` (HTTP) y `fancyhotel/db/` (SQL), un módulo por dominio.
3. No cambies las URLs ni la forma de las respuestas de la API sin actualizar `static/js/controllers.js`.
4. Todo cambio de comportamiento lleva tests; todo bug corregido, un test de regresión.
5. Si tu propuesta fue corregida o rechazada por una persona, o te equivocaste, recordale que lo anote en [docs/AI_LOG.md](docs/AI_LOG.md).
6. Commits en inglés con Conventional Commits y el número de issue, **sin** líneas `Co-Authored-By` ni firmas de IA.
7. Nunca subas secretos ni archivos `.env`.

## Skills del proyecto

Están en `.claude/skills/`. Cargá la que corresponda **antes** de escribir código.

| Skill | Para qué | Archivo |
|---|---|---|
| `fancyhotel-backend` | Endpoints, recursos REST, SQL, esquema, configuración | [SKILL.md](.claude/skills/fancyhotel-backend/SKILL.md) |
| `fancyhotel-frontend` | AngularJS: factories, controladores, vistas, datetimepicker, gráficos | [SKILL.md](.claude/skills/fancyhotel-frontend/SKILL.md) |
| `fancyhotel-testing` | pytest unitario e integración, casos manuales de QA | [SKILL.md](.claude/skills/fancyhotel-testing/SKILL.md) |
| `fancyhotel-docs` | AI Development Log, README, SPEC, descripción de PR | [SKILL.md](.claude/skills/fancyhotel-docs/SKILL.md) |
| `fancyhotel-git` | Ramas por caso, commits, Pull Requests, roles y Definition of Done | [SKILL.md](.claude/skills/fancyhotel-git/SKILL.md) |

| Si vas a… | Cargá |
|---|---|
| Tocar `fancyhotel/api/` o `fancyhotel/db/` | `fancyhotel-backend` + `fancyhotel-testing` |
| Tocar `fancyhotel/static/` o `templates/` | `fancyhotel-frontend` |
| Escribir o arreglar tests, o hacer de QA | `fancyhotel-testing` |
| Hacer un commit, crear una rama o abrir un PR | `fancyhotel-git` + `fancyhotel-docs` |
| Registrar uso de IA, una decisión o un error de la IA | `fancyhotel-docs` |

## Comandos

```bash
# Todo en Docker
docker compose up --build                  # app + MySQL → http://localhost:5000
docker compose exec app pytest             # tests dentro del contenedor

# App en el venv local
docker compose up -d mysql                 # sólo MySQL
flask --app fancyhotel seed-db             # base con datos de prueba
python run.py                              # http://localhost:5000
pytest                                     # tests
```
