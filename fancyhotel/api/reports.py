"""Reportes para managers."""
from flask_restful import Resource

from fancyhotel.db import reports


class ReservationReportResource(Resource):
    def get(self):
        return reports.reservation_report()


class PopularRoomReportResource(Resource):
    def get(self):
        return reports.room_report()


class RevenueReportResource(Resource):
    def get(self):
        return reports.revenue_report()
