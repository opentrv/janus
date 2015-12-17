var map;

function initMap() {
    // Create a map object and specify the DOM element for display.
    console.log("initialise map");
    map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 51.5159, lng: -0.1297},
     	scrollwheel: false,
     	zoom: 12
    });
}


$(document).ready(function(){
    console.log("document ready!");
    initMap();

    var busStops;
    var markers = [];
    $.get('/dataserver/api/tfl/data/bus-stops', function(data, status){
	busStops = data.content;
	for(i in busStops){
	    var marker = new google.maps.Marker({
		position: {lat: busStops[i].latitude, lng: busStops[i].longitude},
		map: map,
		title: busStops[i].name,
		class: 'bus-stop'
	    });

	    marker.addListener('click', function(){
		console.log(this.title);
		console.log(this.position.lat());
		console.log(this.position.lng());
	    });
	}

    });

    
});
