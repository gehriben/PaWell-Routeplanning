import geojson
import json
import shapely
from shapely.geometry import shape, Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
from app import create_geojson
from app import circle_generator as cg

def ratePoints(waypointsOptimalRoute, waypointsNicestRoute, durationOptimal, durationNicest, distanceOptimal, distanceNicest, riseOptimal, riseNicest, slopeOptimal, slopeNicest, maxUmweg):
    #Bewertet die Route anhand verschiedener Parameter

    #Parameters:
    #    waypointsOptimalRoute (array):Die Wegpunkte der optimalen Route
    #    waypointsNicestRoute (array):Die Wegpunkte der schönen Route
    #    durationOptimal (number):Die Dauer der optimalen Route
    #    durationNicest (number):Die Dauer der schönen Route
    #    distanceOptimal (number):Die Distanz der optimalen Route
    #    distanceNicest (number):Die Distanz der schönen Route
    #    riseOptimal (number):Die Steigung der optimalen Route
    #    riseNicest (number):Die Steigung der schönen Route
    #    slopeOptimal (number):Das Gefälle der optimalen Route
    #    slopeNicest (number):Das Gefälle der schönen Route
    #    maxUmweg (number):Der angegebene, maximale Umweg des User

    #Returns:
    #    number:Rating der übergebenen Route
    
    amountOfIdenticalPoints = 0

    jsonWaypointsOptimalRoute = json.loads(waypointsOptimalRoute)
    jsonWaypointsNicestRoute = json.loads(waypointsNicestRoute)

    for optimalPoint in jsonWaypointsOptimalRoute:
        optimalPointObject = Point(optimalPoint['lng'], optimalPoint['lat'])
        for nicestPoint in jsonWaypointsNicestRoute:
            geojson_circle = shape(cg.create_circle(Point(nicestPoint['lng'], nicestPoint['lat']), 0.0001))

            if(geojson_circle.intersects(optimalPointObject)):
                amountOfIdenticalPoints += 1

    percentage_optimal_route, percentage_nicest_route = calculate_green_percentage(jsonWaypointsOptimalRoute, jsonWaypointsNicestRoute)

    IdenticalPointsRating = ((len(jsonWaypointsNicestRoute) - amountOfIdenticalPoints) / len(jsonWaypointsNicestRoute))*4
    green_points_rating = (percentage_nicest_route - percentage_optimal_route)*6

    if(float(maxUmweg) != 0 and float(maxUmweg) < float(distanceNicest) - float(distanceOptimal)): 
        create_geojson.increment_radius = False
        return 0
    else:
        distanceRating = (float(distanceOptimal) / float(distanceNicest))*2
        durationRating = (float(durationOptimal) / float(durationNicest))*2 

        riseRating = float(riseOptimal) / float(riseNicest)
        slopeRating = float(slopeOptimal)/ float(slopeNicest) 

        print("--------------------------")
        print("Es sind "+str(amountOfIdenticalPoints)+" Punkte identisch vom insgesamt "+str(len(jsonWaypointsNicestRoute))+"!")
        print("Unterschied in Distanz: " + str(float(distanceNicest) - float(distanceOptimal)))
        print("Unterschied in Dauer: " + str(float(durationNicest) - float(durationOptimal)))
        print("Unterschied in Steigung: " + str(float(riseNicest) - float(riseOptimal)))
        print("Unterschied in Gefälle: " + str(float(slopeNicest) - float(slopeOptimal)))
        print("Unterschied in Prozent: " + str((percentage_nicest_route - percentage_optimal_route)*100))

        rating = IdenticalPointsRating + green_points_rating + distanceRating + durationRating + ((riseRating + slopeRating) / 2) + 100
        print("RATING DER ROUTE: " + str(rating))

        return rating

def calculate_green_percentage(waypointsOptimalRoute, waypointsNicestRoute):
    with open('app/static/data/created/land_forest_merge.json') as lc:
        data = geojson.load(lc)
        multi_poly = shape(geojson.MultiPolygon(data['features'][0]['geometry']['coordinates'])).buffer(0)
        poly_list = list(multi_poly)

    amount_green_points_optimal_route = 0
    amount_green_points_nicest_route = 0

    for j in poly_list:
        for i in range(len(waypointsOptimalRoute)):
            point = Point(waypointsOptimalRoute[i]['lng'], waypointsOptimalRoute[i]['lat'])
            intersect = j.intersects(point)
            if(intersect):
                amount_green_points_optimal_route += 1

        for i in range(len(waypointsNicestRoute)):
            point = Point(waypointsNicestRoute[i]['lng'], waypointsNicestRoute[i]['lat'])
            intersect = j.intersects(point)
            if(intersect):
                amount_green_points_nicest_route += 1

    percentage_optimal_route = amount_green_points_optimal_route / len(waypointsOptimalRoute)
    percentage_nicest_route = amount_green_points_nicest_route / len(waypointsNicestRoute)

    return percentage_optimal_route, percentage_nicest_route
