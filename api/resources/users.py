from flask import request, Response
from flask_restful import Resource

from models import UserModel


class User(Resource):
    """Handles the User REST resource."""

    def get():
        """To fetch user data and perform retrievals."""
        request_data = request.get_json()

    def post() -> Response:
        """To create users."""
        request_data = request.json
        user_create_errors(request_data)
        user = UserModel(email=request_data['email'], first_name=request_data['first_name'], last_name=request_data['last_name'])
        return Response("User Creation successful.", status=200)
        

    def update():
        """To modify users."""

    def delete():
        """To delete users."""


def user_create_errors(request_data) -> Response:
    """To respond to requests with incomplete data."""
    if "email" not in request_data:
        return Response("Email required for user creation.", status=400)
    if "first_name" not in request_data:
        return Response("First name required for user creation.", status=400)
    if "last_name" not in request_data:
        return Response("Last name required for user creation.", status=400)
