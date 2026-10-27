"""Búsqueda de habitaciones."""
from flask_restful import Resource, reqparse

from fancyhotel.db import rooms


class SearchRoomsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("location", type=str, required=True, location="args",
                                   help="Please select a location")
        self.reqparse.add_argument("checkIn", type=str, required=True, location="args",
                                   help="Please select a check-in date")
        self.reqparse.add_argument("checkOut", type=str, required=True, location="args",
                                   help="Please select a check-out date")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return rooms.search_rooms(args["location"], args["checkIn"], args["checkOut"])
