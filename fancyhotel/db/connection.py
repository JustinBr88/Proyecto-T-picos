"""Conexión a MySQL.

Se abre una conexión por petición y se cierra al terminarla (patrón del tutorial
oficial de Flask). La app original abría una única conexión global al importar
el módulo, lo que impedía usar otra base en los tests y se caía cuando MySQL
cerraba la conexión por inactividad.
"""
import mysql.connector
from flask import current_app, g


def connect(with_database=True):
    """Abre una conexión nueva usando la configuración de la app actual."""
    config = current_app.config
    params = {
        "host": config["DB_HOST"],
        "port": config["DB_PORT"],
        "user": config["DB_USER"],
        "password": config["DB_PASSWORD"],
    }
    if with_database:
        params["database"] = config["DB_NAME"]
    return mysql.connector.connect(**params)


def get_db():
    """Devuelve la conexión de la petición actual, creándola si hace falta."""
    if "db" not in g:
        g.db = connect()
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
