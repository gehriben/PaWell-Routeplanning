import geojson
import json
import shapely
from shapely.geometry import shape, Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
from app import circle_generator as cg
from app import calculate_points as cp

STEP_MULTIPLICATOR = 30
INIT_RADIUS = 200

increment_radius = True
switch_step = 0

def create_green_waypoints(step, route_waypoints):
    #Erstellt Kreise um die optimale Route

    #Parameters:
    #    step (number):Die Anzahl Routen die bereits berechnet wurden
    #    route_waypoints (array):Die Wegpunkte der Route

    #Returns:
    #    array:Array mit den Wegpunkten für die neue Route

    global increment_radius
    global switch_step

    route_waypoints = json.loads(route_waypoints)
    step = int(json.loads(step))
    start_point = Point(route_waypoints[0]['lng'], route_waypoints[0]['lat'])
    radius = 0
    route_features = []
    i = 0

    if(step==1):
        increment_radius = True
        switch_step = 0

    if(increment_radius == True):
        radius = INIT_RADIUS + step*STEP_MULTIPLICATOR
        switch_step = switch_step+1
    else:
        radius = INIT_RADIUS - (step-switch_step)*STEP_MULTIPLICATOR

    if(radius < 20):
        radius = 20

    with open('app/static/data/created/path_road_perimeter.json') as r:
        data = geojson.load(r)
        multi_line = shape(geojson.MultiLineString(data['features'][0]['geometry']['coordinates']))
        road_obj = list(multi_line)

    with open('app/static/data/created/land_forest_merge.json') as lc:
        data = geojson.load(lc)
        multi_poly = shape(geojson.MultiPolygon(data['features'][0]['geometry']['coordinates'])).buffer(0)
        poly_list_land_forest = list(multi_poly)

    for i in range(len(route_waypoints)):
        if(check_waypoint(Point(route_waypoints[i]['lng'], route_waypoints[i]['lat']), poly_list_land_forest, road_obj) == True):
            geojson_circle = Polygon(cg.geodesic_point_buffer(route_waypoints[i]['lat'], route_waypoints[i]['lng'], radius))
            route_features.append(geojson.Feature(geometry=geojson_circle))
    feature_collection = geojson.FeatureCollection(route_features)

    content = geojson.dumps(feature_collection)
    f = open('app/static/data/created/route_circles.json', 'w+')
    f.write(content)

    return cp.calculate_points(start_point)

def check_waypoint(point, poly_list, road_obj):
    #Prüft ob ein Wegpunkt nicht bereits in einem schönen Bereich liegt.

    #Parameters:
    #    point (Point):Der Wegpunkt einer Route
    #    poly_list (MultiPolygon): Wälder und Landschaften als Polygon
    #    road_obj (LineString): Strassenabschnitte als Polylines

    #Returns:
    #    boolean:True = Wegpunkt ist gültig und liegt nicht bereits in einem schönen Gebiet

    geojson_circle = shape(cg.create_circle(point, 0.0001))
    road_intersects = False

    for i in road_obj:
        if(geojson_circle.intersects(i) == True):
            road_intersects = True
            break
    
    if (road_intersects == False):
        return True
    else:
        for j in poly_list:
            intersect = j.intersects(point)
            return not intersect

