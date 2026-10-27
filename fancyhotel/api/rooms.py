"""Búsqueda de habitaciones y disponibilidad por mes."""
from flask_restful import Resource, reqparse

from fancyhotel import availability
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


class AvailabilityResource(Resource):
    """Estado de cada día de un mes en una locación: libre, parcial o lleno (Caso 2)."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("location", type=str, required=True, location="args",
                                   help="Please select a location")
        self.reqparse.add_argument("month", type=availability.parse_month, required=True, location="args",
                                   help="Please provide a month as YYYY-MM")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        location = args["location"]
        year, month = args["month"]

        total_rooms = rooms.count_rooms(location)
        if total_rooms == 0:
            return {"message": "Unknown location", "result": False}, 404

        start, end = availability.month_range(year, month)
        days = availability.monthly_availability(year, month, total_rooms, rooms.get_stays(location, start, end))
        return {"result": True, "location": location, "month": f"{year:04d}-{month:02d}", "days": days}
