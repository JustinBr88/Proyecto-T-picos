"""Configuración de la aplicación, leída de variables de entorno (archivo .env)."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "fancyhotel")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "Fancy_Hotel")

    # Base separada que usan los tests: nunca debe ser la de desarrollo.
    TEST_DB_NAME = os.getenv("TEST_DB_NAME", "Fancy_Hotel_test")

    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
