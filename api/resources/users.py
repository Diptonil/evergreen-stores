import time

from flask import request, Response
from flask_restful import Resource
import redis

from resources.metrics import generate_monitoring_stats


class User(Resource):
    """Handles the User REST resource."""

    def __init__(self, redis_master: redis.sentinel.SentinelConnectionPool, redis_slave: redis.sentinel.SentinelConnectionPool, prometheus_monitor: dict) -> None:
        """Initialize master and slave database instances for writes and reads respectively."""
        self.redis_master = redis_master
        self.redis_slave = redis_slave
        self.prometheus_monitor = prometheus_monitor

    def get(self) -> Response:
        """To perform retrieval of user data, if they exist."""
        endpoint_start_time = time.time()
        query_data = request.args.get('user')
        if self.redis_slave.exists("user_%s" % (query_data)) == 0:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("User does not exist.", status=400)
        response = self.redis_slave.hgetall("user_%s" % (query_data))
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return {"email": response[b"email"].decode(), "first_name": response[b"first_name"].decode(), "last_name": response[b"last_name"].decode()}, 200

    def post(self) -> Response:
        """To create users if they don't already exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        user_profile_errors(request_data)
        if self.redis_slave.exists("user_%s" % (request_data["email"])) == 1:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("User already exists.", status=400)
        self.redis_master.hset("user_%s" % (request_data["email"]), mapping={"email": request_data["email"], "first_name": request_data["first_name"], "last_name": request_data["last_name"]})
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("User creation successful.", status=200)
        
    def put(self) -> Response:
        """To modify users if they exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        user_profile_errors(request_data)
        if self.redis_slave.exists("user_%s" % (request_data["email"])) == 0:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("User does not exist.", status=400)
        self.redis_master.hset("user_%s" % (request_data["email"]), mapping={"email": request_data["email"], "first_name": request_data["first_name"], "last_name": request_data["last_name"]})
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("User updation successful.", status=200)

    def delete(self) -> Response:
        """To delete users, if the exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        if (self.redis_master.delete("user_%s" % (request_data["email"])) == 1):
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("User deletion successful.", status=200)
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("User does not exist.", status=400)


def user_profile_errors(request_data) -> Response:
    """To respond to requests with incomplete data."""
    if "email" not in request_data:
        return Response("Email required for user creation.", status=400)
    if "first_name" not in request_data:
        return Response("First name required for user creation.", status=400)
    if "last_name" not in request_data:
        return Response("Last name required for user creation.", status=400)
