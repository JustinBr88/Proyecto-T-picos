# Graph Report - .  (2026-10-27)

## Corpus Check
- Corpus is ~19,598 words - fits in a single context window. You may not need a graph.

## Summary
- 358 nodes · 561 edges · 25 communities (21 shown, 4 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 70 edges (avg confidence: 0.84)
- Token cost: 232,592 input · 0 output

## Community Hubs (Navigation)
- Skills y reglas de trabajo
- Conexión y capa de datos
- Rutas de la API y comandos CLI
- Tests de integración
- API de reservas
- Configuración, Docker y convenciones
- Generador de datos semilla
- Vistas del frontend
- Contrato API ↔ frontend
- API de autenticación
- API de tarjetas
- API de reportes
- API de reseñas
- API de habitaciones
- Ejemplos de la skill backend
- SQL parametrizado y RNF
- Datos compartidos de tests
- Índice de la capa de datos
- Receta para agregar pantallas

## God Nodes (most connected - your core abstractions)
1. `get_db()` - 36 edges
2. `README - Fancy Hotel` - 21 edges
3. `AI Development Log` - 18 edges
4. `future()` - 15 edges
5. `static/js/controllers.js` - 14 edges
6. `make_reservation()` - 13 edges
7. `Skill fancyhotel-git` - 13 edges
8. `Especificación (SPEC)` - 12 edges
9. `AGENTS.md - Guía para agentes de IA` - 12 edges
10. `seed_database()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Layer rule: api/ validates HTTP, db/ only talks to MySQL` --semantically_similar_to--> `README - Fancy Hotel`  [INFERRED] [semantically similar]
  .claude/skills/fancyhotel-backend/SKILL.md → README.md
- `Unit (no DB) vs integration (MySQL) vs manual QA` --semantically_similar_to--> `Especificación (SPEC)`  [INFERRED] [semantically similar]
  .claude/skills/fancyhotel-testing/SKILL.md → docs/SPEC.md
- `Decisión: reorganizar carpetas durante la migración` --semantically_similar_to--> `Agregar al final en archivos compartidos`  [INFERRED] [semantically similar]
  docs/AI_LOG.md → .claude/skills/fancyhotel-git/SKILL.md
- `Lección: verificar con una prueba real` --semantically_similar_to--> `Analizar antes de modificar`  [INFERRED] [semantically similar]
  docs/AI_LOG.md → AGENTS.md
- `docker compose watch en vez de bind mounts` --semantically_similar_to--> `Carpeta montada vacía: Docker Desktop no comparte disco D`  [INFERRED] [semantically similar]
  README.md → docs/AI_LOG.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **End-to-end endpoint addition across db, api, routes and frontend factory** — _claude_skills_fancyhotel_backend_skill_get_rooms_by_location, _claude_skills_fancyhotel_backend_skill_roomlistresource, _claude_skills_fancyhotel_backend_skill_register_routes, _claude_skills_fancyhotel_frontend_skill_resource_factories, _claude_skills_fancyhotel_backend_skill_add_endpoint_recipe [EXTRACTED 1.00]
- **Bugs resolved during Caso 0 Python 3 migration** — docs_spec_caso_0_puesta_en_marcha, docs_spec_bug_2_put_reservation_id, docs_spec_bug_3_lowercase_customer, docs_spec_bug_4_reqparse_415, docs_spec_bug_5_taberror [EXTRACTED 1.00]
- **Caso 2 availability calendar design (overlap fix, endpoint, datetimepicker)** — docs_spec_caso_2_calendario, docs_spec_bug_1_overlap, docs_spec_overlaps_function, docs_spec_availability_endpoint, _claude_skills_fancyhotel_frontend_skill_eonasdan_datetimepicker [INFERRED 0.85]
- **Errores de la IA por suponer sin verificar** — docs_ai_log_wrong_answer_1_beforeshowday, docs_ai_log_wrong_answer_3_python3_migration, docs_ai_log_wrong_answer_4_bug_2, docs_ai_log_wrong_answer_5_graphify_exclusion, agents_analyze_before_modify, docs_ai_log_lesson_verify_real_test [INFERRED 0.85]
- **Flujo de PR caso -> develop -> main** — _claude_skills_fancyhotel_git_skill_case_branches, _claude_skills_fancyhotel_git_skill_develop_branch, _claude_skills_fancyhotel_git_skill_main_branch, _claude_skills_fancyhotel_git_skill_roles_dev_reviewer_qa, _claude_skills_fancyhotel_git_skill_definition_of_done [EXTRACTED 1.00]
- **Problemas conocidos de la app base** — readme_bug_1, readme_bug_6, readme_plaintext_credentials, readme_client_side_session [EXTRACTED 1.00]

## Communities (25 total, 4 thin omitted)

### Community 0 - "Skills y reglas de trabajo"
Cohesion: 0.05
Nodes (61): fancyhotel-backend skill, Layer rule: api/ validates HTTP, db/ only talks to MySQL, fancyhotel-docs skill, Pull Request template, Record AI usage in the moment, with evidence, $rootScope.currentUser in-memory session, Skill fancyhotel-git, Agregar al final en archivos compartidos (+53 more)

### Community 1 - "Conexión y capa de datos"
Cohesion: 0.07
Nodes (41): close_db(), get_db(), init_app(), Conexión a MySQL. Se abre una conexión por petición y se cierra al terminarla…, Devuelve la conexión de la petición actual, creándola si hace falta., add_credit_card(), delete_credit_card(), get_credit_cards() (+33 more)

### Community 2 - "Rutas de la API y comandos CLI"
Cohesion: 0.09
Nodes (30): command, Capa HTTP: recursos REST agrupados por dominio. Todas las rutas de la API se…, register_routes(), init_app(), init_db_command(), Comandos de consola para preparar la base de datos. flask --app fancyhotel…, seed_db_command(), Config (+22 more)

### Community 3 - "Tests de integración"
Cohesion: 0.10
Nodes (25): parametrize, make_reservation(), Crea una reserva por la API y devuelve su id., test_add_and_delete_card(), test_cannot_delete_card_used_in_future_reservation(), test_reservations_by_card_number(), _get(), PUT /api/reservation con el id en el cuerpo: es el que llama el frontend… (+17 more)

### Community 4 - "API de reservas"
Cohesion: 0.11
Nodes (15): CancelReservationResource, change_reservation_dates(), CreateReservationResource, GetReservationByCardNumberResource, nights_between(), Resource, Crear, consultar, modificar y cancelar reservas., Comprueba si las habitaciones de una reserva están libres en otras fechas. (+7 more)

### Community 5 - "Configuración, Docker y convenciones"
Cohesion: 0.09
Nodes (26): reqparse arguments must declare location (args/json), schema.py TABLES dictionary, fancyhotel-frontend skill, No build: libraries via CDN with exact version or static/libs, Fancy_Hotel_test recreated before each test, app service (fancyhotel-app), grant-test-db inline config, mysql service (mysql:8.4) (+18 more)

### Community 6 - "Generador de datos semilla"
Cohesion: 0.13
Nodes (24): _add_months(), build_cards(), build_customers(), build_reservations(), build_reviews(), build_rooms(), _daily_start_probability(), is_empty() (+16 more)

### Community 7 - "Vistas del frontend"
Cohesion: 0.23
Nodes (16): cancelReservation.html view, login.html view, payment.html view, popularRoomCatReport.html view, registerUser.html view, reservationReport.html view, revenueReport.html view, searchRoom.html view (+8 more)

### Community 8 - "Contrato API ↔ frontend"
Cohesion: 0.17
Nodes (13): Add endpoint recipe (db query, resource, route, tests, factory), register_routes() route map, API response shape {result, message} and status codes, Eonasdan bootstrap-datetimepicker (file named bootstrap-datepicker.js), reservationController, $resource factories (authFactory, reservationFactory, paymentFactory, reviewFactory, reportFactory), Regression test per fixed bug with bug ID in docstring, Test first for pure logic (+5 more)

### Community 9 - "API de autenticación"
Cohesion: 0.28
Nodes (4): LoginResource, NewUserRegistrationResource, Resource, Registro e inicio de sesión.

### Community 10 - "API de tarjetas"
Cohesion: 0.22
Nodes (4): CreditCardResource, Resource, Tarjetas de crédito del cliente., No permite borrar una tarjeta usada en una reserva que aún no terminó.

### Community 11 - "API de reportes"
Cohesion: 0.28
Nodes (5): PopularRoomReportResource, Resource, Reportes para managers., ReservationReportResource, RevenueReportResource

### Community 12 - "API de reseñas"
Cohesion: 0.29
Nodes (3): Resource, Reseñas por locación., ReviewResource

### Community 14 - "API de habitaciones"
Cohesion: 0.33
Nodes (3): Resource, Búsqueda de habitaciones., SearchRoomsResource

### Community 15 - "Ejemplos de la skill backend"
Cohesion: 0.67
Nodes (3): get_db() per-request connection, get_rooms_by_location (example), RoomListResource (example)

## Knowledge Gaps
- **26 isolated node(s):** `FancyHotelApp Angular module`, `get_db() per-request connection`, `register_routes() route map`, `schema.py TABLES dictionary`, `RoomListResource (example)` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_db()` connect `Conexión y capa de datos` to `Rutas de la API y comandos CLI`, `API de reservas`, `Generador de datos semilla`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `future()` connect `Tests de integración` to `Rutas de la API y comandos CLI`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Fase 2 — Casos 1, 2, 3 en paralelo` connect `Configuración, Docker y convenciones` to `Contrato API ↔ frontend`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `README - Fancy Hotel` (e.g. with `Layer rule: api/ validates HTTP, db/ only talks to MySQL` and `$rootScope.currentUser in-memory session`) actually correct?**
  _`README - Fancy Hotel` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `static/js/controllers.js` (e.g. with `cancelReservation.html view` and `login.html view`) actually correct?**
  _`static/js/controllers.js` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FancyHotelApp Angular module`, `get_db() per-request connection`, `register_routes() route map` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Skills y reglas de trabajo` be split into smaller, more focused modules?**
  _Cohesion score 0.05222734254992319 - nodes in this community are weakly interconnected._