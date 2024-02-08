/**
 * Zeigt die optimale Route auf der Karte an, mit dessen Eigenschaften
 * @param {RouteObject} optimalRoute - Das Routen Objekt der optimalen Route
 */
function displayOptimalRoute(optimalRoute) {
    document.getElementById('btnCalcNicestRoute').disabled = false;
    document.getElementById('txtStart').disabled = true;
    document.getElementById('txtEnd').disabled = true;
    document.getElementById("editBtn").style.visibility = "visible";
    popup.style.display = "none";

    durationOfFastestRoute = calculateRouteDuration(optimalRoute["routes"][0]["legs"]);
    distanceOfFastestRoute = calculateRouteDistance(optimalRoute["routes"][0]["legs"]);
    document.getElementById('lblValueDurationOptimalRoute').innerHTML = durationOfFastestRoute.toString(10) + " Minuten";
    document.getElementById('lblValueDistanceOptimalRoute').innerHTML = distanceOfFastestRoute.toString(10) + " km";

    optimalRouteObject = optimalRoute;
    waypointsOfFastestRoute = optimalRoute["routes"][0]["overview_path"];
    startCoordinates = optimalRoute["routes"][0]["legs"][0]["start_location"];

    directionsRenderer[0].setDirections(optimalRoute);
    calcElevationOptimalRoute(optimalRoute);
}

/**
 * Zeigt die schöne Route auf der Karte an, mit dessen Eigenschaften
 * @param {RouteObject} route - Das Routen Objekt der schönen Route
 * @param {number} routeDuration - Die Dauer der schönen Route
 * @param {number} routeDistance - Die Distanz der schönen Route
 * @param {number} routeRise - Die Steigung der schönen Route
 * @param {number} routeSlope - Das Gefälle der schönen Route
 */
function displayNicestRoute(route, routeDuration, routeDistance, routeRise, routeSlope) {
    document.getElementById('lblValueDurationNicestRoute').innerHTML = routeDuration.toString(10) + " Minuten";
    document.getElementById('lblValueDistanceNicestRoute').innerHTML = routeDistance.toString(10) + " km";
    document.getElementById('lblValueSlopeNicestRoute').innerHTML = (Math.round((routeSlope + Number.EPSILON) * 100) / 100)  + " m";
    document.getElementById('lblValueRiseNicestRoute').innerHTML = (Math.round((routeRise + Number.EPSILON) * 100) / 100) + " m";

    popup.style.display = "none";

    for(i=1; i<=route.length; i++) {
        directionsRenderer[i].setDirections(route[i-1]);
    }
}