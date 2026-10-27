"""Reseñas por locación."""
from flask_restful import Resource, reqparse

from fancyhotel.db import reviews


class ReviewResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("location", type=str, required=True, location="args",
                                   help="Please provide a location")

        self.create_reqparse = reqparse.RequestParser()
        self.create_reqparse.add_argument("username", type=str, required=True, location="json",
                                          help="Please provide a username")
        self.create_reqparse.add_argument("comment", type=str, required=True, location="json",
                                          help="Please provide a comment")
        self.create_reqparse.add_argument("rating", type=str, required=True, location="json",
                                          help="Please provide a rating")
        self.create_reqparse.add_argument("location", type=str, required=True, location="json",
                                          help="Please provide a location")
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return reviews.get_reviews(args["location"])

    def post(self):
        args = self.create_reqparse.parse_args()
        message, status = reviews.add_review(args["username"], args["location"], args["comment"], args["rating"])
        return {"message": message, "result": status}, (200 if status else 400)
