import math
import geojson
import json
import shapely
from shapely.geometry import shape, Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
from app import circle_generator as cg

def calculate_points(start_point):
    #Berechnet aus den erstellten Kreisen die passenden Wegpunkte und gibt sie zurück

    #Parameters:
    #    start_point (Point):Startpunkt der Route (vom User angegeben)

    #Returns:
    #    array:Wegpunkte die in schönen Bereichen liegen
    center_points = list(create_intersection())
    filtered_points = filterPoints(center_points)
    ordered_points = order_points(filtered_points, start_point, [])

    return ordered_points

def create_intersection():
    #Prüft ob es Überschneidungen zwischen Kreise und Wälder/Landschaften gibt
    #und generiert Koordinatenpunkte aus diesen.

    #Returns:
    #    array:Array mit Punkten die auf Strassen innerhalb von schönen Bereichen liegen
    land_cover_list = []
    route_object_list = []

    #einfach die Schnittmenge der Dinge verwenden
    with open('app/static/data/created/land_forest_merge.json') as lc:
        data = geojson.load(lc)
        multi_poly = shape(geojson.MultiPolygon(data['features'][0]['geometry']['coordinates'])).buffer(0)
        poly_list = list(multi_poly)

    with open('app/static/data/created/route_circles.json') as r:
        data = geojson.load(r)
        for feature in data['features']:
            temp_poly = shape(geojson.Polygon(feature['geometry']['coordinates']))
            route_object_list.append(temp_poly)


    features = []
    temp_features = []

    for i in route_object_list:
        for j in poly_list:
            intersect = i.intersection(j)
            if not intersect.is_empty:
                temp_features.append(intersect)

    union = cascaded_union(temp_features)

    roads = points_on_road(list(union))

    center_points = centroid_points(roads)
    #center_points = centroid_points(list(union))

    features.append(geojson.Feature(geometry=union))
    #create_json(features)
    return center_points


def points_on_road(union_poly):
    #Gibt alle Punkte zurück die innerhalb der Überschneidungszone auf Strassen liegen

    #Parameters:
    #    union_poly (Polygon):Die Überschneidungzonen zwischen Kreise der Route und Wälder/Landschaften

    #Returns:
    #    array:Array mit allen gültigen Punkten

    road_obj = []
    temp_list = []

    with open('app/static/data/created/path_road_perimeter.json') as r:
        data = geojson.load(r)

        multi_line = shape(geojson.MultiLineString(data['features'][0]['geometry']['coordinates']))
        road_obj = list(multi_line)

        for i in union_poly:
            counter = 0
            for j in road_obj:
                intersect = i.intersection(j)
                if not intersect.is_empty:
                    temp_list.append(intersect)
                    counter += 1

    return temp_list

def centroid_points(areas):
    #Zentriert die Punkte auf die Mitte der Strassen

    #Parameters:
    #    areas (array):Punkte die auf den Strassen liegen

    #Returns:
    #    array:Array mit allen zentrierten Punkten
    center_points = []
    for i in areas:
        center = [i.centroid.x, i.centroid.y]
        center_points.append(center)

    #create_roadpoints_json(center_points)
    return center_points

def filterPoints(centerPoints):
    #Filtert Punkte die zu nahe aneinander liegen

    #Parameters:
    #    centerPoints (array):Alle Punkte die innerhalb der Überschneidungszone auf Strassen liegen

    #Returns:
    #    array:Array mit der gefilterten Anzahl der übergebenen Punkte
    waypoint_features = []
    valid_list = []
    count = 0

    filteredPoints = check_nearby_waypoint(valid_list, centerPoints)

    for point in filteredPoints:
        geojson_point = shape(Point(point[0], point[1]))
        waypoint_features.append(geojson.Feature(geometry=geojson_point))

    feature_collection = geojson.FeatureCollection(waypoint_features)

    content = geojson.dumps(feature_collection)
    f = open('app/static/data/created/waypoint_circles.json', 'w+')
    f.write(content)

    return filteredPoints

def check_nearby_waypoint(valid_list, remaining_list):
    #Prüft rekursiv ob um einen Wegpunkte weiter Wegpunkte in der Nähe sind und entfernt diese

    #Parameters:
    #    valid_list (array):Array mit den übrigen, gültigen Punkte
    #    remaining_list (array):Array mit allen möglichen Punkte welches mit jedem Durchlauf kleiner wird

    #Returns:
    #    array:Array reduzierten Anzahl an Wegpunkten
    temp_center = Point(remaining_list[0][0], remaining_list[0][1])
    geojson_circle = shape(cg.create_circle(temp_center, 0.003))
    remaining_points = []

    for x in range(len(remaining_list)):
        if(x != 0):
            intersection = geojson_circle.intersection(Point(remaining_list[x][0], remaining_list[x][1]))
            if intersection.is_empty:
                remaining_points.append([remaining_list[x][0], remaining_list[x][1]])

    valid_list.append(remaining_list[0])

    if(len(remaining_points) == 0):
        return valid_list
    else:
        return check_nearby_waypoint(valid_list, remaining_points)

def order_points(points, start_point, ordered_list):
    #Ordnet die Wegpunkte so an, dass sie der Reihe nach im Array liegen.

    #Parameters:
    #    points (array):Alle Punkte die aktuell unsortiert sind
    #    start_point (Point):Der Startpunkt der Route (vom User angegeben)
    #    ordered_list (array):Das Array mit den sortierten Wegpunkten, welches rekursiv gefüllt wird

    #Returns:
    #    array:Das Array mit den sortierten Wegpunkten

    shortest_distance = 0
    saved_i = 0
    tmp_list = []

    for i in range(len(points)):
        pointObject = Point(points[i][0], points[i][1])
        distance = start_point.distance(pointObject)

        if (distance < shortest_distance or shortest_distance == 0):
            shortest_distance = distance
            saved_i = i


    ordered_list.append(points[saved_i])

    for i in range(len(points)):
        if(i != saved_i):
            tmp_list.append(points[i])

    if(len(tmp_list) != 0):
        return order_points(tmp_list, Point(points[saved_i][0], points[saved_i][1]), ordered_list)
    else:
        return ordered_list
