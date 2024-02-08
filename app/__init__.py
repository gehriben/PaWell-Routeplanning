from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api = Api(app)
CORS(app)

from app import routes
from app import rest_api

api.add_resource(rest_api.Waypoint, '/waypoint')
api.add_resource(rest_api.Route, '/route')
api.add_resource(rest_api.Perimeter, '/perimeter')
api.add_resource(rest_api.Rate, '/rate')

if __name__ == '__init__':
    app.run(debug=True)
