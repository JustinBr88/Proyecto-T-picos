# HU3 — Previsión de demanda

## Estado de integración

La rama HU3 incorpora manualmente la factory Flask, `api/`, `db/`, Compose, configuración, seed y pruebas base de `main`; `main` no fue modificada. La consulta de HU3 está en `fancyhotel/db/forecast.py`, el recurso HTTP en `fancyhotel/api/reports.py` y la ruta en `fancyhotel/api/__init__.py`. `fancyhotel/api.py` y `fancyhotel/db/mysqldb.py` son archivos heredados sin uso por `run.py`; se conservaron para no eliminar cambios previos sin revisión humana. `fancyhotel/serve.py` es sólo un punto de entrada de compatibilidad; el oficial es `run.py`.

El 28 de octubre de 2026 `python run.py` inició y respondió 200 en `/` y 403 sin sesión en `/api/reports/forecast`. MySQL 8.4.13 inició con el Compose de la rama y Python se conectó a `Fancy_Hotel`. La base de desarrollo se dejó vacía. La base aislada `Fancy_Hotel_test` recibió un conjunto de demostración identificado; el endpoint devolvió Atlanta 1, 2 y 3 noches, Miami 2, 3 y 4, y previsiones de 2 y 3 noches al mes respectivamente. La cancelación de prueba no alteró los conteos. Edge headless confirmó login, portal, consulta a la API, tres instancias Chart.js, filtros y estado de datos insuficientes. No ejecutar `seed-db` sobre una base con datos que se quieran conservar: el comando borra y recrea tablas.

Después se inicializó el entorno **normal** `Fancy_Hotel` sin ejecutar `seed-db`: primero se comprobaron vacías sus siete tablas y luego `python -m fancyhotel.dev_demo` insertó el conjunto de demostración del generador de `main`, con una contraseña de manager generada en el `.env` local. La base quedó con 1 manager, 11 clientes, 50 habitaciones y 4 415 reservas, de ellas 331 canceladas, con check-ins entre 2025-07-01 y 2026-12-26. El inicializador rechaza nuevas inserciones si alguna tabla ya contiene registros. Este histórico es **simulado** y está identificado en la respuesta de la API y en el dashboard mediante `demonstration_data`.

Flask normal (`python run.py`, sin `DB_NAME=Fancy_Hotel_test`) confirmó `SELECT DATABASE() = Fancy_Hotel`. Por HTTP real, el manager obtuvo 200 y 9 286 noches históricas / 2 753 previstas con 12 meses y horizonte 3; Miami/Standard con 6 meses y horizonte 2 devolvió 514 noches históricas. Cliente y anónimo recibieron 403; un filtro inválido, 400. La búsqueda de habitaciones devolvió 10 resultados para Miami y los tres reportes anteriores respondieron 200. Edge headless confirmó el formulario de login, el portal, tres gráficos, el aviso de demostración, los mismos totales y la actualización del filtro. Tras ejecutar toda la suite de pruebas, los conteos y resultados de `Fancy_Hotel` permanecieron iguales.

## Ejecución de esta rama

Desde la raíz del repositorio en WSL, con Docker Desktop e integración WSL disponibles:

```bash
docker version
docker compose up -d mysql
docker compose ps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
# Guardar el valor generado como FLASK_SECRET_KEY en .env
flask --app fancyhotel init-db
python run.py
```

Abrir `http://localhost:5000`. El servidor usa `127.0.0.1:5000`. Para apagar Flask, `Ctrl+C`; para detener MySQL sin borrar datos, `docker compose stop mysql`; para volver a iniciarlo, `docker compose up -d mysql`. Ambos comandos de Docker y la persistencia de datos se comprobaron. Los valores de `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME` siguen `fancyhotel/config.py` y `docker-compose.yml`. Si Flask corre dentro de otro contenedor, `DB_HOST` debe ser `mysql` y `DB_PORT` 3306; si corre en WSL como en la prueba, `127.0.0.1` y el puerto publicado 3306.

Para una demostración en la base aislada, ejecutar `pytest -q` primero y luego `python -m tests.prepare_hu3_demo`. El script se niega a escribir si la base de prueba contiene reservas o si su nombre no termina en `_test`. Ejecutar Flask con `DB_NAME=Fancy_Hotel_test python run.py`; iniciar sesión con `Mtest` / `admin12`, datos de la fixture del proyecto. **No presentar estas reservas de demostración como histórico real.** `pytest` reinicia `Fancy_Hotel_test`, por lo que hay que preparar la demostración de nuevo después de correr la suite.

Para usar la aplicación normal después de confirmar que `Fancy_Hotel` esté vacía, guardar `DEV_MANAGER_PASSWORD` (8–16 caracteres) en `.env` y ejecutar `python -m fancyhotel.dev_demo` una sola vez. El comando no elimina información y se niega a insertar sobre tablas con registros. Arrancar luego con `python run.py`, iniciar sesión como `Madmn` con la contraseña del `.env`, entrar al portal administrativo y seleccionar «Previsión de la demanda». La base normal ya quedó preparada en este entorno: **no hay que ejecutar de nuevo el inicializador**.

## Métricas y método

El histórico usa meses completos anteriores al mes actual. Cada estancia no cancelada aporta una noche por habitación y fecha, desde check-in incluido hasta check-out excluido. Las reservas se cuentan por identificador distinto; las habitaciones, por ubicación y número distintos en cada mes. La ocupación divide noches ocupadas entre habitaciones del inventario **actual** por días del mes. No existe histórico de capacidad, fecha de creación ni fecha de cancelación, por lo que no puede medirse demanda por fecha de compra ni ocupación histórica exacta cuando cambió el inventario.

La previsión usa una media móvil recursiva de tres meses de noches de habitación. Requiere al menos tres meses completos desde el primer mes con estancia en el período seleccionado. Los meses intermedios sin reservas cuentan como cero. El horizonte se limita a 1–6 meses y el histórico a 3–24. El error retrospectivo medio absoluto compara cada mes conocido desde el cuarto con la media de sus tres meses previos. No se modelan estacionalidad, cancelaciones futuras ni cambios de capacidad; los valores previstos son aproximaciones y se redondean a noches enteras. Sin suficiente histórico, la API devuelve `insufficient_data: true` y ninguna previsión.

## API y revisión

`GET /api/reports/forecast?location=&type=&months=12&horizon=3` exige una sesión de manager creada por `/api/login`. Devuelve `history`, `forecast`, `locations`, `room_types`, `backtest_mae`, `insufficient_data` y la base de capacidad. Los parámetros inválidos devuelven 400 y la falta de sesión administrativa devuelve 403. Las consultas usan parámetros; las conexiones y cursores siguen el patrón existente.

La suite final `python -m pytest -q` completó **47 passed** contra MySQL de prueba; `node tests/test_forecast_frontend.js` mostró `Frontend controller contract: OK`. Edge headless mostró 15 noches históricas y 15 previstas sin filtros; al filtrar Miami/Standard, 9 históricas y 6 previstas, con tres gráficos. Al filtrar Atlanta/Suite mostró «Datos insuficientes» y ocultó el indicador previsto. La captura inspeccionada de la demostración se conserva en `docs/evidence/hu3-dashboard-demo.png`; representa datos de prueba, no reservas reales.

Para Reviewer: revisar el cálculo de noches en `forecast.py`, la sesión configurada en `config.py` y `api/auth.py`, la consulta de `db/forecast.py`, la capacidad actual y los archivos heredados sin uso. Para QA: probar dos ubicaciones, categoría, meses vacíos, reserva que cruza mes, cancelación, acceso sin sesión y sin datos. Los reportes administrativos anteriores todavía carecen de autorización en el backend y requieren una tarea de seguridad separada. No se modificaron workflows.

## Tecnología del frontend

La guía académica menciona JavaScript sin framework, pero `main` usa AngularJS 1.4.6 para rutas, controladores y llamadas `$resource`. El dashboard HU3 conserva esa estructura y dibuja los gráficos con Chart.js 2.9.4; el cálculo y los datos provienen de Flask/MySQL. No se añadió otro framework ni se migró el frontend. El equipo debe decidir en su revisión cómo documentar esta discrepancia respecto de la guía. AngularJS y Chart.js se cargan desde CDN y requieren acceso a Internet en el navegador.
