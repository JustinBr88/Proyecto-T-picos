---
name: fancyhotel-docs
description: >
  Cómo documentar en Fancy Hotel: AI Development Log (evidencia del uso de IA que
  pide el enunciado), README, SPEC y descripción de Pull Requests.
  Trigger: después de usar IA de forma significativa, cuando la IA se equivoca o se
  rechaza un cambio, al tomar una decisión de diseño, al cambiar cómo se instala o
  usa el proyecto, o al redactar un PR.
license: Apache-2.0
metadata:
  author: equipo-fancyhotel
  version: "1.0"
---

## Cuándo usarla

El proyecto se evalúa por el **proceso**, no por cuánto código generó la IA. La evidencia vive en `docs/AI_LOG.md` y se escribe **en el momento**, nunca reconstruida al final.

| Pasó esto | Dónde se anota |
|---|---|
| La IA hizo algo que afectó el desarrollo (análisis, código, tests, diagnóstico) | `AI_LOG.md` → **Registro** |
| La IA dio una respuesta incorrecta (código roto, supuesto falso, API inexistente) | `AI_LOG.md` → **Respuestas incorrectas** |
| Se descartó una propuesta de la IA (en el chat o en la revisión del PR) | `AI_LOG.md` → **Cambios rechazados** |
| El equipo decidió algo de diseño o alcance | `AI_LOG.md` → **Decisiones humanas** |
| Cambió cómo instalar, configurar o correr el proyecto | `README.md` |
| Cambió un criterio, se encontró un bug o se resolvió uno | `docs/SPEC.md` (§1 bugs, §3 criterios) |
| Se abre un Pull Request | Descripción del PR (plantilla abajo) |

## Reglas críticas

- **No registrar cada prompt**: sólo lo que cambió el rumbo del desarrollo.
- Cada fila lleva **evidencia**: hash de commit, número de PR o archivo. Sin evidencia no sirve para la presentación.
- La columna "Decisión humana" dice qué hizo la persona: *Aceptado*, *Modificado (qué)*, *Rechazado (por qué)*, *Pendiente de revisión*.
- Una respuesta incorrecta explica **por qué** estaba mal y **cómo se detectó**. Esto vale puntos: no esconder los errores de la IA.
- Numeración correlativa (`#`) en cada tabla; nunca borrar filas, a lo sumo corregirlas.
- Si se usa una herramienta de IA nueva, agregarla a la tabla "Herramientas usadas".
- Fechas en formato `AAAA-MM-DD`.
- Los documentos del proyecto se escriben en español; el código y los commits, en inglés.

## Formatos

```markdown
<!-- Registro -->
| 8 | 2026-11-03 | 2 | Justin | Código | Claude Code | Endpoint de disponibilidad por mes | Generó el endpoint y 4 tests | Modificado: el cálculo de "parcial" estaba invertido | PR #12 |

<!-- Respuestas incorrectas -->
| 4 | 2026-11-03 | Usar `beforeShowDay` en el datepicker | Esa opción no existe en Eonasdan | Al leer la librería | Se usó `disabledDates` |

<!-- Cambios rechazados -->
| 1 | 2026-11-04 | 1 | Guardar el CVV cifrado | Contradice el Caso 4: el CVV no se guarda |

<!-- Decisiones humanas -->
| 5 | 2026-11-04 | Previsión con media móvil de 3 meses | Bethel | Fácil de explicar en la presentación |
```

## Plantilla de Pull Request

```markdown
## Qué cambia
<!-- resumen en 2-3 líneas -->

Closes #<issue>

## Cómo probar
1. `flask --app fancyhotel seed-db`
2. ...

## Tests
- [ ] `pytest` en verde (sin skipped de integración)
- [ ] Criterios cubiertos: CA?.?, CA?.?

## Uso de IA en este PR
<!-- herramienta, qué se pidió, qué se corrigió o rechazó; filas agregadas al AI_LOG -->

## Checklist
- [ ] Reviewer asignado (rol del caso)
- [ ] QA dejó su validación en un comentario
- [ ] AI_LOG actualizado
```

## Comandos

```bash
git log --oneline -10    # hashes para la columna Evidencia
```

## Recursos

- [docs/AI_LOG.md](../../../docs/AI_LOG.md) · [docs/SPEC.md](../../../docs/SPEC.md) · [docs/FASES.md](../../../docs/FASES.md) · [README.md](../../../README.md)
