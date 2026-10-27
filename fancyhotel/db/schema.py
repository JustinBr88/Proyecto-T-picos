"""Esquema de la base de datos.

Las tablas son las mismas de la app original (antes se creaban en
MysqlManager.init_db). Los nombres ya no llevan el prefijo "Fancy_Hotel." para
que la base se pueda elegir por configuración (desarrollo o tests).
"""
from flask import current_app

from fancyhotel.db.connection import connect

# Orden de creación: cada tabla aparece después de las tablas a las que referencia.
TABLES = {
    "Customer": """
        CREATE TABLE IF NOT EXISTS Customer (
            username CHAR(5) NOT NULL,
            password VARCHAR(16) NOT NULL,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL,
            email VARCHAR(30) NOT NULL,
            PRIMARY KEY (username),
            UNIQUE (email)
        )""",
    "Manager": """
        CREATE TABLE IF NOT EXISTS Manager (
            username CHAR(5) NOT NULL,
            password VARCHAR(16) NOT NULL,
            PRIMARY KEY (username)
        )""",
    "Credit_Card": """
        CREATE TABLE IF NOT EXISTS Credit_Card (
            card_number CHAR(16) NOT NULL,
            name VARCHAR(41) NOT NULL,
            cvv CHAR(3) NOT NULL,
            expiration_date DATE NOT NULL,
            username CHAR(5) NOT NULL,
            PRIMARY KEY (card_number),
            FOREIGN KEY (username) REFERENCES Customer (username)
        )""",
    "Review": """
        CREATE TABLE IF NOT EXISTS Review (
            review_id INT NOT NULL AUTO_INCREMENT,
            location VARCHAR(9) NOT NULL,
            comment VARCHAR(1000) DEFAULT NULL,
            rating VARCHAR(10) NOT NULL,
            username CHAR(5) NOT NULL,
            PRIMARY KEY (review_id),
            FOREIGN KEY (username) REFERENCES Customer (username)
        )""",
    "Reservation": """
        CREATE TABLE IF NOT EXISTS Reservation (
            reservation_id INT NOT NULL AUTO_INCREMENT,
            checkin_date DATE NOT NULL,
            checkout_date DATE NOT NULL,
            total_cost FLOAT NOT NULL DEFAULT 0,
            username CHAR(5) NOT NULL,
            card_number CHAR(16) DEFAULT NULL,
            cancelled_or_not CHAR(1) NOT NULL DEFAULT '0',
            PRIMARY KEY (reservation_id),
            FOREIGN KEY (username) REFERENCES Customer (username),
            FOREIGN KEY (card_number) REFERENCES Credit_Card (card_number) ON DELETE SET NULL
        )""",
    "Room": """
        CREATE TABLE IF NOT EXISTS Room (
            location VARCHAR(9) NOT NULL,
            room_number INT NOT NULL,
            type VARCHAR(20) NOT NULL,
            room_cost FLOAT NOT NULL,
            capacity INT NOT NULL,
            extra_bed_price FLOAT DEFAULT NULL,
            PRIMARY KEY (location, room_number)
        )""",
    "Reserves_Extra_Bed": """
        CREATE TABLE IF NOT EXISTS Reserves_Extra_Bed (
            location VARCHAR(9) NOT NULL,
            room_number INT NOT NULL,
            reservation_id INT NOT NULL,
            extra_bed_or_not CHAR(1) DEFAULT NULL,
            PRIMARY KEY (location, room_number, reservation_id),
            FOREIGN KEY (location, room_number) REFERENCES Room (location, room_number),
            FOREIGN KEY (reservation_id) REFERENCES Reservation (reservation_id)
        )""",
}

VIEWS = ["reservation_by_category"]


def create_database():
    """Crea la base configurada (DB_NAME) si no existe."""
    conn = connect(with_database=False)
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{current_app.config['DB_NAME']}`")
        cursor.close()
    finally:
        conn.close()


def create_tables():
    conn = connect()
    try:
        cursor = conn.cursor()
        for ddl in TABLES.values():
            cursor.execute(ddl)
        cursor.close()
    finally:
        conn.close()


def drop_tables():
    conn = connect()
    try:
        cursor = conn.cursor()
        for view in VIEWS:
            cursor.execute(f"DROP VIEW IF EXISTS {view}")
        for table in reversed(list(TABLES)):
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        cursor.close()
    finally:
        conn.close()


def init_schema(reset=False):
    """Crea la base y las tablas. Con reset=True borra antes todo lo existente."""
    create_database()
    if reset:
        drop_tables()
    create_tables()
