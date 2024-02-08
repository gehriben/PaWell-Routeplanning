let map;
let directionsService;
let geocodingService
let directionsRenderer = [];

const RestURL = 'http://127.0.0.1:5000/'
const apiKey = 'AIzaSyBXffDrv5b4RWmyFylQzwoumN5VpHwPpEU';

/**
 * Stellt eine Karte durch den API Dienst von Google dar.
 */
function initGoogleMap() {
  var polylineOptionsActual = new google.maps.Polyline({
    strokeColor: '#FF0000'
  });

  directionsService = new google.maps.DirectionsService();
  geocodingService = new google.maps.Geocoder();

  directionsRenderer[0] = new google.maps.DirectionsRenderer({polylineOptions: polylineOptionsActual});
  directionsRenderer[1] = new google.maps.DirectionsRenderer();
  directionsRenderer[2] = new google.maps.DirectionsRenderer();
  directionsRenderer[3] = new google.maps.DirectionsRenderer();
  directionsRenderer[4] = new google.maps.DirectionsRenderer();
  directionsRenderer[5] = new google.maps.DirectionsRenderer();


  let winterthur = new google.maps.LatLng(47.502197, 8.725780);

  map = new google.maps.Map(document.getElementById('map'), {
      center: winterthur,
      zoom: 15
  });

  directionsRenderer[0].setMap(map);
  directionsRenderer[1].setMap(map);
  directionsRenderer[2].setMap(map);
  directionsRenderer[3].setMap(map);
  directionsRenderer[4].setMap(map);
  directionsRenderer[5].setMap(map);
}


/**
 * Implementiert die Funktionalität des Sliders
 */
function sliderChange() {
  var slider = document.getElementById("slBerechnungszeit");
  if (slider.value == 1) {
    document.getElementById('lblBerechnungszeit').innerHTML = "Kurz";
    document.getElementById('lblBerechnungszeit').style.color = "#2ecc71";

    document.getElementById('lblResult').innerHTML = "Minimal";
    document.getElementById('lblResult').style.color = "#b94141";

    document.getElementById('txtMaxUmweg').value = "";
    document.getElementById('txtMaxUmweg').disabled = true;
  } else if (slider.value == 2) {
    document.getElementById('lblBerechnungszeit').innerHTML = "Mittel";
    document.getElementById('lblBerechnungszeit').style.color = "#fcba03";

    document.getElementById('lblResult').innerHTML = "Mittelmässig";
    document.getElementById('lblResult').style.color = "#fcba03";

    document.getElementById('txtMaxUmweg').disabled = false;
  } else if (slider.value == 3) {
    document.getElementById('lblBerechnungszeit').innerHTML = "Hoch";
    document.getElementById('lblBerechnungszeit').style.color = "#b94141";

    document.getElementById('lblResult').innerHTML = "Gut";
    document.getElementById('lblResult').style.color = "#2ecc71";

    document.getElementById('txtMaxUmweg').disabled = false;
  }
}