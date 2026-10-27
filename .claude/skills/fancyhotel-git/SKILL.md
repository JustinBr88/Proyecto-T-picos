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

- Dos ramas permanentes y protegidas: **`develop`** (integración) y **`main`** (versión estable). Nunca `push` directo ni `push --force` a ninguna de las dos.
- Las ramas de los casos ya existen en GitHub y salen de `develop`; su PR va **contra `develop`**, nunca contra `main`. Correcciones sueltas: `fix/descripcion-corta`, también desde `develop`.
- `main` sólo recibe un PR `develop → main` al cerrar una fase, después de la regresión.
- Commits en inglés con [Conventional Commits](https://www.conventionalcommits.org/es/) y el issue al final: `tipo(ámbito): descripción (#N)`.
- Commits chicos y con un solo propósito: es la evidencia de "commits identificables".
- **Sin** líneas `Co-Authored-By` ni firmas de IA en los commits: el uso de IA se documenta en el AI Log y en el PR.
- Antes de abrir el PR: `git pull --rebase origin develop`, `pytest` en verde y el grafo actualizado en el último commit (`graphify update .` si sólo cambió código; `/graphify . --update` si cambió documentación). Ver README, "Grafo del proyecto".
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
6. Mergeado a `develop` e issue cerrado a mano (GitHub sólo los cierra solo al mergear en `main`).

## Issues

| Caso | Issue |
|---|---|
| 0 | #2 |
| 1 | #3 |
| 2 | #4 |
| 3 | #5 |
| 4 | #6 |
| 5 | #7 |

## Comandos

```bash
git fetch origin
git switch feature/caso-2-calendario            # la rama ya existe en GitHub
git merge origin/develop                        # traer lo último de develop
git add -p                                      # revisar lo que entra en el commit
git commit -m "feat(calendar): add availability endpoint (#4)"
git pull --rebase origin develop
pytest
git push
gh pr create --base develop --fill              # o desde GitHub (base: develop)
```

## Recursos

- Reglas completas: [docs/SPEC.md](../../../docs/SPEC.md) §5 · Fases y dependencias entre casos: [docs/FASES.md](../../../docs/FASES.md)
- Qué poner en el PR: skill `fancyhotel-docs`
