var timer_id;

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

function populateTable(measurements, measurement_types){
    console.log("populateTable");
    console.log("measurement_types: " + measurement_types);
    console.log(measurements);
    var table = $("#data-table");
    table.empty();
    headers_tag = "<thead><tr><th>Datetime</th>"
    // headers_tag = "<tr style=\"position: absolute;\"><th>Datetime</th>"
    for(var i in measurement_types){
	headers_tag += "<th>" + measurement_types[i] + "</th>";
    }
    headers_tag += "</tr></thead>"
    table.append(headers_tag);
    // group measurements by datetime
    measurement_dates = {}
    for(var i in measurements){
	var measurement = measurements[i];
	if(!(measurement.datetime in measurement_dates)){
	    measurement_dates[measurement.datetime] = [measurement];
	} else {
	    measurement_dates[measurement.datetime].push(measurement);
	}
    }

    for(var i in measurement_dates){
	var row_tag = "<tr><td>" + i + "</td>";
	for(var j in measurement_types){
	    var column_tag = "<td></td>"
	    for(var k in measurement_dates[i]){
		if(measurement_dates[i][k].type == measurement_types[j]){
		    column_tag = "<td>" + measurement_dates[i][k].value + "</td>";
		    break;
		}
	    }
	    row_tag += column_tag;
	}
	row_tag += "</tr>";
	table.append(row_tag);
    }
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

    $("#live-graph-button").click(function(e){
	$(this).toggleClass("down-button");
	if($(this).hasClass("down-button")){
	    timer_id = startTimer(10000);
	} else {
	    console.log("clearInterval: " + timer_id);
	    clearInterval(timer_id);
	}	    
    });
    
    dataFilterSection.find("form").submit(function(e){
    	console.log("form submission");
	e.preventDefault();
	var table = $("#data-table");
	table.empty();
	$("#graph").empty();
	$("#quantity-selector").empty();
	$("#filter-warnings").css("color", "black");
	$("#filter-warnings").text("loading");
	var datetimeFirst = dataFilterForm.find("#datetime-first-input").val();
	var datetimeLast = dataFilterForm.find("#datetime-last-input").val();
	var sensorId = dataFilterForm.find("#sensor-id-input option:selected").text()
	var x = $.get("/dataserver/api/opentrv/data", {
	    "datetime-first": datetimeFirst,
	    "datetime-last": datetimeLast,
	    "sensor-id": sensorId,
	}).done(function(response){
	    data = response.content;
	    if(data.length){
		
		// get the quantities
		var measurement_types = getMeasurementTypes(data)

		populateTable(data, measurement_types);
		
		for(var i in measurement_types){
		    var option_tag = "<option value=\"" + measurement_types[i] + "\">";
		    option_tag += measurement_types[i];
		    option_tag += "</option>";
		    $("#quantity-selector").append(option_tag);
		}
		$("#quantity-selector").change();
		$("#filter-warnings").text("");
	    } else {
		$("#filter-warnings").css("color", "red");
		$("#filter-warnings").text("No data found. Try adjusting the date filters.");
		$.get("/dataserver/api/opentrv/data/dates?sensor-id=" + sensorId, function(response){
		    if(response.status == 200){
			if(response.content.length == 2){
			    var first = response.content[0];
			    var last = response.content[1];
			    $("#filter-warnings").text($("#filter-warnings").text() + " Earliest found mesaurement for sensor " + sensorId + ": " + first + ", latest measurement: " + last);
			}
		    }
		});
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

    function getData(){
	console.log("getData");
	var datetimeFirst = dataFilterForm.find("#datetime-first-input").val();
	var datetimeLast = new Date().toISOString(); //dataFilterForm.find("#datetime-last-input").val();
	var sensorId = dataFilterForm.find("#sensor-id-input option:selected").text()
	console.log(datetimeLast);
	var x = $.get("/dataserver/api/opentrv/data", {
	    "datetime-first": datetimeFirst,
	    "datetime-last": datetimeLast,
	    "sensor-id": sensorId,
	}).done(function(response){
	    
	    data = response.content;

	    console.log("response:");
	    console.log(response);
	    console.log("data:");
	    console.log(data);
	    
	    if(data.length){
		// get the quantities
		var measurement_types = getMeasurementTypes(data)
		
		populateTable(data, measurement_types);
		
		// for(var i in measurement_types){
		// 	var option_tag = "<option value=\"" + measurement_types[i] + "\">";
		// 	option_tag += measurement_types[i];
		// 	option_tag += "</option>";
		// 	$("#quantity-selector").append(option_tag);
		// }
		$("#quantity-selector").change();
	    } else {
	    }
	});
    }
    
    function startTimer(interval){
	console.log("startTimer: interval: " + interval);
	return setInterval(getData, interval);
    }

    // $.get("/dataserver/api/opentrv/data/sensor-ids", function(response){
    // 	var sensors = response.content;
    // 	for(var i in sensors){
    // 	    var option_tag = "<option value=\"" + sensors[i] + "\">" + sensors[i] + "</option>"
    // 	    $("#sensor-id-input").append(option_tag);
    // 	}
    // 	$("#data-filter-section form").submit()
    // 	// $("#property-selection-section button").first().click();
    // });

    $("#datetime-first-input").on("change", function(){
	console.log("datetime-first-input changed");
	console.log("new val: " + $(this).val());
	updateSensors($(this).val(), $("#datetime-last-input").val());
    });

    $("#datetime-last-input").on("change", function(){
	console.log("datetime-last-input changed");
	console.log("new val: " + $(this).val());
	updateSensors($("#datetime-first-input").val(), $(this).val());
    });

    function updateSensors(datetimeFirst, datetimeLast){
	var selectedSensor = $("#sensor-id-input").val();
	console.log("datetimeFirst: " + datetimeFirst);
	console.log("datetimeLast: " + datetimeLast);
	console.log("selectedSensor: " + selectedSensor);
	$.get("/dataserver/api/opentrv/data/sensor-ids", {'datetime-first': datetimeFirst, 'datetime-last': datetimeLast})
	    .done(function(response){
		var sensors = response.content;
		console.log("sensors: " + response.content);
		$("#sensor-id-input").empty();
		for(var i in sensors){
		    var optionTag = $("<option value=\"" + sensors[i] + "\">" + sensors[i] + "</option>");
		    if(sensors[i] == selectedSensor || i == 0){
			optionTag.prop("selected", true);
		    }
		    $("#sensor-id-input").append(optionTag);
		}
	    });
    }
    
    $("#datetime-first-input").change();
    
});

