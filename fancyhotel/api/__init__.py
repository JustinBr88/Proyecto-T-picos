"""Capa HTTP: recursos REST agrupados por dominio.

Todas las rutas de la API se registran aquí, así que este archivo es el mapa
completo de endpoints. Las URLs son las mismas de la app original porque el
frontend (static/js/controllers.js) las usa tal cual.

Nota sobre flask-restful con Flask 3: cada argumento de reqparse declara su
`location` ("args" para la query string, "json" para el cuerpo). Sin eso, los
GET responden 415 porque reqparse intenta leer un cuerpo JSON que no existe.
"""
from fancyhotel.api import auth, payments, reports, reservations, reviews, rooms


def register_routes(api):
    # Autenticación
    api.add_resource(auth.LoginResource, "/api/login")
    api.add_resource(auth.NewUserRegistrationResource, "/api/register")

    # Habitaciones
    api.add_resource(rooms.SearchRoomsResource, "/api/searchRoom")
    api.add_resource(rooms.AvailabilityResource, "/api/availability")

    # Reservas
    api.add_resource(reservations.CreateReservationResource, "/api/reservation/create")
    api.add_resource(reservations.UpdateReservationResource, "/api/reservation")
    api.add_resource(reservations.GetReservationByCardNumberResource, "/api/reservation/cardNumber")
    api.add_resource(reservations.ReservationResource, "/api/reservation/<string:reservation_id>")
    api.add_resource(reservations.UpdateReservationConfirmResource,
                     "/api/reservation/<string:reservation_id>/availability")
    api.add_resource(reservations.CancelReservationResource, "/api/reservation/<string:reservation_id>/cancel")

    # Pagos
    api.add_resource(payments.CreditCardResource, "/api/payment")

    # Reseñas
    api.add_resource(reviews.ReviewResource, "/api/review")

    # Reportes (managers)
    api.add_resource(reports.ReservationReportResource, "/api/reports/reservation")
    api.add_resource(reports.PopularRoomReportResource, "/api/reports/popularRoom")
    api.add_resource(reports.RevenueReportResource, "/api/reports/revenue")
