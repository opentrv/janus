var map;
var currentInfoWindow;

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

function addBusStop(busStop, map){
    var marker = new google.maps.Marker({
	position: {lat: busStop.latitude, lng: busStop.longitude},
	map: map,
	title: busStop.name,
	class: "bus-stop"
    });

    info = "<p>" + busStop.name + "</p>"
    info += "<p>lat: " + busStop.latitude + "<br>"
    info += "lng: " + busStop.longitude + "<br>"
    // info += "occupancy: " + busStop.occupancy + "</p>"
    
    var infowindow = new google.maps.InfoWindow({
	content: info
    });
    
    marker.addListener('click', function() {
	if(currentInfoWindow !== undefined){
	    currentInfoWindow.close();
	}
	infowindow.open(map, marker);
	currentInfoWindow = infowindow;
    });

    return marker;
}

$(document).ready(function(){
    console.log("document ready!");
    initMap();

    $.get("/dataserver/api/tfl/data/bus-stops", function(response){
	if(response.status == 200){
	    var busStops = response.content;
	    for(var i in busStops){
		var busStop = busStops[i];
		var marker = addBusStop(busStop, map);
	    }
	}
    });


});
