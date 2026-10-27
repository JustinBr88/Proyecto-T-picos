"""Comandos de consola init-db y seed-db."""
import pytest

from fancyhotel.db import schema
from fancyhotel.db.connection import get_db

pytestmark = pytest.mark.integration


def _count_rooms(app):
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM Room")
        (count,) = cursor.fetchone()
        cursor.close()
        return count


def test_seed_if_empty_loads_data_into_an_empty_database(app, db):
    with app.app_context():
        schema.init_schema(reset=True)

    result = app.test_cli_runner().invoke(args=["seed-db", "--if-empty", "--months", "2"])

    assert result.exit_code == 0, result.output
    assert "Reservation:" in result.output
    assert _count_rooms(app) == 50


def test_seed_if_empty_never_touches_existing_data(app, db):
    """Lo usa el contenedor al arrancar: no puede borrar lo que ya hay."""
    rooms_before = _count_rooms(app)

    result = app.test_cli_runner().invoke(args=["seed-db", "--if-empty"])

    assert result.exit_code == 0, result.output
    assert "ya tiene datos" in result.output
    assert _count_rooms(app) == rooms_before
