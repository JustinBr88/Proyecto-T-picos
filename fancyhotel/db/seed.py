"""Datos de prueba para desarrollo.

Genera managers, clientes, tarjetas, habitaciones, reseñas y un histórico de
reservas con estacionalidad (más demanda en verano y diciembre), que es lo que
necesita el Caso 3 para la previsión de demanda. También deja reservas futuras
para que el calendario del Caso 2 muestre días ocupados.

Es determinista (semilla fija) pero relativo a la fecha de hoy: dos ejecuciones
el mismo día generan exactamente los mismos datos.

Las reservas generadas nunca se solapan en una misma habitación.

Credenciales de prueba (sólo para desarrollo local):
    Cliente demo:  Cdemo / demo1234
    Manager:       Madmn / admin1234
    Clientes:      C0001 … C0010 / pass1234
"""
import random
from datetime import date, timedelta

from fancyhotel.db.connection import get_db

RANDOM_SEED = 42

# Las mismas locaciones que ofrece el frontend (static/views/searchRoom.html).
LOCATIONS = ["Atlanta", "Charlotte", "Savannah", "Orlando", "Miami"]
LOCATION_PRICE_FACTOR = {"Atlanta": 1.0, "Charlotte": 0.9, "Savannah": 0.95, "Orlando": 1.1, "Miami": 1.25}

# (tipo, números de habitación, costo por noche, capacidad, costo cama extra)
ROOM_TYPES = [
    ("Standard", [101, 102, 103, 104, 105], 89.0, 2, 15.0),
    ("Family", [201, 202, 203], 129.0, 4, 20.0),
    ("Suite", [301, 302], 219.0, 4, 30.0),
]

# Ocupación esperada por mes (1 = enero).
MONTHLY_OCCUPANCY = {1: 0.35, 2: 0.38, 3: 0.45, 4: 0.50, 5: 0.55, 6: 0.70,
                     7: 0.80, 8: 0.75, 9: 0.50, 10: 0.45, 11: 0.45, 12: 0.65}
MAX_NIGHTS = 6
AVERAGE_NIGHTS = (1 + MAX_NIGHTS) / 2
CANCELLATION_RATE = 0.07
EXTRA_BED_RATE = 0.2
FUTURE_DAYS = 60

DEMO_CUSTOMER = ("Cdemo", "demo1234", "Demo", "Cliente", "demo@fancyhotel.test")
MANAGER = ("Madmn", "admin1234")
FIRST_NAMES = ["Ana", "Luis", "María", "Carlos", "Sofía", "Jorge", "Lucía", "Pedro", "Elena", "Diego"]
LAST_NAMES = ["Gómez", "Pérez", "Rodríguez", "Castillo", "Herrera", "Vargas", "Morales", "Ríos", "Núñez", "Torres"]
RATINGS = ["excellent", "good", "Neutral", "bad", "very bad"]
REVIEW_COMMENTS = ["Excelente atención.", "Habitación limpia y cómoda.", "Buena ubicación.",
                   "El desayuno podría mejorar.", "Mucho ruido por la noche.", "Volvería sin dudarlo."]


def _add_months(day, months):
    month_index = day.month - 1 + months
    return date(day.year + month_index // 12, month_index % 12 + 1, 1)


def _daily_start_probability(occupancy):
    """Probabilidad diaria de que empiece una reserva para lograr la ocupación dada.

    Si una reserva dura en promedio L noches y empieza con probabilidad p en cada
    día libre, la ocupación es L / (L + (1 - p) / p). Despejando p:
    """
    return occupancy / (AVERAGE_NIGHTS * (1 - occupancy) + occupancy)


def build_customers():
    customers = [DEMO_CUSTOMER]
    for i in range(1, 11):
        first, last = FIRST_NAMES[i - 1], LAST_NAMES[i - 1]
        customers.append((f"C{i:04d}", "pass1234", first, last, f"cliente{i}@fancyhotel.test"))
    return customers


def build_cards(customers, today):
    """Una tarjeta por cliente (dos para el cliente demo). Devuelve filas y un mapa usuario → tarjeta."""
    rows, card_by_user = [], {}
    for index, (username, _, first, last, _) in enumerate(customers):
        cards_for_user = 2 if username == DEMO_CUSTOMER[0] else 1
        for n in range(cards_for_user):
            card_number = f"4000{index:04d}{n:08d}"
            expiration = date(today.year + 2 + n, (index % 12) + 1, 1)
            rows.append((card_number, f"{first} {last}", "123", expiration, username))
            card_by_user.setdefault(username, card_number)
    return rows, card_by_user


def build_rooms():
    rows = []
    for location in LOCATIONS:
        factor = LOCATION_PRICE_FACTOR[location]
        for room_type, numbers, cost, capacity, extra_bed in ROOM_TYPES:
            for number in numbers:
                rows.append((location, number, room_type, round(cost * factor, 2), capacity, extra_bed))
    return rows


def build_reservations(rng, rooms, customers, card_by_user, start, end):
    """Recorre cada habitación día por día y va creando reservas que no se solapan."""
    usernames = [c[0] for c in customers]
    reservations, reserved_rooms = [], []
    reservation_id = 0

    for location, number, _, cost, _, extra_bed_price in rooms:
        day = start
        while day < end:
            if rng.random() >= _daily_start_probability(MONTHLY_OCCUPANCY[day.month]):
                day += timedelta(days=1)
                continue

            nights = rng.randint(1, MAX_NIGHTS)
            checkout = day + timedelta(days=nights)
            extra_bed = rng.random() < EXTRA_BED_RATE
            cancelled = rng.random() < CANCELLATION_RATE
            total_cost = 0 if cancelled else round((cost + (extra_bed_price if extra_bed else 0)) * nights, 2)
            username = rng.choice(usernames)

            reservation_id += 1
            reservations.append((reservation_id, day, checkout, total_cost, username,
                                 card_by_user[username], "1" if cancelled else "0"))
            reserved_rooms.append((location, number, reservation_id, "1" if extra_bed else "0"))
            day = checkout

    return reservations, reserved_rooms


def build_reviews(rng, customers):
    rows = []
    for location in LOCATIONS:
        for _ in range(3):
            rows.append((location, rng.choice(REVIEW_COMMENTS), rng.choice(RATINGS), rng.choice(customers)[0]))
    return rows


def seed_database(history_months=15, today=None):
    """Inserta los datos de prueba en una base vacía. Devuelve cuántas filas cargó por tabla."""
    today = today or date.today()
    rng = random.Random(RANDOM_SEED)

    customers = build_customers()
    cards, card_by_user = build_cards(customers, today)
    rooms = build_rooms()
    start = _add_months(today, -history_months)
    end = today + timedelta(days=FUTURE_DAYS)
    reservations, reserved_rooms = build_reservations(rng, rooms, customers, card_by_user, start, end)
    reviews = build_reviews(rng, customers)

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO Manager (username, password) VALUES (%s, %s)", MANAGER)
        cursor.executemany(
            "INSERT INTO Customer (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)",
            customers)
        cursor.executemany(
            "INSERT INTO Credit_Card (card_number, name, cvv, expiration_date, username) VALUES (%s, %s, %s, %s, %s)",
            cards)
        cursor.executemany(
            """INSERT INTO Room (location, room_number, type, room_cost, capacity, extra_bed_price)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            rooms)
        cursor.executemany(
            """INSERT INTO Reservation
            (reservation_id, checkin_date, checkout_date, total_cost, username, card_number, cancelled_or_not)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            reservations)
        cursor.executemany(
            """INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id, extra_bed_or_not)
            VALUES (%s, %s, %s, %s)""",
            reserved_rooms)
        cursor.executemany(
            "INSERT INTO Review (location, comment, rating, username) VALUES (%s, %s, %s, %s)",
            reviews)
        db.commit()
    finally:
        cursor.close()

    return {
        "Manager": 1,
        "Customer": len(customers),
        "Credit_Card": len(cards),
        "Room": len(rooms),
        "Reservation": len(reservations),
        "Review": len(reviews),
    }
