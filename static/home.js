function getKeys(object){
    var keys = []
    for(var key in object){
	keys.push(key);
    }
    return keys;
}

function getMeasurementTypes(measurements){
    var measurement_types_dict = {}
    for(var i in measurements){
	measurement_types_dict[measurements[i].type] = null;
    }
    return getKeys(measurement_types_dict);
}

$(document).ready(function(){
    
    var validQuantities = ["Temperature", "Humidity", "Light", "Occupancy", "Battery"]
    var propertyDetailsSection = $("#property-details-section");
    var dataSection = $("#data-section");
    var dataFilterSection = dataSection.find("#data-filter-section");
    var dataFilterForm = dataFilterSection.find("form");
    var dataTable = dataSection.find("table#data-table");
    var graphSection = dataSection.find("section#graph-section");
    var graph = graphSection.find("div#graph-div svg#graph");
    var graphQuantitySelector = graphSection.find("select#quantity-selector");

    var data = [];
    
    dataFilterSection.find("form").submit(function(e){
    	console.log("form submission");
	e.preventDefault();
	$("#quantity-selector").empty();
	var datetimeFirst = dataFilterForm.find("#datetime-first-input").val();
	var datetimeLast = dataFilterForm.find("#datetime-last-input").val();
	var sensorId = dataFilterForm.find("#sensor-id-input option:selected").text()
	var x = $.get("dataserver/api/opentrv/data", {
	    "datetime-first": datetimeFirst,
	    "datetime-last": datetimeLast,
	    "sensor-id": sensorId,
	}).done(function(response){
	    data = response.content;
	    if(data.length){
		// get the quantities
		var measurement_types = getMeasurementTypes(data)
		console.log(measurement_types.length);
		for(var i in measurement_types){
		    var option_tag = "<option value=\"" + measurement_types[i] + "\">";
		    option_tag += measurement_types[i];
		    option_tag += "</option>";
		    $("#quantity-selector").append(option_tag);
		}
		$("#quantity-selector").change();
	    }
	});

    });

    $("#quantity-selector").change(function(e){
	var type = $("#quantity-selector").val();
	var measurements = [];
	for(var i in data){
	    if(data[i].type == type){
		measurements.push({
		    'datetime': data[i].datetime,
		    'value': data[i].value
		});
	    }
	}
	loadGraph(measurements, type);
    });

    function loadGraph(measurements, type){
    	console.log("loadGraph");
	console.log("n_measurements: " + measurements.length);
	console.log(measurements);
	
    	var m = [20, 20, 30, 50],
    	    w = 960 - m[1] - m[3],
    	    h = 500 - m[0] - m[2];
	
    	var svg = d3.select("#graph")
	    .attr("width", w + m[1] + m[3])
	    .attr("height", h + m[0] + m[2]);
	svg.selectAll("*").remove();

	var g = svg.append("g");
	g.attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    	var minDate = d3.min(data, function(d){
    	    return d.datetime;
    	});
	
    	var maxDate = d3.max(data, function(d){
    	    return d.datetime;
    	});
	
    	console.log("minDate: " + minDate + ", maxDate: " + maxDate);

	console.log(maxDate);
	
    	if(minDate != undefined){
    	    var xscale = d3.time
		.scale()
		.range([0, w])
		.domain([new Date(minDate), new Date(maxDate)]);
		// .domain([new Date(minDate - 3600 * 1000), new Date(maxDate.getTime() + (3600 * 1000))]);
    	    var xaxis = d3.svg.axis();
    	    xaxis.orient('bottom');
    	    xaxis.scale(xscale);
    	    g.append("g").call(xaxis)
    		.attr("transform", "translate(0, " + h + ")")
    		.attr("class", "axis x-axis");
	    
    	    var minY = d3.min(measurements, function(d){ return d.value; });
    	    var maxY = d3.max(measurements, function(d){ return d.value; });
    	    console.log(minY);
    	    console.log(maxY);
	    
    	    var yscale = d3.scale.linear()
    		.range([h, 0])
    		.domain([minY - minY * 0.1, maxY + maxY * 0.1]);
    	    var yaxis = d3.svg.axis();
    	    yaxis.scale(yscale);
    	    yaxis.orient('left');
    	    g.append("g").call(yaxis)
    		.attr("class", "axis y-axis");
	    
    	    var line = d3.svg.line()
    	    	.x(function(d){ return xscale(new Date(d.datetime)); })
    	    	.y(function(d){ return yscale(d.value); })
	    
	    
    	    g.append("path")
    	    	.datum(measurements)
    	    	.attr("class", "line")
    	    	.attr("d", line);
	    
    	    console.log(svg);
    	} else {
    	}
    }

    $.get("dataserver/api/opentrv/data/sensor-ids", function(response){
	var sensors = response.content;
	console.log(sensors);
	for(var i in sensors){
	    var option_tag = "<option value=\"" + sensors[i] + "\">" + sensors[i] + "</option>"
	    $("#sensor-id-input").append(option_tag);
	}
	$("#data-filter-section form").submit()
	// $("#property-selection-section button").first().click();
    });
    
});

