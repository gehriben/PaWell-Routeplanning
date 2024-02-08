let optimalRouteObject
let waypointsOfFastestRoute;
let durationOfFastestRoute;
let distanceOfFastestRoute;

let startLocation;
let endLocation;
let startCoordinates;

let maxUmweg;
let popup;

let allPossibleWaypointsOfRoute = [];
let generatedRoutes = [];

var delayFactor = 0;

/**
 * Berechnet die optimale Route anhand der angegebenen Ortschaften
 */
function initCalculationOfFastestRoute() {
    resetSettingsOfFastestRoute();

    startLocation = document.getElementById('txtStart').value;
    endLocation = document.getElementById('txtEnd').value;

    var request = {
        origin: startLocation,
        destination: endLocation,
        provideRouteAlternatives: true,
        travelMode: 'WALKING'
    };

    directionsService.route(request, function(result, status) {
        if (status == 'OK') {
            popup = document.getElementById("loadingPopup");
            popup.style.display = "block";
            document.getElementById("lblLoadingScreen").innerHTML = "<strong>Die Route wird vorbereitet</strong>"

            fastestRouteEnabler(result["routes"][0]["overview_path"], result)
        } else if(status === google.maps.DirectionsStatus.NOT_FOUND) {
            alert("Keine Route gefunden! Bitte überprüfen Sie Ihre Angaben.");
        } else {
            alert("Es ist ein unerwarteter Fehler aufgetreten!");
        }
    });
}

/**
 * Initalisert die Berechnung der schönen Route im Backend
 */
function initCalculationOfNicestRoute(step) {
    if(step == 1) {
        resetSettingsOfNicestRoute();

        document.getElementById("lblLoadingScreen").innerHTML = "<strong>Die Route wird generiert... 0%</strong>"
        popup.style.display = "block";

        if(document.getElementById('txtMaxUmweg').value == "") {
            maxUmweg = 0;
        
        } else if (isNaN(document.getElementById('txtMaxUmweg').value)) {
            alert("Bitte geben Sie für den maximalen Umweg einen gültigen Wert ein.");
            return;
        } else {
            maxUmweg = document.getElementById('txtMaxUmweg').value;
        }
    }

    $.post(RestURL + "waypoint",
    {
        step: step,
        waypoints: JSON.stringify(waypointsOfFastestRoute)
    },
    function(data, status){
        processCalculatedPoints(data);
    });
}

/**
 * Wechselt die Darstellung wenn der User eine andere Route berechnen möchte
 */
function changeRoute() {
    document.getElementById('btnCalcNicestRoute').disabled = true;
    document.getElementById('txtStart').disabled = false;
    document.getElementById('txtEnd').disabled = false;
    document.getElementById("editBtn").style.visibility = "hidden";

    document.getElementById('txtStart').value = "";
    document.getElementById('txtEnd').value = "";
    document.getElementById('txtMaxUmweg').value = "";

    document.getElementById("slBerechnungszeit").value = 2;

    document.getElementById('lblValueDurationOptimalRoute').innerHTML = "0 Minuten";
    document.getElementById('lblValueDistanceOptimalRoute').innerHTML = "0 km";
    document.getElementById('lblValueSlopeOptimalRoute').innerHTML = " 0 m";
    document.getElementById('lblValueRiseOptimalRoute').innerHTML = " 0 m";

    document.getElementById('lblValueDurationNicestRoute').innerHTML = "0 Minuten";
    document.getElementById('lblValueDistanceNicestRoute').innerHTML = "0 km";
    document.getElementById('lblValueSlopeNicestRoute').innerHTML = " 0 m";
    document.getElementById('lblValueRiseNicestRoute').innerHTML = " 0 m";

    initGoogleMap();
}

/**
 * Setze globale Variablen zurück, welche die schnellste Route betreffen
 */
function resetSettingsOfFastestRoute() {
    waypointsOfFastestRoute = [];
    durationOfFastestRoute = null;
    distanceOfFastestRoute = null;
    startLocation = null;
    startCoordinates = [];
    endLocation = null
}

/**
 * Setze globale Variablen zurück, welche die schönste Route betreffen
 */
function resetSettingsOfNicestRoute() {
    maxUmweg = null;

    allPossibleWaypointsOfRoute = [];
    generatedRoutes = [];

    delayFactor = 0;

    initGoogleMap();
    directionsRenderer[0].setDirections(optimalRouteObject);
}