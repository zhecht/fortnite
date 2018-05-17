
var heading_width = 20; //20 px wide for numbers/letters
var px_per_box = (850 - (heading_width * 2)) / 10;
var first_radius = 256;
var first_storm_time = 320; //3 min
var px_per_sec = px_per_box / 45;
var starting_loc_chosen = false;
var starting_x, starting_y;

function formatSpeed(seconds) {
	var min = parseInt(seconds / 60);
	var out_str = "";
	if (min !== 0) {
		out_str += (min+"m ");
	}
	seconds -= (min * 60);
	out_str += (seconds+"s");
	return out_str + seconds + 's';
}

function dist(x1,y1,x2,y2) {
	return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}

function findPointOnLine(x0,y0,x1,y1,dist) {
	//find point from (x0,y0) -> (x1,y1) w/ dist
	//Vector from starting to circle, subtract

	Vec_x = x1 - x0;
	Vec_y = y1 - y0;
	//Vector Length
	Vec_len = Math.sqrt(Vec_x * Vec_x + Vec_y * Vec_y);
	//calc unit vector
	Vec_x /= Vec_len;
	Vec_y /= Vec_len;
	//multiply by our distance
	Vec_x *= dist;
	Vec_y *= dist;
	//add vector to point A
	P_x = x0 + Vec_x;
	P_y = y0 + Vec_y;
	return [P_x, P_y];

}

function SVG(tag) {
	return document.createElementNS('http://www.w3.org/2000/svg', tag);
}

var drawCircle = function(x,y) {
	var $svg = $("svg");
	$(SVG('circle'))
		.attr('class', 'time_circles')
		.attr('cx', x)
		.attr('cy', y)
		.attr('r', 3)
		.attr('fill', "white")
		.appendTo($svg);
};

var drawLine = function(x1,y1,x2,y2) {
	x1 += 11; y1 += 11; x2 += 11; y2 += 11;
	var $svg = $("svg");
	$(SVG('line'))
		.attr('class', 'route_line')
		.attr('stroke', 'red')
		.attr('stroke-width', '3')
		.attr('x1', x1)
		.attr('y1', y1)
		.attr('x2', x2)
		.attr('y2', y2)		
		.appendTo($svg);	
}


function mapStartingClosest(x1,y1,h,k,r) {
	var Vx = x1 - h, Vy = y1 - k;
	var magV = Math.sqrt(Vx * Vx + Vy * Vy);
	var Ax = h + Vx / magV * r;
	var Ay = k + Vy / magV * r;
	return [Ax,Ay];
}

function mapClosest(x1,y1,h,k,r) {
	var Vx = x1 - h, Vy = y1 - k;
	var magV = Math.sqrt(Vx * Vx + Vy * Vy);
	var Ax = h + Vx / magV * r;
	var Ay = k + Vy / magV * r;

	var edge_dist = dist(x1, y1, Ax, Ay);
	var storm_velocity = edge_dist / first_storm_time;
	var outrun_dist = 0;

	//loop from 380s -> 0s to find a time where we can outrun
	for(var i = parseInt(edge_dist); i > 0; --i) {
		var storm_time_to_circle = i / storm_velocity;
		var player_time_to_circle = i / px_per_sec;

		if (player_time_to_circle < storm_time_to_circle) {
			//we can outrun the storm
			outrun_dist = i;
			break;
		}
	}

	//var coords = findPointOnLine(Ax,Ay,x1,y1,outrun_dist);
	//drawCircle(coords[0],coords[1]);

	var time_intervals = [30,60,90];
	for (var i = 0; i < time_intervals.length; ++i) {
		var d = storm_velocity * (first_storm_time - time_intervals[i]);
		var coords = findPointOnLine(x1,y1,Ax,Ay,d);
		drawCircle(coords[0],coords[1]);
	}
	return [Ax,Ay];
}


function mapClosestBackup(x1,y1,h,k,r) {
	var Vx = x1 - h, Vy = y1 - k;
	var magV = Math.sqrt(Vx * Vx + Vy * Vy);
	var Ax = h + Vx / magV * r;
	var Ay = k + Vy / magV * r;
	
	//find y-intercept. y = mx + b
	var slope = (Ay - y1) / (Ax - x1);
	var b = Ay - (Ax * slope);

	//var y_intercept = slope * 20 + b;
	//var edge_x = 20, edge_y = y_intercept;
	var edge_dist = dist(x1, y1, Ax, Ay);
	var storm_dist_per_second = edge_dist / first_storm_time;	

	var distances = [15,30,60];
	for (var i = 0; i < distances.length; ++i) {
		var d = storm_dist_per_second * distances[i];
		var coords = findPointOnLine(Ax,Ay,x1,y1,d);
		drawCircle(coords[0],coords[1]);
		//$("#svg").append("<circle cx="+coords[0]+" cy="+coords[1]+" r='4' fill='white' ></circle>");
	}
	return [Ax,Ay];
}




$("#content").click(function(e){

	var x = $(window)[0].scrollX + e.clientX;
	var y = $(window)[0].scrollY + e.clientY;

	if (starting_loc_chosen) {
		x = 650, y = 480;

		$(".time_circles,.route_line").remove();
		$("#first_circle").attr({"cx": x, "cy": y}).show();
		
		var coords = mapStartingClosest(starting_x, starting_y, x, y, first_radius);
		var Ax = coords[0], Ay = coords[1];
		$("#shortest_loc").attr({"cx": Ax, "cy": Ay}).show();
		$("#shortest_line").attr({
			"x1": starting_x, "y1": starting_y,
			"x2": Ax, "y2": Ay
		});

		
		//getPathData(starting_x,starting_y,x,y);

		//var max = 830;
		var max = 100;
		for (var i = 20; i < max; i += 20) {
			mapClosest(i, 20, x, y, first_radius);
			mapClosest(20, i, x, y, first_radius);
			mapClosest(max, i, x, y, first_radius);
			mapClosest(i, max, x, y, first_radius);
		}
		
	} else {
		x = 645, y = 110;
		$("#starting_loc").attr({"cx": x, "cy": y}).show();
		starting_x = x, starting_y = y;
		starting_loc_chosen = true;
	}
});

$(document).ready(function() {
	$.ajax({
		url: "/find_location_and_path",
		success: function(data) {
			//console.log(data);
			var prev_coord = [data[0]["starting_x"],data[0]["starting_y"]];
			for (var i = 1; i < data.length; ++i) {
				var chest_data = data[i];
				var chest_coord = [chest_data["x"],chest_data["y"]];
				drawLine(prev_coord[0],prev_coord[1],chest_coord[0],chest_coord[1]);
				prev_coord = chest_coord;
			}
		}
	});
});


function getPathData(starting_x,starting_y,circle_x,circle_y) {
	$.ajax({
		url: "/find_path",
		data: {
			starting_x: starting_x,
			starting_y: starting_y,
			circle_r: first_radius,
			circle_x: circle_x,
			circle_y: circle_y,
			time_left: first_storm_time
		},
		success: function(data) {
			//console.log(data);
			var prev_coord = [starting_x,starting_y];
			for (var i = 0; i < data.length; ++i) {
				var chest_data = data[i];
				var chest_coord = [chest_data["x"],chest_data["y"]];
				drawLine(prev_coord[0],prev_coord[1],chest_coord[0],chest_coord[1]);
				prev_coord = chest_coord;
			}
		}
	});
}