# Fancy Hotel — Sistema de reservas web

Proyecto 1 de **Tópicos Especiales II** (Prof. Regis Rivera): Feature Sprint con IA sobre una aplicación existente.

- **Equipo:** Ana · Justin · Bethel
- **App base:** [thegrucoder/Hotel-Reservation-System](https://github.com/thegrucoder/Hotel-Reservation-System), migrada a Python 3 y reorganizada (Caso 0)
- **Documentación del proyecto:** [Especificación](docs/SPEC.md) · [Plan de fases](docs/FASES.md) · [AI Development Log](docs/AI_LOG.md)

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 · Flask 3 · flask-restful |
| Frontend | AngularJS 1.4 · Bootstrap 3 · bootstrap-datetimepicker |
| Base de datos | MySQL 8.4 (en Docker) |
| Tests | pytest |

## Estructura

```
.
├── run.py                   Punto de entrada: python run.py
├── fancyhotel/              Aplicación
│   ├── __init__.py          create_app(): arma la app
│   ├── config.py            Configuración (variables de entorno)
│   ├── cli.py               Comandos init-db y seed-db
│   ├── api/                 Capa HTTP: un módulo por dominio
│   │   ├── __init__.py      ← mapa de TODAS las rutas de la API
│   │   ├── auth.py          Registro y login
│   │   ├── rooms.py         Búsqueda de habitaciones
│   │   ├── reservations.py  Reservas
│   │   ├── payments.py      Tarjetas
│   │   ├── reviews.py       Reseñas
│   │   └── reports.py       Reportes de managers
│   ├── db/                  Capa de datos: consultas SQL por dominio
│   │   ├── connection.py    Conexión a MySQL por petición
│   │   ├── schema.py        Tablas
│   │   ├── seed.py          Datos de prueba
│   │   └── users.py, rooms.py, reservations.py, payments.py, reviews.py, reports.py
│   ├── static/              Frontend
│   │   ├── js/controllers.js  Controladores y rutas de AngularJS
│   │   ├── views/             Vistas HTML
│   │   └── libs/              Librerías de terceros
│   └── templates/index.html Página que carga el frontend
├── tests/
│   ├── unit/                Sin base de datos
│   └── integration/         Contra MySQL (base de tests separada)
├── docker-compose.yml       MySQL para desarrollo y tests
└── docs/                    Especificación, fases y AI Log
```

**Regla de capas:** `api/` valida la petición y arma la respuesta; `db/` sólo habla con MySQL. Un recurso de `api/` nunca escribe SQL, y un módulo de `db/` nunca conoce la petición HTTP.

## Puesta en marcha

Requisitos: **Python 3.12** y **Docker Desktop**.

```bash
# 1. Levantar MySQL (la primera vez descarga la imagen)
docker compose up -d

# 2. Crear el entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements-dev.txt

# 3. Crear las tablas y cargar datos de prueba
flask --app fancyhotel seed-db

# 4. Arrancar la app → http://localhost:5000
python run.py
```

Con [uv](https://docs.astral.sh/uv/) el paso 2 es `uv venv --python 3.12` + `uv pip install -r requirements-dev.txt`.

### Configuración

No hace falta configurar nada para desarrollo: los valores por defecto de `fancyhotel/config.py` coinciden con los de `docker-compose.yml`. Para cambiarlos, creá un archivo `.env` en la raíz (está en `.gitignore`):

| Variable | Por defecto | Uso |
|---|---|---|
| `DB_HOST` / `DB_PORT` | `127.0.0.1` / `3306` | Servidor MySQL |
| `DB_USER` / `DB_PASSWORD` | `fancyhotel` / `fancyhotel_dev` | Usuario de la app |
| `DB_NAME` | `Fancy_Hotel` | Base de desarrollo |
| `TEST_DB_NAME` | `Fancy_Hotel_test` | Base de tests (se borra en cada test) |
| `MYSQL_ROOT_PASSWORD` | `root_dev` | Sólo para docker compose |
| `FLASK_DEBUG` | `0` | `1` = recarga automática y errores detallados |

> Si cambiás usuario o contraseña después de haber levantado el contenedor, hay que recrearlo: `docker compose down -v && docker compose up -d`.

### Usuarios de prueba

Los crea `seed-db` (sólo para desarrollo local):

| Rol | Usuario | Contraseña |
|---|---|---|
| Cliente demo (2 tarjetas) | `Cdemo` | `demo1234` |
| Manager | `Madmn` | `admin1234` |
| Clientes | `C0001` … `C0010` | `pass1234` |

El rol se deduce de la primera letra del usuario: `C` = cliente, `M` = manager.

### Comandos de base de datos

```bash
flask --app fancyhotel init-db           # crea las tablas si no existen
flask --app fancyhotel init-db --reset   # borra todo y crea las tablas vacías
flask --app fancyhotel seed-db           # borra todo y carga datos de prueba (15 meses de histórico)
flask --app fancyhotel seed-db --months 24
```

## Tests

```bash
pytest                  # todo
pytest tests/unit       # sólo unitarios (no necesitan MySQL)
pytest -m integration   # sólo integración
```

Si MySQL no está corriendo, los tests de integración aparecen como *skipped* con el motivo.

## Forma de trabajo

Resumen (detalle en [SPEC.md §5](docs/SPEC.md)):

- `develop` es la rama de integración; `main` guarda la versión estable. Ambas protegidas: todo entra por Pull Request aprobado.
- Una rama por caso (`feature/caso-N-descripcion`), que sale de `develop` y vuelve a `develop` con el Reviewer del caso.
- Commits con [Conventional Commits](https://www.conventionalcommits.org/es/) y referencia al issue: `feat(calendar): add availability endpoint (#3)`.
- Cada uso relevante de IA se registra en [docs/AI_LOG.md](docs/AI_LOG.md) **en el momento**, no al final.

## Problemas conocidos

| ID | Descripción | Se resuelve en |
|---|---|---|
| BUG-1 | La disponibilidad no detecta solapamientos parciales de fechas (`db/rooms.py`) | Caso 2 |
| BUG-6 | "Actualizar reserva" muestra costo 0 en pantalla (error en `controllers.js`; el backend guarda bien) | Pendiente |
| — | Contraseñas y CVV guardados en texto plano | Caso 4 |
| — | Los reportes están fijos a agosto y septiembre (`db/reports.py`) | Caso 3 (a evaluar) |
| — | La sesión vive sólo en el navegador (`$rootScope.currentUser`) y la API confía en el `username` que recibe | Fuera de alcance |
