"""Comandos de consola para preparar la base de datos.

    flask --app fancyhotel init-db            Crea la base y las tablas.
    flask --app fancyhotel init-db --reset    Borra todo y lo vuelve a crear.
    flask --app fancyhotel seed-db            Recrea la base con datos de prueba.
"""
import click
from flask.cli import with_appcontext

from fancyhotel.db import schema, seed


@click.command("init-db")
@click.option("--reset", is_flag=True, help="Borra las tablas existentes antes de crearlas.")
@with_appcontext
def init_db_command(reset):
    schema.init_schema(reset=reset)
    click.echo("Base de datos lista.")


@click.command("seed-db")
@click.option("--months", default=15, show_default=True, help="Meses de histórico de reservas a generar.")
@with_appcontext
def seed_db_command(months):
    schema.init_schema(reset=True)
    summary = seed.seed_database(history_months=months)
    click.echo("Datos de prueba cargados:")
    for name, count in summary.items():
        click.echo(f"  {name}: {count}")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
