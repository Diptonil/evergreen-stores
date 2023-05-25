from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from constants import SECRET_KEY
from resources.users import User

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY


# User Resources
api.add_resource(User, '/user')

# Product Resources


if __name__ == '__main__':
    app.run(debug=True, port=5000)