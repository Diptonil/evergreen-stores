from flask import request, Response
from flask_restful import Resource
import redis


class User(Resource):
    """Handles the User REST resource."""

    def __init__(self, redis_master: redis.sentinel.SentinelConnectionPool, redis_slave: redis.sentinel.SentinelConnectionPool) -> None:
        """Initialize master and slave database instances for writes and reads respectively."""
        self.redis_master = redis_master
        self.redis_slave = redis_slave

    def get(self) -> Response:
        """To perform retrieval of user data, if they exist."""
        query_data = request.args.get('user')
        if self.redis_slave.exists("user_%s" % (query_data)) == 0:
            return Response("User does not exist.", status=400)
        return Response(self.redis_slave.hgetall("user_%s" % (query_data)), status=200)

    def post(self) -> Response:
        """To create users if they don't already exist."""
        request_data = request.json
        user_profile_errors(request_data)
        if self.redis_slave.exists("user_%s" % (request_data["email"])) == 1:
            return Response("User already exists.", status=400)
        self.redis_master.hset("user_%s" % (request_data["email"]), mapping={"email": request_data["email"], "first_name": request_data["first_name"], "last_name": request_data["last_name"]})
        return Response("User creation successful.", status=200)
        
    def update(self) -> Response:
        """To modify users if they exist."""
        request_data = request.json
        user_profile_errors(request_data)
        if self.redis_slave.exists("user_%s" % (request_data["email"])) == 0:
            return Response("User does not exist.", status=400)
        self.redis_master.hset("user_%s" % (request_data["email"]), mapping={"email": request_data["email"], "first_name": request_data["first_name"], "last_name": request_data["last_name"]})
        return Response("User updation successful.", status=200)

    def delete(self) -> Response:
        """To delete users, if the exist."""
        request_data = request.json
        if (self.redis_master.delete("user_%s" % (request_data["email"])) == 1):
            return Response("User deletion successful.", status=200)
        return Response("User does not exist.", status=400)


def user_profile_errors(request_data) -> Response:
    """To respond to requests with incomplete data."""
    if "email" not in request_data:
        return Response("Email required for user creation.", status=400)
    if "first_name" not in request_data:
        return Response("First name required for user creation.", status=400)
    if "last_name" not in request_data:
        return Response("Last name required for user creation.", status=400)
