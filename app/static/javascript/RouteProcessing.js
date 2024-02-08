/**
 * Erhält eine berechnete Route sortiert die Teilrouten und entfernt falls nötig die Sackgassen.
 * @param {RouteObject} routeResults - Das Routen Objekt
 */
function processRoutes(routeResults) {
    orderedResults = orderLegs(routeResults, []);
    let orderedLegs = [];
    let overview_path = [];

    for(i=0; i<orderedResults.length; i++) {
        orderedLegs = orderedLegs.concat(orderedResults[i]["routes"][0]["legs"]);
        overview_path = overview_path.concat(orderedResults[i]["routes"][0]["overview_path"]);
    }

    $.ajax({
        type: "POST",
        url: RestURL + "route",
        data: JSON.stringify(orderedLegs),
          async: false,
          success: async function(data) {  
            if(data != "finished") {
                processDeletedDeadEndsRoute(data);
            }
            else {
                calcElevationNicestRoute(routeResults, orderedLegs, overview_path);
            }
          }
    });
}

/**
 * Erhält Koordinatenpunkte für die schöne Route vom Backend und erstellt Wegpunkte daraus.
 * @param {Coordinates} pointsData - Koordinatenpunkte 
 */
async function processCalculatedPoints(pointsData) {
    let points = [];
    for(i=0; i<pointsData.length; i++) {
        let point = new google.maps.LatLng(pointsData[i][1], pointsData[i][0]);
        points.push(point);
    }

    let routes = collectWaypointsOfRoutes(points);
    createRouteWithMultipleRoutes(routes);
}

/**
 * Erhält vom Backend Koordinatenpunkte die keine Sackgassen mehr enthalten und generiert Wegpunkte daraus.
 * @param {Coordinates} route - Koordinatenpunkte ohne Sackgassen
 */
function processDeletedDeadEndsRoute(route) {
    let points = [];
    for(i=1; i<route.length; i++) {
        let point = new google.maps.LatLng(route[i][0], route[i][1]);
        points.push(point);
    }

    allPossibleWaypointsOfRoute.forEach(element => points.push(element));

    let routes = collectWaypointsOfRoutes(points);
    createRouteWithMultipleRoutes(routes);
}