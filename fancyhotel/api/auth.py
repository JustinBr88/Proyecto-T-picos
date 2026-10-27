"""Registro e inicio de sesión."""
from flask_restful import Resource, reqparse

from fancyhotel.db import users


class NewUserRegistrationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="json",
                                   help="Username is required to register")
        self.reqparse.add_argument("email", type=str, required=True, location="json",
                                   help="Email is required to register")
        self.reqparse.add_argument("password", type=str, required=True, location="json",
                                   help="Password is required to register")
        self.reqparse.add_argument("firstName", type=str, required=True, location="json",
                                   help="First name is required to register")
        self.reqparse.add_argument("lastName", type=str, required=True, location="json",
                                   help="Last name is required to register")
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if users.user_exists(args["username"]) or users.email_exists(args["email"]):
            return {"error": "This user already exists", "result": False}, 400

        users.register_user(args["username"], args["email"], args["password"],
                            args["firstName"], args["lastName"])
        return {"message": "User successfully created", "result": True}


class LoginResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True, location="json",
                                   help="Username is required to sign in")
        self.reqparse.add_argument("password", type=str, required=True, location="json",
                                   help="Password is required to sign in")
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if users.login(args["username"], args["password"]):
            return {"message": "You logged in!", "result": True}
        return {"error": "Login information invalid. Check your username or password", "result": False}, 401
