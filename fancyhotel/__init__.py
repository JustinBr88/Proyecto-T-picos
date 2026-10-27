"""Fancy Hotel: sistema de reservas web.

Estructura del paquete:
    api/        Capa HTTP: recursos REST (validan la petición y arman la respuesta).
    db/         Capa de datos: conexión, esquema, consultas SQL y datos semilla.
    static/     Frontend AngularJS (controladores, vistas y librerías).
    templates/  Página principal que carga el frontend.
"""
from flask import Flask, render_template
from flask_restful import Api

from fancyhotel import cli
from fancyhotel.api import register_routes
from fancyhotel.config import Config
from fancyhotel.db import connection


def create_app(config_overrides=None):
    """Crea y configura la aplicación (patrón *application factory* de Flask)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    connection.init_app(app)
    cli.init_app(app)
    register_routes(Api(app))

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
