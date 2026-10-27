# Plan de fases — Proyecto 1

Referencia de requisitos: [SPEC.md](SPEC.md).

```
Fase 0  Preparación ──► Fase 1  Caso 0 (migración) ──► Fase 2  Casos 1, 2, 3 (en paralelo)
                                                            │
                                                            ▼
                         Fase 5  Presentación ◄── Fase 4  Integración ◄── Fase 3  Casos 4, 5
```

Cada fase tiene un **criterio de salida**: no se pasa a la siguiente hasta cumplirlo.

---

## Fase 0 — Preparación (todo el equipo)

**Objetivo:** que los tres trabajen con las mismas reglas antes de tocar código.

| Tarea | Responsable |
|---|---|
| Leer el SPEC completo y acordar cambios | Todos |
| Dar acceso de colaborador a Ana y Bethel en el repo | Justin |
| Crear los issues de los casos 0–5 con sus criterios de aceptación como checklist | Justin |
| Crear las etiquetas `caso-0` … `caso-5`, `bug`, `ia-rechazado` | Justin |
| Proteger `main` (PR obligatorio, 1 aprobación) | Justin |
| Crear `docs/AI_LOG.md` con la tabla y las tres secciones | Ana |
| Crear la plantilla de PR (`.github/pull_request_template.md`) | Bethel |
| Cada integrante instala Python 3.12 y MySQL 8 localmente | Todos |
| Decidir: MySQL local vs. Docker Compose (ver decisiones abiertas) | Todos |

**Criterio de salida:** issues creados, `main` protegida, plantillas en el repo y todos con el entorno instalado.

---

## Fase 1 — Caso 0: puesta en marcha técnica (todo el equipo)

**Objetivo:** app base funcionando en Python 3 con datos y pytest. Bloquea todo lo demás.

**Rama:** `feature/caso-0-migracion` · **Issue:** Caso 0

| Paso | Tarea | Sugerencia de reparto |
|---|---|---|
| 1.1 | Importar el código base al repo (commit inicial intacto, para tener la referencia del "antes") | Justin |
| 1.2 | Migrar a Python 3: `print`, imports relativos (`import api`, `from db...`), dependencias actuales | Justin |
| 1.3 | Configuración por variables de entorno (`python-dotenv`); quitar `root/password` y la conexión a `sys` | Ana |
| 1.4 | Script de seed: managers, clientes, habitaciones en ≥2 locaciones, histórico de 12–18 meses | Bethel |
| 1.5 | pytest + fixture de base `Fancy_Hotel_test` + test de humo | Ana |
| 1.6 | Corregir BUG-3 (`FROM customer`) y decidir BUG-2 (endpoint roto) | Justin |
| 1.7 | README actualizado: cómo instalar, configurar, sembrar datos, correr y testear | Bethel |
| 1.8 | Prueba manual de regresión de todos los flujos existentes | Todos |

**Por qué la hacemos juntos:** es la base de los tres casos siguientes. Si uno la hace solo y los demás no entienden el setup, se traban en la Fase 2.

**Ojo con la IA en esta fase:** la migración Python 2 → 3 y las versiones de Flask / flask_restful son terreno fértil para respuestas desactualizadas o incorrectas. Verificar cada sugerencia contra la documentación oficial y registrar los errores en el AI Log: es la primera evidencia de las restricciones 8 y 9.

**Criterio de salida:** CA0.1 a CA0.6 cumplidos, PR mergeado a `main`.

---

## Fase 2 — Historias obligatorias (en paralelo)

**Objetivo:** desarrollar los Casos 1, 2 y 3 al mismo tiempo, cada uno en su rama.

| Caso | Rama | Dev | Reviewer | QA |
|---|---|---|---|---|
| 1 — Pago guardado | `feature/caso-1-pago-guardado` | Ana | Justin | Bethel |
| 2 — Calendario | `feature/caso-2-calendario` | Justin | Bethel | Ana |
| 3 — Previsión | `feature/caso-3-prevision-demanda` | Bethel | Ana | Justin |

**Ciclo por caso:**
1. **Analizar** el código afectado *antes* de pedirle nada a la IA (lo exige el enunciado). Anotar en el issue qué archivos se tocarán.
2. **Tests primero** para la lógica pura (solapamiento, previsión, validaciones).
3. **Desarrollar** con la herramienta de IA; registrar en el AI Log los prompts que importaron.
4. **PR** con la plantilla → el Reviewer revisa el código.
5. **QA** valida cada criterio de aceptación y comenta el resultado en el PR.
6. **Merge** a `main` y cierre del issue.

**Archivos compartidos (riesgo de conflictos):**
- `api.py`, `serve.py`, `db/mysqldb.py` y `controllers.js` los tocan los tres casos.
- Regla: cada caso agrega sus funciones y recursos **al final** de su sección y hace `git pull --rebase origin main` antes de abrir el PR. Quien mergea segundo resuelve los conflictos.

**Criterio de salida:** los tres PR mergeados, con tests en verde y QA documentado.

---

## Fase 3 — Historias propias

| Caso | Rama | Dev | Reviewer | QA | Depende de |
|---|---|---|---|---|---|
| 4 — Seguridad de credenciales | `feature/caso-4-seguridad` | Ana | Bethel | Justin | Caso 1 mergeado |
| 5 — Gestión de habitaciones | `feature/caso-5-gestion-habitaciones` | Bethel | Justin | Ana | Caso 3 (sólo CA5.6) |

Mismo ciclo que la Fase 2. El Caso 5 puede arrancar antes, durante la Fase 2, si Bethel termina el Caso 3; el criterio CA5.6 se deja para el final.

**Criterio de salida:** los dos PR mergeados.

---

## Fase 4 — Integración y QA final (todo el equipo)

| Tarea | Responsable |
|---|---|
| Regresión completa sobre `main` con una base recién sembrada | Todos (cada uno prueba flujos que **no** desarrolló) |
| Suite completa de pytest en verde | Ana |
| Revisar el AI Log: ¿cada caso tiene al menos una respuesta incorrecta, un cambio rechazado y una decisión humana? | Bethel |
| Verificar la tabla de trazabilidad del SPEC (sección 7) | Justin |
| Tag de versión `v1.0` | Justin |

**Criterio de salida:** `main` estable, tests en verde, AI Log completo.

---

## Fase 5 — Presentación

| Tarea | Responsable |
|---|---|
| Presentación (PowerPoint / Canva) | Todos |
| Guion de demo: un flujo por caso | Todos |
| **Ensayo cruzado:** cada uno presenta y explica un caso que no desarrolló | Todos |
| Simulacro de "pedido de cambio en vivo": uno pide un cambio y otro lo implementa con IA en ~10 min | Todos |

> El presentador se elige al azar y puede haber pedidos de cambio en vivo. Los tres tienen que poder explicar **todos** los casos y moverse por el código.

---

## Decisiones abiertas (resolver en la Fase 0)

| Decisión | Opción A | Opción B | Recomendación |
|---|---|---|---|
| MySQL para desarrollo | Instalación local en cada PC | Docker Compose con MySQL 8 | **B, ya implementada en el Caso 0** (`docker-compose.yml`). Confirmar que Ana y Bethel tienen Docker; si no, sirve un MySQL local con el mismo usuario y contraseña (ver README). |
| Herramienta de gráficos (Caso 3) | Chart.js por CDN | Generar las imágenes en el backend | **A**: encaja con el front actual y no agrega dependencias de Python. |
| Método de previsión (Caso 3) | Media móvil | Regresión lineal + estacionalidad | Arrancar con **A**, pasar a B si hay tiempo. Lo importante es poder explicarlo en la presentación. |
| Mantener flask-restful | Mantenerlo (sin mantenimiento desde 2023, pero funciona con el ajuste de `location`) | Migrar a `MethodView` de Flask | **A** durante el proyecto: cambiarlo tocaría todos los endpoints sin aportar a ninguna historia. |
| Fechas de cada fase | — | — | Pendiente: definir según la fecha de entrega. |
