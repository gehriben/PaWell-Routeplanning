/**
 * Fügt mehrere Routen zu einer Route zusammen
 * @param {Waypoints} routes - Alle Wegpunkte die zu einer Route zusammengefügt werden müssen
 */

function createRouteWithMultipleRoutes(routes) {
    let routeResults = [];
    directionsRendererCount = 0;
    for (i=0; i<routes.length; i++) {
        let start = "";
        let end = "";
        finished = false;

        if(i==0){
            start = startLocation;
        } else {
            start = routes[i-1][routes[i-1].length - 1]["location"];
        }

        if(i+1 == routes.length) {
            end = endLocation;
        } else {
            end = routes[i][routes[i].length - 1]["location"];
        }
  
        var request = {
            origin: start,
            destination: end,
            provideRouteAlternatives: true,
            optimizeWaypoints: true,
            waypoints: routes[i],
            travelMode: 'WALKING'
        };

        requestRouteFromAPI(request, routeResults, routes);
    }
}

/**
 * Die Google Maps API erlaubt nur 10 Requests hintereinander. Ab diesem Punkt ist ein Request nur jede Sekunde wieder erlaubt.
 * Diese Methode fängt dieses Problem ab und führt bei einem Fehler nur jede Sekunde wieder ein Request aus.
 * @param {DirectionsRequest} request - Der Request an die DirectionsAPI
 * @param {RouteObject} routeResults - Bereits berechnete Route
 * @param {Waypoints} routeResults - Das Array mit allen Wegpunkten
 */
function requestRouteFromAPI(request, routeResults, routes) {
    directionsService.route(request, function(result, status) {
        if (status == 'OK') {
            routeResults.push(result);
            if(routeResults.length == routes.length) {
                processRoutes(routeResults);
            }
        } else if (status === google.maps.DirectionsStatus.OVER_QUERY_LIMIT) {
            delayFactor++;
            setTimeout(function () {
                requestRouteFromAPI(request, routeResults, routes);
            }, delayFactor * 1000);
        }
    });
}

/**
 * Sortiert rekursiv die einzelnen Teilschritte der Route
 * @param {RouteObject} routeResults - Das Route Objekt mit der unsortierten Route
 * @param {RouteObject} orderedResult - Das Route Objekt mit der sortierten Route
 * @return {RouteObject} Gibt die sortierte Route als RouteObject zurück
 */
function orderLegs(routeResults, orderedResult) {
    let remainingResults = []



    for (i=0; i<routeResults.length; i++) {
        let unorderdLegs = routeResults[i]["routes"][0]["legs"];

        if(orderedResult.length == 0 && unorderdLegs[0]["start_location"].equals(startCoordinates)) {
            orderedResult.push(routeResults[i]);
        } else if(orderedResult.length != 0 && orderedResult[orderedResult.length-1]["routes"][0]["legs"][orderedResult[orderedResult.length-1]["routes"][0]["legs"].length-1]["end_address"] == unorderdLegs[0]["start_address"]) {
            orderedResult.push(routeResults[i]);
        } else {
            remainingResults.push(routeResults[i]);
        }
    }

    if(remainingResults.length != 0) {
        return orderLegs(remainingResults, orderedResult);
    } else {
        return orderedResult;
    }
}

/**
 * Sammelt mehrere Routen, bewertet diese und wählt anschliessend die beste aus
 * @param {RouteObject} routeResults - Das Route Objekt einer berechneten Route
 * @param {orderedLegsObject} orderedLegs - Die sortierten Teilschritte der Route
 * @param {overview_pathObject} overview_path - Die einzelnen Wegpunkte der Route
 * @param {number} routeRise - Die Steigung der Route
 * @param {number} routeSlope -  Das Gefälle der Route
 */
async function collectRoutes(routeResults, orderedLegs, overview_path, routeRise, routeSlope) {
    let slBerechnungszeit = document.getElementById("slBerechnungszeit");
    let maxSteps;

    if(slBerechnungszeit.value == 1) {
        maxSteps = 1;
    } else if (slBerechnungszeit.value == 2) {
        maxSteps = 5;
    } else if (slBerechnungszeit.value == 3) {
        maxSteps = 10;
    }

    
    let routeDuration = calculateRouteDuration(orderedLegs);
    let routeDistance = calculateRouteDistance(orderedLegs);

    let routeRating = await rateRoute(waypointsOfFastestRoute, overview_path, durationOfFastestRoute, routeDuration, distanceOfFastestRoute, routeDistance, riseOfFastestRoute, routeRise, slopeOfFastestRoute, routeSlope,);
    let routeProperties = []
    routeProperties.push(routeRating);
    routeProperties.push(routeResults);
    routeProperties.push(orderedLegs);
    routeProperties.push(routeDuration);
    routeProperties.push(routeDistance);
    routeProperties.push(routeRise);
    routeProperties.push(routeSlope);
    routeProperties.push(generatedRoutes.length+1);

    generatedRoutes.push(routeProperties);

    document.getElementById("lblLoadingScreen").innerHTML = "<strong>Die Route wird generiert... "+(generatedRoutes.length/maxSteps*100)+"%</strong>"

    if(generatedRoutes.length < maxSteps) {
        initCalculationOfNicestRoute(generatedRoutes.length+1);
    } else {
        let highestRating = 0;
        let index = 0;
        for(i=0; i<generatedRoutes.length; i++) {
            if(generatedRoutes[i][0] > highestRating) {
                highestRating = generatedRoutes[i][0];
                index = i;
            }
        }

        console.log("It was step "+generatedRoutes[index][7]+" with rating "+generatedRoutes[index][0]);
        displayNicestRoute(generatedRoutes[index][1], generatedRoutes[index][3], generatedRoutes[index][4], generatedRoutes[index][5], generatedRoutes[index][6], generatedRoutes[index][2]); 
    }
}