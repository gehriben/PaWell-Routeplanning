const maxWaypointsPossibleFromAPI = 25;

/**
 * Generiert aus allen Koordinaten Wegpunkte und speichert sie in Route Arrays (max. 25 Wegpunkte pro Array)
 * @param {Coordinates} snappedCoordinates - Array mit allen Koordinaten der neuen Route
 * @return {Waypoints} Array mit Routen Arrays die max. 25 Wegpunkte enthalten
 */
function collectWaypointsOfRoutes(snappedCoordinates) {
    let waypoints = [];
    let routes = [];
    allPossibleWaypointsOfRoute = [];

    routeAmount = snappedCoordinates.length / 25;
    routeAmount = Math.floor(routeAmount);

    routeIteration = 0;

    for(; routeIteration < routeAmount; routeIteration++) {
        let route = [];
        for(i=0; i<25; i++) {
            route.push(generateWaypoint(snappedCoordinates[(routeIteration*25)+i]));
        }

        routes.push(route);
    }

    let route = [];
    for(i=snappedCoordinates.length - (snappedCoordinates.length - routeAmount*25); i<snappedCoordinates.length; i++) {
        route.push(generateWaypoint(snappedCoordinates[i]))
    }
    routes.push(route);

    return routes;
}

/**
 * Erstellt aus einem Koordinatenpunkt einer Wegpunkte für eine Route
 * @param {Coordinates} coordinates - Koordinaten eines Routenpunktes
 * @return {Waypoint} Wegpunkt für eine Google Maps Route
 */
function generateWaypoint(coordinates) {
    return {
          location: coordinates,
          stopover: true
        }
}