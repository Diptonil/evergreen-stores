from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from redis.sentinel import Sentinel

from constants import SECRET_KEY, HOST, PORT, REDIS_MASTER_NAME, REDIS_SENTINEL, REDIS_SOCKET_TIMEOUT
from resources.metrics import Metrics
from resources.products import Product
from resources.users import User


app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY

# Database Connection
redis_sentinel = Sentinel([(address.split(':')[0], address.split(':')[1]) for address in REDIS_SENTINEL.split(',')], socket_timeout=REDIS_SOCKET_TIMEOUT)
redis_master = redis_sentinel.master_for(REDIS_MASTER_NAME, socket_timeout=REDIS_SOCKET_TIMEOUT)
redis_slave = redis_sentinel.slave_for(REDIS_MASTER_NAME, socket_timeout=REDIS_SOCKET_TIMEOUT)

# Prometheus Configuration
prometheus_monitor = {
    "counter": Counter("python_request_operation_total", "The total number of processed requests."),
    "histogram": Histogram("python_request_duration_seconds", "Histogram for the duration in seconds.", buckets=(1, 2, 5, 6, 10, float("inf")))
}

# Resources
api.add_resource(User, '/user', resource_class_kwargs={"prometheus_monitor": prometheus_monitor, "redis_master": redis_master, "redis_slave": redis_slave})
api.add_resource(Product, '/product', resource_class_kwargs={"prometheus_monitor": prometheus_monitor, "redis_master": redis_master, "redis_slave": redis_slave})
api.add_resource(Metrics, '/metrics', resource_class_kwargs={"prometheus_monitor": prometheus_monitor})


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)