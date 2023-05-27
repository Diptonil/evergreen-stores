import time

from flask import request, Response
from flask_restful import Resource
import redis

from resources.metrics import generate_monitoring_stats


class Product(Resource):
    """Handles the Product REST resource."""

    def __init__(self, redis_master: redis.sentinel.SentinelConnectionPool, redis_slave: redis.sentinel.SentinelConnectionPool, prometheus_monitor: dict) -> None:
        """Initialize master and slave database instances for writes and reads respectively."""
        self.redis_master = redis_master
        self.redis_slave = redis_slave
        self.prometheus_monitor = prometheus_monitor

    def get(self) -> Response:
        """To perform retrieval of product data with their IDs, if they exist."""
        endpoint_start_time = time.time()
        query_data = request.args.get('id')
        if self.redis_slave.exists("product_%s" % (query_data)) == 0:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("Product does not exist in inventory.", status=400)
        response = self.redis_slave.hgetall("product_%s" % (query_data))
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return {"id": response[b"id"].decode(), "name": response[b"name"].decode(), "category": response[b"category"].decode(), "company": response[b"company"].decode(), "is_sold": response[b"is_sold"].decode(), "date_manufactured": response[b"date_manufactured"].decode(), "cost": response[b"cost"].decode()}, 200

    def post(self) -> Response:
        """To create products if they don't already exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        product_profile_errors(request_data)
        if self.redis_slave.exists("product_%s" % (request_data["id"])) == 1:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("Product already exists.", status=400)
        self.redis_master.hset("product_%s" % (request_data["id"]), mapping={"id": request_data["id"], "name": request_data["name"], "category": request_data["category"], "company": request_data["company"], "is_sold": request_data["is_sold"], "date_manufactured": request_data["date_manufactured"], "cost": request_data["cost"]})
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("Product creation successful.", status=200)
        
    def put(self) -> Response:
        """To modify products if they exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        product_profile_errors(request_data)
        if self.redis_slave.exists("product_%s" % (request_data["id"])) == 0:
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("Product does not exist.", status=400)
        self.redis_master.hset("product_%s" % (request_data["id"]), mapping={"id": request_data["id"], "name": request_data["name"], "category": request_data["category"], "company": request_data["company"], "is_sold": request_data["is_sold"], "date_manufactured": request_data["date_manufactured"], "cost": request_data["cost"]})
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("Product updation successful.", status=200)

    def delete(self) -> Response:
        """To delete users, if the exist."""
        endpoint_start_time = time.time()
        request_data = request.json
        if (self.redis_master.delete("product_%s" % (request_data["id"])) == 1):
            endpoint_end_time = time.time()
            generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
            return Response("Product deletion successful.", status=200)
        endpoint_end_time = time.time()
        generate_monitoring_stats(endpoint_start_time, endpoint_end_time, self.prometheus_monitor)
        return Response("Product does not exist.", status=400)


def product_profile_errors(request_data) -> Response:
    """To respond to requests with incomplete data."""
    if "id" not in request_data:
        return Response("Product ID required for product creation.", status=400)
    if "name" not in request_data:
        return Response("Name required for product creation.", status=400)
    if "category" not in request_data:
        return Response("Category required for product creation.", status=400)
    if "company" not in request_data:
        return Response("Company required for product creation.", status=400)
    if "is_sold" not in request_data:
        return Response("Sale status required for product creation.", status=400)
    if "date_manufactured" not in request_data:
        return Response("Manufacture date required for product creation.", status=400)
    if "cost" not in request_data:
        return Response("Cost required for product creation.", status=400)
