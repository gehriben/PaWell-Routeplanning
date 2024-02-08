let starCoordinate;
let endCoordinate;

/**
 * Lädt die Geodaten für die Bäume
 */
function loadGeoData(){
    start_Location = document.getElementById('txtStart').value;
    end_Location = document.getElementById('txtEnd').value;


        geocodingService.geocode({'address': start_Location}, function(results, status) {
          if (status === 'OK') {
            starCoordinate = results[0].geometry.location;
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

        geocodingService.geocode({'address': end_Location}, function(results, status) {
          if (status === 'OK') {
            endCoordinate = results[0].geometry.location;
            findPerimeter(starCoordinate, endCoordinate);
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

}

/**
 * Start den Algorithmus zur Eingrenzung der Daten
 */
function fastestRouteEnabler(waypoints, route){
    $.ajax({
        type: "POST",
        url: RestURL + "perimeter",
        data: JSON.stringify(waypoints),
          async: true,
          success: function(data) {
            displayOptimalRoute(route);
          }
    });
}