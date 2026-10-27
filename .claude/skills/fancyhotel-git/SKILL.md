---
name: fancyhotel-git
description: >
  Flujo de Git de Fancy Hotel: ramas por caso, Conventional Commits con issue,
  Pull Requests con roles Dev / Reviewer / QA y Definition of Done.
  Trigger: al crear una rama, hacer commit, abrir o revisar un PR, mergear o
  crear issues del proyecto.
license: Apache-2.0
metadata:
  author: equipo-fancyhotel
  version: "1.0"
---

## Cuándo usarla

- Empezar a trabajar en un caso, hacer commits, abrir, revisar o mergear un PR.

## Roles por caso

| Caso | Rama | Dev | Reviewer | QA |
|---|---|---|---|---|
| 0 — Migración | `feature/caso-0-migracion` | Equipo | — | — |
| 1 — Pago guardado | `feature/caso-1-pago-guardado` | Ana | Justin | Bethel |
| 2 — Calendario | `feature/caso-2-calendario` | Justin | Bethel | Ana |
| 3 — Previsión | `feature/caso-3-prevision-demanda` | Bethel | Ana | Justin |
| 4 — Seguridad | `feature/caso-4-seguridad` | Ana | Bethel | Justin |
| 5 — Habitaciones | `feature/caso-5-gestion-habitaciones` | Bethel | Justin | Ana |

## Reglas críticas

- `main` está protegida: **todo entra por PR**. Nunca `push` directo ni `push --force` a `main`.
- Una rama por caso, creada desde `main` actualizado. Correcciones sueltas: `fix/descripcion-corta`.
- Commits en inglés con [Conventional Commits](https://www.conventionalcommits.org/es/) y el issue al final: `tipo(ámbito): descripción (#N)`.
- Commits chicos y con un solo propósito: es la evidencia de "commits identificables".
- **Sin** líneas `Co-Authored-By` ni firmas de IA en los commits: el uso de IA se documenta en el AI Log y en el PR.
- Antes de abrir el PR: `git pull --rebase origin main` y `pytest` en verde.
- `api/__init__.py`, `controllers.js` y `db/schema.py` los tocan varios casos: agregar lo nuevo **al final** de su sección para reducir conflictos. Resuelve los conflictos quien mergea segundo.
- El **Reviewer** aprueba el código; el **QA** comenta el resultado de cada criterio. Recién ahí se mergea (*squash* o *merge*, el equipo decide uno y lo mantiene).

| Tipo | Uso |
|---|---|
| `feat` | Funcionalidad nueva |
| `fix` | Corrección de bug |
| `test` | Sólo tests |
| `refactor` | Cambio interno sin cambiar comportamiento |
| `docs` | Documentación (README, SPEC, AI_LOG) |
| `build` | Dependencias, Docker |
| `chore` | Mantenimiento |

## Definition of Done (por historia)

1. Criterios de aceptación cumplidos.
2. Tests automatizados escritos y en verde.
3. PR aprobado por el Reviewer.
4. QA validó y lo dejó comentado en el PR.
5. AI Log actualizado.
6. Mergeado a `main` e issue cerrado.

## Comandos

```bash
git switch main && git pull
git switch -c feature/caso-2-calendario
git add -p                                      # revisar lo que entra en el commit
git commit -m "feat(calendar): add availability endpoint (#3)"
git pull --rebase origin main
pytest
git push -u origin feature/caso-2-calendario
gh pr create --base main --fill                 # o desde GitHub
```

## Recursos

- Reglas completas: [docs/SPEC.md](../../../docs/SPEC.md) §5 · Fases y dependencias entre casos: [docs/FASES.md](../../../docs/FASES.md)
- Qué poner en el PR: skill `fancyhotel-docs`
