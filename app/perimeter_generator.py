import geojson
import shapely
from shapely.geometry import shape, LineString, Point, Polygon
from shapely.ops import cascaded_union, transform
from app import circle_generator as cg
from geopy.geocoders import Nominatim, GoogleV3
from app import settings

"""
landcover daten verringern auf einen Kreis mit den 2 Standorten
landcover Daten kombinieren mit Nutzflächen

"""
def generate(point_list):
    #Erstellt alle nötigen Geodaten

    #Parameters:
    #    point_list (array) : Array mit Koordinatenpunkte

    #Returns:

    last = len(point_list) - 1

    settings.init()

    """geolocator = GoogleV3(api_key=settings.api_schluessel, domain='maps.googleapis.com')
    location1 = geolocator.geocode(point_list[0], components={"country": "CH"})
    location2 = geolocator.geocode(point_list[1], components={"country": "CH"})"""

    point_a = Point(point_list[0]['lng'], point_list[0]['lat'])
    point_b = Point(point_list[last]['lng'], point_list[last]['lat'])

    circle = create_circle_around(point_a, point_b)
    forest_in_circle, cities_in_circle = generate_perimeter_forest(circle)
    land_space_in_circle = generate_perimeter_with_land(circle)
    united_land_and_forest = merge_land_forest(land_space_in_circle, forest_in_circle)
    roads_in_circle = road_minimizer(circle)
    road_centers = centroid_points(roads_in_circle)
    all_waypoints = filter_road_points(road_centers, united_land_and_forest, 'possible_waypoints.json')
    # road centers ist hier glaube ich falsch
    """all_waypoints_city = filter_road_points(road_centers, cities_in_circle, 'waypoints_in_cities.json')
    #road centers ist hier glaube ich falsch
    all_waypoints_city = filter_road_points(road_centers, cities_in_circle, 'waypoints_in_cities.json')
    print('create all waypoints in city done')
    trees_in_city = filter_trees(cities_in_circle)
    print('all trees in city')
    city_waypoints = find_green_city_waypoints(all_waypoints_city, trees_in_city)
    print('green waypoints in city')
    print('city_waypoints')"""

    return "finished"


def generate_perimeter_forest(circle):
    #Speichert Geodaten aus dem landcover in einem bestimmten Kreis ab, der als Parameter mitgegeben wird.

    #Parameters:
    #    circle (Shapely Object) : Kreis

    #Returns:
    #   union (Shapely Multipolygon) : Landcover Daten, in einem bestimmten Kreis
    #   union_cities (Shapely Multipolygon) : Städte und Siedlungen in einem bestimmten Kreis

    land_cover_list = []
    cities = []
    features = []

    with open('app/static/data/landcover_switzerland.json') as lc:
        data = geojson.load(lc)

        for feature in data['features']:
            if not feature['properties']['objval'] == 'Siedl' and not feature['properties']['objval'] == 'Stadtzentr':
                temp_poly = shape(geojson.MultiPolygon(feature['geometry']['coordinates']))
                temp_intersection = temp_poly.intersection(circle)
                if not temp_intersection.is_empty:
                    land_cover_list.append(temp_poly)
            else:
                temp_poly = shape(geojson.MultiPolygon(feature['geometry']['coordinates']))
                temp_intersection = temp_poly.intersection(circle)
                if not temp_intersection.is_empty:
                    cities.append(temp_poly)

    union = cascaded_union(land_cover_list)
    union_cities = cascaded_union(cities)

    features.append(geojson.Feature(geometry=union))
    create_json(features, 'path_perimeter.json')

    features = []
    features.append(geojson.Feature(geometry=union_cities))
    create_json(features, 'cities.json')

    return union, union_cities



def create_circle_around(point_a, point_b):
    #Erstellt einen Kreis durch 2 Punkte
    #Der Durchmesser des Kreises ist die Distanz zwischen den 2 Punkten und der Mittelpunkt ist in der Mitte beider Punkte

    #Parameters:
    #    point_a (Shapely Point) : Punkt mit Koordinaten
    #    point_b (Shapely Point) : Punkt mit Koordinaten

    #Returns:
    #   geojson_circle (Shapely Polygon): Kreis durch 2 Punkten

    a_to_b = LineString([point_a, point_b])

    center = a_to_b.centroid
    distance = center.distance(point_a)
    temp_circle = center.buffer(distance)
    geojson_circle = shapely.geometry.mapping(temp_circle)

    return shape(geojson_circle)


def create_json(features, filename):
    #Erstellt ein JSON File mit dem GeoJSON Format

    #Parameters:
    #    features (array) : Features eines GeoJSON objekt
    #    filename (string) : Name der zu speichernden Datei

    #Returns:


    feature_collection = geojson.FeatureCollection(features)
    content = geojson.dumps(feature_collection)
    f = open('app/static/data/created/' + filename, 'w+')
    f.write(content)



def road_minimizer(circle):
    #Speichert Geodaten aus dem Strassennetz Datensatz in einem bestimmten Kreis ab, der als Parameter mitgegeben wird.

    #Parameters:
    #    circle (Shapely Object) : Kreis

    #Returns:
    #   union (shapely Polygon) : Alle strassenabschnitte im Kreis

    road_lines = []
    features = []

    with open('app/static/data/strassen.json') as lc:
        data = geojson.load(lc)

        for feature in data['features']:
            road_classification = feature['properties']['OBJEKTART']

            if road_classification == 10 or road_classification == 11 or road_classification == 15 or road_classification == 16:
                temp_poly = shape(geojson.MultiLineString(feature['geometry']['coordinates']))
                temp_intersection = temp_poly.intersection(circle)
                if not temp_intersection.is_empty:
                    road_lines.append(temp_poly)

    union = cascaded_union(road_lines)

    features.append(geojson.Feature(geometry=union))
    create_json(features, 'path_road_perimeter.json')
    return union


def centroid_points(roads):
    #Berechnet die Mittelpunkte von Strassenabschnitten

    #Parameters:
    #    roads (array<Shapely Polyline>) : Kreis

    #Returns:
    #   center_points (shapely Point) : Mittelpunkte aller als Parameter mitgegebenen Strassen

    center_points = []
    for i in roads:
        center_points.append(i.centroid)
    return center_points


def filter_road_points(road_points, land, filename):
    #Nimmt alle Strassenpunkte und prüft, ob sie in einem grünen Bereich liegen, wenn es so ist, wird der Punkt auf der Strasse einer Liste abgelegt.

    #Parameters:
    #    road_points (array<Shapely Point>) : Strassenpunkte
    #    land (array<Shapely Polygon>) : Bereiche als Polygon
    #    filename (string) : Name der zu speichernden Datei

    #Returns:
    #   filtered (array<shapely Point>) : Alle Strassen punkte die auf einem bestimmten Bereich liegen

    filtered = []
    features = []
    for p in road_points:
        for f in land:
            temp_intersection = p.intersection(f)
            if not temp_intersection.is_empty:
                if temp_intersection != Point(0, 0):
                    filtered.append(temp_intersection)

    filtered = cascaded_union(filtered)

    features.append(geojson.Feature(geometry=filtered))
    create_json(features, filename)

    return filtered


def generate_perimeter_with_land(circle):
    #Speichert Geodaten aus dem invertierten landcover Datensatz in einem bestimmten Kreis ab, der als Parameter mitgegeben wird.

    #Parameters:
    #    circle (Shapely Object) : Kreis

    #Returns:
    #   union (Shapely Multipolygon) : invertierte Landcover Daten, in einem bestimmten Kreis

    land_cover_list = []
    features = []

    with open('app/static/data/landcover_switzerland_invert.json') as lc:
        data = geojson.load(lc)
        multipoly = shape(geojson.MultiPolygon(data['features'][0]['geometry']['coordinates']))
        poly_list = list(multipoly)

        for poly in poly_list:
            temp_intersection = poly.intersection(circle)
            if not temp_intersection.is_empty:
                land_cover_list.append(temp_intersection)

    union = cascaded_union(land_cover_list)

    features.append(geojson.Feature(geometry=union))
    create_json(features, 'path_perimeter_land.json')
    return union


def merge_land_forest(land, forest):
    #Merge von Waldflächen und Nutzflächen

    #Parameters:
    #   land (Shapely Multipolygon) : invertierte Landcover Daten, in einem bestimmten Kreis
    #   forest (Shapely Multipolygon) : Landcover Daten, in einem bestimmten Kreis

    #Returns:
    #   union (list<Shapely Multipolygon>) : eine Liste von allen Shapely Objekten die aus Wälder und Nutzflächen

    features = []
    land_cover_list = [land, forest]

    union = cascaded_union(land_cover_list)

    features.append(geojson.Feature(geometry=union))
    create_json(features, 'land_forest_merge.json')
    return list(union)


def filter_trees(cities):
    # Filtern von Bäumen aus dem Trees Datensatz in der Stadt

    #Parameters:
    #   cities (list<Shapely Multipolygon>) : Siedlungen und Städte

    #Returns:
    #   tree_list (list<Shapely Point>) : eine Liste von Bäumen in den Bereichen von "cities"

    tree_list = []
    geo_tree_list = []
    features = []

    with open('app/static/data/single_trees.json') as lc:
        data = geojson.load(lc)
        for feature in data['features']:
            try:
                temp_point = shape(geojson.Point(feature['geometry']['coordinates']))
            except:
                continue
            if cities.contains(temp_point):
                tree_list.append(temp_point)
                geo_tree_list.append(geojson.Feature(geometry=temp_point))

    create_json(geo_tree_list, 'trees_in_cities.json')

    return tree_list


def find_green_city_waypoints(waypoints, trees):
    # identifikation von grünen Wegpunkten in der Stadt oder Siedlung

    #Parameters:
    #   waypoints (array<Shapely Point>) : Wegpunkte in der Stadt
    #   trees (list<Shapely Point>) : Bäume in der Stadt

    #Returns:
    #   waypoint_list (list<Shapely Point>) : eine Liste von Wegpunkten, die 5 oder mehr Bäume in der Umgebung haben.


    individual_points = [Point(pt.x, pt.y) for pt in waypoints]
    waypoint_list = []
    geo_waypoint_list = []

    for p in individual_points:
        counter = 0
        geojson_circle = Polygon(cg.geodesic_point_buffer(p.y, p.x, 15))
        for t in trees:
            print("1")
            if geojson_circle.contains(t):
                counter += 1
        if counter >= 5:
            waypoint_list.append(p)
            geo_waypoint_list.append(geojson.Feature(geometry=p))

    create_json(geo_waypoint_list, 'green_waypoints_city.json')

    return waypoint_list
