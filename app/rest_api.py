from flask import request
from flask_restful import Resource, reqparse
from app import create_geojson as cg
from app import dead_end_removal as der
from app import perimeter_generator as pg
from app import rate_route

parser = reqparse.RequestParser()


class Waypoint(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return cg.create_green_waypoints(request.form['step'], request.form['waypoints'])

class Route(Resource):
    def post(self):
        return der.remove_dead_end(request.get_json(force=True))

# Umkreis aus 2 Punkten und GeoJSON erstellen
class Perimeter(Resource):
    def post(self):
        return pg.generate(request.get_json(force=True))

class Rate(Resource):
    def post(self):
        return rate_route.ratePoints(request.form['optimal'], request.form['nicest'], request.form['durationOptimal'], request.form['durationNicest'], request.form['distanceOptimal'], request.form['distanceNicest'], request.form['riseOptimal'], request.form['riseNicest'], request.form['slopeOptimal'], request.form['slopeNicest'], request.form['maxUmweg'])

