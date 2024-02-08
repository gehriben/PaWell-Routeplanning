import shapely
import geojson
from shapely.geometry.point import Point
from functools import partial
import pyproj
from shapely.ops import cascaded_union, transform

proj_wgs84 = pyproj.Proj(init='epsg:4326')

def route_circle(route_waypoints, circle_buffer):
    #Erstellt für alle mitgegebenen Wegpunkten Shapely Polygon Objekte in Form von Kreisen.

    #Parameters:
    #    route_waypoints (array) : Die Wegpunkte der Route
    #    circle_buffer (int): Grösse eines kreises in Kilometer

    #Returns:
    #    circles (arrray): Eine Liste von Shapely Polygon Objekte in Form von Kreisen.

    route_features = []
    circles = []

    for i in range(len(route_waypoints)):
        temp_center = Point(route_waypoints[i]['lng'], route_waypoints[i]['lat'])
        geojson_circle = shapely.geometry.mapping(create_circle(temp_center, circle_buffer))
        circles.append(geojson_circle)
        route_features.append(geojson.Feature(geometry=geojson_circle))

    feature_collection = geojson.FeatureCollection(route_features)

    content = geojson.dumps(feature_collection)
    f = open('app/static/data/created/route_circle.json', 'w+')
    f.write(content)
    return circles


def create_circle(point, circle_buffer):
    #Erstellt für einen Shapely Point Objekt ein Shapely Polygon Objekt in Form eines Kreises

    #Parameters:
    #    point (Shapely Point): Punkt, an dem der Kreis erstellt werden soll
    #    circle_buffer (int): Grösse eines Kreises in Kilometer+

    #Returns:
    #    circle (Shapely Polygon): Ein Kreis

    temp_circle = point.buffer(circle_buffer)
    circle = shapely.geometry.mapping(temp_circle)

    return circle


def geodesic_point_buffer(lat, lon, meter):
    # Azimuthal equidistant projection
    # Erstellt für einen Shapely Point Objekt ein Shapely Polygon Objekt in Form eines Kreises
    # Der kreis wird durch azimutale äquidistante Projektion der Erdoberfläche angepasst

    #Parameters:
    #    lat (int): Breitengrad des Koordinatenpunktes
    #    lon (int): Längengrad des Koordinatenpunktes
    #    meter (int): Grösse des Kreises in meter
    #Returns:
    #    circle (Shapely Polygon): Ein Kreis, der nach Azimuthal Projektion die Erde Reflektiert

    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(meter)  # distance in metres
    return_obj = transform(project, buf).exterior.coords[:]
    return return_obj