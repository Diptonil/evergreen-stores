from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from redis.sentinel import Sentinel

from constants import SECRET_KEY, REDIS_MASTER_NAME, REDIS_SENTINEL, REDIS_SOCKET_TIMEOUT
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

# Resources
api.add_resource(User, '/user', resource_class_kwargs={"redis_master": redis_master, "redis_slave": redis_slave})
api.add_resource(Product, '/product', resource_class_kwargs={"redis_master": redis_master, "redis_slave": redis_slave})


if __name__ == '__main__':
    app.run(debug=True, port=5000)