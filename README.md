Online Hotel Reservation System group project for CS 4400
---------------------------------------------------------
Download Mysql from [here]http://dev.mysql.com/downloads/mysql/

Download MySql Workbench from [here](http://dev.mysql.com/downloads/file/?id=459911)

Downlad MySql Community Server from [here](http://dev.mysql.com/downloads/file/?id=459870)

go to fancyhotel folder

run 'python serve.py' 

open 'localhost:5000' in the broswer 


We have to use MySql (per project requirements), going to use it with the MySQL connector for Python. 

UI won't get us any extra points, so feel free to do what you want, but don't waste your time on it if there are other things to do.

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
Things to be done:
* Create login abilities
* Carry logged-in account to do things
* Pretty much all requests, while being logged in
* regex to disallow bad input from registering users
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
Requisitos: **Python 3.12** y **Docker Desktop**.

```bash
# 1. Levantar MySQL (la primera vez descarga la imagen)
docker compose up -d

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
# 2. Crear el entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements-dev.txt

# 3. Crear las tablas y cargar datos de prueba
flask --app fancyhotel seed-db

# 4. Arrancar la app → http://localhost:5000
<<<<<<< Updated upstream
=======
=======
# 2. Crear el entorno virtual e instalar dependencias (WSL / Linux)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# 3. Crear .env con FLASK_SECRET_KEY=<valor aleatorio largo y privado>

# 4. Crear las tablas sin borrar datos existentes
flask --app fancyhotel init-db

# 5. Arrancar la app normal con Fancy_Hotel → http://localhost:5000
>>>>>>> Stashed changes
>>>>>>> Stashed changes
python run.py
```

Con [uv](https://docs.astral.sh/uv/) el paso 2 es `uv venv --python 3.12` + `uv pip install -r requirements-dev.txt`.

### Configuración

<<<<<<< Updated upstream
No hace falta configurar nada para desarrollo: los valores por defecto de `fancyhotel/config.py` coinciden con los de `docker-compose.yml`. Para cambiarlos, creá un archivo `.env` en la raíz (está en `.gitignore`):
=======
<<<<<<< Updated upstream
No hace falta configurar nada para desarrollo: los valores por defecto de `fancyhotel/config.py` coinciden con los de `docker-compose.yml`. Para cambiarlos, creá un archivo `.env` en la raíz (está en `.gitignore`):
=======
Los valores de base de datos por defecto de `fancyhotel/config.py` coinciden con los de `docker-compose.yml`. La clave de sesión sí debe configurarse. Creá un archivo `.env` en la raíz (está en `.gitignore`):
>>>>>>> Stashed changes
>>>>>>> Stashed changes

| Variable | Por defecto | Uso |
|---|---|---|
| `DB_HOST` / `DB_PORT` | `127.0.0.1` / `3306` | Servidor MySQL |
| `DB_USER` / `DB_PASSWORD` | `fancyhotel` / `fancyhotel_dev` | Usuario de la app |
| `DB_NAME` | `Fancy_Hotel` | Base de desarrollo |
| `TEST_DB_NAME` | `Fancy_Hotel_test` | Base de tests (se borra en cada test) |
| `MYSQL_ROOT_PASSWORD` | `root_dev` | Sólo para docker compose |
| `FLASK_DEBUG` | `0` | `1` = recarga automática y errores detallados |
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes

> Si cambiás usuario o contraseña después de haber levantado el contenedor, hay que recrearlo: `docker compose down -v && docker compose up -d`.

### Usuarios de prueba

Los crea `seed-db` (sólo para desarrollo local):
<<<<<<< Updated upstream
=======
=======
| `FLASK_SECRET_KEY` | sin valor | Obligatoria para firmar sesiones administrativas |
| `DEV_MANAGER_PASSWORD` | sin valor | Contraseña de 8–16 caracteres para la carga inicial de demostración |

> Si cambiás usuario o contraseña después de crear el volumen, los valores iniciales de MySQL no cambian automáticamente. Conservá el volumen y revisá usuarios y permisos antes de modificar datos.

### Primera carga de la base normal

`Fancy_Hotel` puede arrancar vacía, pero se necesita un manager, habitaciones y
reservas para probar el portal y la previsión. **Sólo si las siete tablas están
vacías**, agregá a `.env` una contraseña privada de 8–16 caracteres en
`DEV_MANAGER_PASSWORD=` y ejecutá:

```bash
python -m fancyhotel.dev_demo
python run.py
```

El comando reutiliza el generador de `main` para crear 15 meses de **datos de
demostración**, 50 habitaciones, clientes y el manager `Madmn`. Rechaza una base
con cualquier registro; no borra tablas ni sobreescribe información. La cuenta
administrativa es `Madmn` con la contraseña guardada en el `.env` local. El
dashboard muestra un aviso de que las reservas generadas no son reales. No
mezcles estos registros con datos operativos: para datos reales, usa una base
separada y revisa su procedencia antes de tomar decisiones comerciales.

La autenticación heredada guarda contraseñas en texto plano, con longitud máxima
de 16 caracteres. Esta carga se limita a desarrollo local; no uses una contraseña
de producción. `seed-db` sigue disponible por compatibilidad, pero **borra y
recrea las tablas** y no debe utilizarse sobre una base que se quiera conservar.

### Usuarios del generador heredado

Los crea `seed-db` (sólo para desarrollo local). **Estas contraseñas no
corresponden al manager creado por `python -m fancyhotel.dev_demo`**, cuya
contraseña está en el `.env` local:
>>>>>>> Stashed changes
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
=======
node tests/test_forecast_frontend.js  # contrato del controlador HU3
>>>>>>> Stashed changes
>>>>>>> Stashed changes
```

Si MySQL no está corriendo, los tests de integración aparecen como *skipped* con el motivo.

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
=======
### HU3 — Previsión de demanda

Después de cargar datos en una base **de prueba desechable**, iniciar sesión como
manager y abrir `#/forecast` desde el portal. La API es
`GET /api/reports/forecast?location=&type=&months=12&horizon=3`. El comando
`seed-db` **borra y recrea** las tablas de la base configurada: no ejecutarlo
sobre datos que deban conservarse.

Para una demostración sin tocar la base de desarrollo: ejecutar `pytest -q`
(prepara la base aislada `Fancy_Hotel_test`), después
`python -m tests.prepare_hu3_demo` y arrancar con
`DB_NAME=Fancy_Hotel_test python run.py`. Entrar con `Mtest` / `admin12`, cuenta
de la fixture de pruebas. Los datos son **demostrativos**, no reservas reales.
La suite de tests reinicia esa base; volver a preparar la demo después de probar.
Para detener MySQL conservando el volumen: `docker compose stop mysql`.

>>>>>>> Stashed changes
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
>>>>>>> Stashed changes
