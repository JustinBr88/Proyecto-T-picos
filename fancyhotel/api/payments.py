"""Tarjetas de crédito del cliente."""
from datetime import datetime

from flask_restful import Resource, reqparse

from fancyhotel.db import payments, reservations


class CreditCardResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="args",
                                   help="Please provide a username")

        self.delete_reqparse = reqparse.RequestParser()
        self.delete_reqparse.add_argument("username", type=str, required=True, location="args",
                                          help="Please provide a username")
        self.delete_reqparse.add_argument("card_number", type=str, required=True, location="args",
                                          help="Please provide a card number")

        self.create_reqparse = reqparse.RequestParser()
        self.create_reqparse.add_argument("username", type=str, required=True, location="json",
                                          help="Please provide a username")
        self.create_reqparse.add_argument("card_number", type=str, required=True, location="json",
                                          help="Please provide a card_number")
        self.create_reqparse.add_argument("name", type=str, required=True, location="json",
                                          help="Please provide a name")
        self.create_reqparse.add_argument("cvv", type=str, required=True, location="json",
                                          help="Please provide a cvv")
        self.create_reqparse.add_argument("expiration_date", type=str, required=True, location="json",
                                          help="Please provide a expiration_date")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return payments.get_credit_cards(args["username"])

    def post(self):
        args = self.create_reqparse.parse_args()
        message, status = payments.add_credit_card(args["username"], args["card_number"], args["cvv"],
                                                   args["expiration_date"], args["name"])
        return {"message": message, "result": status}, (200 if status else 400)

    def delete(self):
        """No permite borrar una tarjeta usada en una reserva que aún no terminó."""
        args = self.delete_reqparse.parse_args()
        today = datetime.now()
        for reservation in reservations.get_reservation_by_card_number(args["username"], args["card_number"]):
            if (datetime.strptime(reservation["checkout_date"], "%Y-%m-%d") - today).days > 0:
                return {"message": "This card is used in a future reservation!", "result": False}, 400

        message, status = payments.delete_credit_card(args["username"], args["card_number"])
        return {"message": message, "result": status}, (200 if status else 400)
