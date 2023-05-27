from flask import request, Response
from flask_restful import Resource
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge


class Metrics(Resource):
    """Responsible to serve Prometheus monitoring data."""

    def __init__(self, prometheus_monitor: dict) -> None:
        self.prometheus_monitor = prometheus_monitor

    def get(self) -> Response:
        """Relay API stats to Prometheus by periodically polling this endpoint."""
        response = list()
        for _, value in self.prometheus_monitor.items():
            response.append(prometheus_client.generate_latest(value))
        return Response(response, status=200, mimetype="text/plain")


def generate_monitoring_stats(endpoint_start_time: float, endpoint_end_time: float, prometheus_monitor: dict):
    """Generates the statistics of every endpoint and reports it to Prometheus."""
    prometheus_monitor["counter"].inc()
    prometheus_monitor["counter"].observe(endpoint_end_time - endpoint_start_time)
