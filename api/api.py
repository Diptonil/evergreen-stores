from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.constants import SECRET_KEY
from api.resources.users import CreateUser, RetrieveUser, UpdateUser, DeleteUser

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY


# Resources
api.add_resource(CreateUser, '/user/create')
api.add_resource(RetrieveUser, '/user/get')
api.add_resource(UpdateUser, '/user/update')
api.add_resource(DeleteUser, '/user/delete')


if __name__ == '__main__':
    app.run(debug=True, port=5000)