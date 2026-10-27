---
name: fancyhotel-backend
description: >
  Convenciones del backend de Fancy Hotel (Python 3.12, Flask 3, flask-restful, MySQL):
  capas api/ y db/, cómo agregar un endpoint, consultas SQL y conexión.
  Trigger: al crear o modificar endpoints, recursos REST, consultas SQL, el esquema o
  cualquier archivo en fancyhotel/api/, fancyhotel/db/, config.py o cli.py.
license: Apache-2.0
metadata:
  author: equipo-fancyhotel
  version: "1.0"
---

## Cuándo usarla

- Agregar o cambiar un endpoint (`fancyhotel/api/`).
- Escribir o cambiar consultas SQL o tablas (`fancyhotel/db/`).
- Tocar la configuración, la conexión o los comandos `init-db` / `seed-db`.

## Reglas críticas

| Regla | Por qué |
|---|---|
| `api/` valida la petición y arma la respuesta; `db/` sólo habla con MySQL. Un recurso nunca escribe SQL; un módulo de `db/` nunca importa `flask_restful` ni lee `request`. | Separa responsabilidades y permite testear la lógica sin HTTP. |
| Todo argumento de `reqparse` declara `location`: `"args"` en GET/DELETE (query string), `"json"` en POST/PUT. | Sin eso, flask-restful con Flask 3 responde **415** a los GET (BUG-4). |
| Nunca `type=list` en `reqparse` para listas de objetos: leer `request.json` y validar a mano. | `type=list` convierte cada dict en la lista de sus claves. |
| SQL **siempre** parametrizado: `%(nombre)s` + dict. Jamás f-strings ni `+` con datos del usuario. | Inyección SQL. Las f-strings sólo para nombres de tabla fijos del código. |
| Las tablas van **sin** prefijo de base (`FROM Room`, no `FROM Fancy_Hotel.Room`) y con el nombre exacto (`Customer`, no `customer`). | La base se elige por configuración (dev o tests) y MySQL en Docker distingue mayúsculas. |
| Conexión: `get_db()` de `fancyhotel/db/connection.py`. Nunca abrir conexiones propias. | Una conexión por petición; se cierra sola al terminar. |
| Toda escritura hace `db.commit()`; si falla a mitad, `db.rollback()`. | mysql-connector no hace autocommit. |
| Mantener la forma de las respuestas existentes (`{"result": bool, "message": ...}`) y los códigos (400 error de negocio, 401 login, 404 no encontrado). | El frontend (`controllers.js`) depende de esas claves. |
| Cambios de esquema en `fancyhotel/db/schema.py` (diccionario `TABLES`, en orden de dependencias) y, si hace falta, ajustar `db/seed.py`. | `seed-db` recrea todo desde ahí. |
| Lógica de negocio no trivial (fechas, precios, previsión) en **funciones puras** sin BD, con tests unitarios, en un módulo de dominio propio (`fancyhotel/availability.py` es el ejemplo). Nunca dentro de `db/`. | `db/` sólo habla con MySQL; así la regla se testea sin base. Ver skill `fancyhotel-testing`. |

## Agregar un endpoint (receta)

1. **Consulta** en el módulo de dominio de `fancyhotel/db/` (o uno nuevo si es un dominio nuevo).
2. **Recurso** en el módulo de dominio de `fancyhotel/api/`.
3. **Ruta** en `register_routes()` de `fancyhotel/api/__init__.py` (es el mapa de todas las rutas).
4. **Tests** de integración en `tests/integration/`.
5. Si el frontend lo usa: acción nueva en la factory de `controllers.js` (skill `fancyhotel-frontend`).

## Ejemplos

```python
# fancyhotel/db/rooms.py
def get_rooms_by_location(location):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT location, room_number, type, room_cost FROM Room WHERE location = %(location)s",
            {"location": location},
        )
        return [
            {"location": loc, "room_number": number, "room_type": room_type, "cost": cost}
            for (loc, number, room_type, cost) in cursor.fetchall()
        ]
    finally:
        cursor.close()
```

```python
# fancyhotel/api/rooms.py
class RoomListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("location", type=str, required=True, location="args",
                                   help="Please select a location")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return {"response": rooms.get_rooms_by_location(args["location"]), "result": True}

# fancyhotel/api/__init__.py → register_routes()
api.add_resource(rooms.RoomListResource, "/api/rooms")
```

## Comandos

```bash
python run.py                                  # app en http://localhost:5000
flask --app fancyhotel seed-db                 # recrear la base con datos de prueba
flask --app fancyhotel init-db --reset         # base vacía
pytest tests/integration                       # tests contra MySQL
```

## Recursos

- Mapa de rutas: [fancyhotel/api/__init__.py](../../../fancyhotel/api/__init__.py)
- Esquema: [fancyhotel/db/schema.py](../../../fancyhotel/db/schema.py)
- Bugs conocidos y criterios por caso: [docs/SPEC.md](../../../docs/SPEC.md)
