var map;

function initMap() {
    // Create a map object and specify the DOM element for display.
    console.log("initialise map");
    map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 51.5159, lng: -0.1297},
     	scrollwheel: false,
     	zoom: 12
    });
    // console.log(map);
}

$(document).ready(function(){
    console.log("document ready!");
    initMap();

    var marker = new google.maps.Marker({
	position: {lat: 51.5159, lng: -0.1297},
	map: map,
	title: 'Hello World!'
    });
});
