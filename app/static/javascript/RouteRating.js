let riseOfFastestRoute;
let slopeOfFastestRoute;


/**
 * Fordert eine Bewertung der Route vom Backend an, indem entsprechende Parameter übergeben werden.
 * @param {number} optimalRouteWaypoints - Die Wegpunkte der optimalen Route
 * @param {number} nicestRouteWaypoints - Die Wegpunkte der schönen Route
 * @param {number} durationOptimal - Die Dauer der optimalen Route
 * @param {number} durationNicest - Die Dauer der schönen Route
 * @param {number} distanceOptimal - Die Distanz der optimalen Route
 * @param {number} distanceNicest - Die Distanz der schönen Route
 * @param {number} riseOptimal - Die Steigung der optimalen Route
 * @param {number} riseNicest - Die Steigung der schönen Route
 * @param {number} slopeOptimal - Das Gefälle der optimalen Route
 * @param {number} slopeNicest - Das Gefälle der schönen Route
 * @return {number} Die Bewertung der übergebenen Route
 */
async function rateRoute(optimalRouteWaypoints, nicestRouteWaypoints, durationOptimal, durationNicest, distanceOptimal, distanceNicest, riseOptimal, riseNicest, slopeOptimal, slopeNicest) {
    let routeRating = 0;
    
    await $.post(RestURL + "rate",
    {
        optimal: JSON.stringify(optimalRouteWaypoints),
        nicest: JSON.stringify(nicestRouteWaypoints),
        durationOptimal: durationOptimal,
        durationNicest: durationNicest,
        distanceOptimal: distanceOptimal,
        distanceNicest: distanceNicest,
        riseOptimal: riseOptimal,
        riseNicest: riseNicest,
        slopeOptimal: slopeOptimal,
        slopeNicest: slopeNicest,
        maxUmweg: maxUmweg
    },
    function(data, status){
        routeRating = data;
    });

    return routeRating;
}

/**
 * Berechnet die Dauer der übergebenen Route
 * @param {RouteObject} route - Das Routen Objekt
 * @return {number} Die Dauer die für die Route benötigt wird (in Minuten)
 */
function calculateRouteDuration(route) {
    let duration = 0;
    for(i=0; i<route.length; i++) {
        let tmpDuration = [0, 0];
        let splitedText = route[i]["duration"]["text"].split(" ");
        
        if (splitedText[1] == "Minuten" || splitedText[1] == "Minute") {
            tmpDuration[1] = parseInt(splitedText[0], 10);
        } else {
            tmpDuration[0] = parseInt(splitedText[0], 10);
            tmpDuration[1] = parseInt(splitedText[2], 10);
        }

        duration += tmpDuration[0]*60 + tmpDuration[1];
    }

    return duration;
}

/**
 * Berechnet die Distanz der übergebenen Route
 * @param {RouteObject} route - Das Routen Objekt
 * @return {number} Die Distanz der Route (in km)
 */
function calculateRouteDistance(route) {
    let distance = 0.0;
    for(i=0; i<route.length; i++) {
        let tmpDistance = parseFloat(route[i]["distance"]["text"]);
        let unit = route[i]["distance"]["text"].split(" ")[1];

        if(unit == "m")
            tmpDistance = tmpDistance / 1000;

        distance += tmpDistance;
    }

    distance = Math.round((distance + Number.EPSILON) * 100) / 100

    return distance;
}

/**
 * Berechnet die Steigung und das Gefälle der schönen Route
 * @param {RouteObject} routeResults - Das Routen Objekt
 * @param {OrderedLegsObject} orderedLegs - Die einzelnen Teilabschnitte einer Route in sortierter Reihenfolge
 * @param {Overview_pathObject} overview_path - Die Wegpunkte einer Route in sortierter Reihenfolge
 */
function calcElevationNicestRoute(routeResults, orderedLegs, overview_path) {
    let pathValues = [];
    let route = orderedLegs;

    for(i=0; i<route.length; i++) {
        let steps = route[i]["steps"];

        for(j=0; j<steps.length; j++) {
            let startLocation = steps[j]["start_location"];
            let endLocation = steps[j]["end_location"];

            pathValues.push(startLocation);
            pathValues.push(endLocation);
        }
    }

    let rise = 0;
    let slope = 0;

    let elevator = new google.maps.ElevationService;
    elevator.getElevationForLocations({
        'locations': pathValues
    }, function(results, status) {
        if (status == 'OK') {

            for(i=1; i<results.length; i++) {
                difference = results[i]["elevation"] - results[i-1]["elevation"];

                if(difference < 0) {
                    slope += -(difference);
                } else {
                    rise += difference;
                }
            }
        } else {
            console.log("An Error occured in getElevation! Error is: "+status);
        }

        collectRoutes(routeResults, orderedLegs, overview_path, rise, slope);
    });
}

/**
 * Berechnet die Steigung und das Gefälle der optimalen Route
 * @param {RouteObject} routeResults - Das Routen Objekt
 */
function calcElevationOptimalRoute(routeResults) {
    let pathValues = [];
    let route = routeResults["routes"][0]["legs"];

    for(i=0; i<route.length; i++) {
        let steps = route[i]["steps"];

        for(j=0; j<steps.length; j++) {
            let startLocation = steps[j]["start_location"];
            let endLocation = steps[j]["end_location"];

            pathValues.push(startLocation);
            pathValues.push(endLocation);
        }
    }

    let rise = 0;
    let slope = 0;

    let elevator = new google.maps.ElevationService;
    elevator.getElevationForLocations({
        'locations': pathValues
    }, function(results, status) {
        if (status == 'OK') {
            for(i=1; i<results.length; i++) {
                difference = results[i]["elevation"] - results[i-1]["elevation"];

                if(difference < 0) {
                    slope += -(difference);
                } else {
                    rise += difference;
                }
            }

            document.getElementById('lblValueSlopeOptimalRoute').innerHTML = (Math.round((slope + Number.EPSILON) * 100) / 100)  + " m";
            document.getElementById('lblValueRiseOptimalRoute').innerHTML = (Math.round((rise + Number.EPSILON) * 100) / 100) + " m";

            riseOfFastestRoute = rise;
            slopeOfFastestRoute = slope;
        }
    });
}