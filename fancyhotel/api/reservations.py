"""Crear, consultar, modificar y cancelar reservas."""
from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse

from fancyhotel.db import reservations, rooms

DATE_FORMAT = "%Y-%m-%d"


def nights_between(check_in, check_out):
    return (datetime.strptime(check_out, DATE_FORMAT) - datetime.strptime(check_in, DATE_FORMAT)).days


def change_reservation_dates(username, reservation_id, check_in, check_out):
    """Cambia las fechas de una reserva si todas sus habitaciones están libres y
    recalcula el costo. Devuelve (cuerpo, código HTTP).

    La usan los dos endpoints de actualización. Antes, ReservationResource.put
    (el que llama el frontend) tenía su propia copia rota de esta lógica (BUG-2).
    """
    total_cost = 0
    for room in reservations.get_rooms_for_reservation(username, reservation_id):
        if not rooms.is_room_free(room["room_number"], room["location"], check_in, check_out, reservation_id):
            return {"message": "Some rooms in your reservation are not free during the specified times",
                    "result": False}, 400
        total_cost += room["cost"]
        if room["extra_bed_or_not"] == "1":
            total_cost += room["extra_bed_price"]
    total_cost *= nights_between(check_in, check_out)

    message, status = reservations.update_reservation(username, reservation_id, check_in, check_out, total_cost)
    return {"message": message, "result": status}, (200 if status else 400)


class CreateReservationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="json",
                                   help="Please provide a username")
        self.reqparse.add_argument("checkIn", type=str, required=True, location="json",
                                   help="Please provide a checkIn")
        self.reqparse.add_argument("checkOut", type=str, required=True, location="json",
                                   help="Please provide a checkOut")
        self.reqparse.add_argument("card_number", type=str, required=True, location="json",
                                   help="Please provide a card_number")
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        # "rooms" se lee directo del JSON: reqparse con type=list convierte cada
        # habitación (un dict) en la lista de sus claves.
        selected_rooms = request.json.get("rooms")
        if not isinstance(selected_rooms, list) or not selected_rooms:
            return {"message": {"rooms": "Please provide a list of rooms"}}, 400

        total_cost = 0
        for room in selected_rooms:
            total_cost += room["cost"]
            if room["extra_bed_or_not"] == 1:
                total_cost += room["extra_bed_price"]
        total_cost *= nights_between(args["checkIn"], args["checkOut"])

        reservation_id, message, result = reservations.insert_reservation(
            args["username"], args["checkIn"], args["checkOut"], args["card_number"], selected_rooms, total_cost)
        body = {"id": reservation_id, "message": message, "result": result}
        return (body, 200) if result else (body, 400)


class UpdateReservationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("reservation_id", type=str, required=True, location="json",
                                   help="Please provide a reservation_id")
        self.reqparse.add_argument("checkIn", type=str, required=True, location="json",
                                   help="Please provide a check-in date")
        self.reqparse.add_argument("checkOut", type=str, required=True, location="json",
                                   help="Please provide a check-out date")
        self.reqparse.add_argument("username", type=str, required=True, location="json",
                                   help="Please provide a user name")
        super().__init__()

    def put(self):
        args = self.reqparse.parse_args()
        return change_reservation_dates(args["username"], args["reservation_id"], args["checkIn"], args["checkOut"])


class ReservationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("checkIn", type=str, required=True, location="json",
                                   help="Please provide a check-in date")
        self.reqparse.add_argument("checkOut", type=str, required=True, location="json",
                                   help="Please provide a check-out date")
        self.reqparse.add_argument("username", type=str, required=True, location="json",
                                   help="Please provide a user name")

        self.getreqparse = reqparse.RequestParser()
        self.getreqparse.add_argument("username", type=str, required=True, location="args",
                                      help="Please provide a user name")
        super().__init__()

    def get(self, reservation_id):
        args = self.getreqparse.parse_args()
        reservation = reservations.get_reservation(args["username"], reservation_id, False)
        if reservation:
            return {"data": reservation, "result": True}
        return {"error": "No reservation found", "result": False}, 404

    def put(self, reservation_id):
        args = self.reqparse.parse_args()
        return change_reservation_dates(args["username"], reservation_id, args["checkIn"], args["checkOut"])


class UpdateReservationConfirmResource(Resource):
    """Comprueba si las habitaciones de una reserva están libres en otras fechas."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("checkIn", type=str, required=True, location="args",
                                   help="Please provide a check-in date")
        self.reqparse.add_argument("checkOut", type=str, required=True, location="args",
                                   help="Please provide a check-out date")
        self.reqparse.add_argument("username", type=str, required=True, location="args",
                                   help="Please provide a user name")
        super().__init__()

    def get(self, reservation_id):
        args = self.reqparse.parse_args()
        reservation_rooms = reservations.get_rooms_for_reservation(args["username"], reservation_id)
        for room in reservation_rooms:
            if not rooms.is_room_free(room["room_number"], room["location"], args["checkIn"], args["checkOut"],
                                      reservation_id):
                return {"message": "Some rooms in your reservation are not free during the specified times",
                        "result": False}, 400
        return {"message": "Rooms are available", "result": True, "rooms": reservation_rooms}


class CancelReservationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="args",
                                   help="Please provide a user name")
        super().__init__()

    def get(self, reservation_id):
        args = self.reqparse.parse_args()
        message, status = reservations.cancel_reservation(args["username"], reservation_id)
        if status:
            return {"message": "Cancelled reservation", "result": True}
        return {"message": message, "result": False}, 400


class GetReservationByCardNumberResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="args",
                                   help="Please provide a username")
        self.reqparse.add_argument("card_number", type=str, required=True, location="args",
                                   help="Please provide a card number")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return reservations.get_reservation_by_card_number(args["username"], args["card_number"])
