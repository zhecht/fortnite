from flask import *
path = Blueprint('path', __name__, template_folder='views')


def findMin(arr):
	min_id = 0
	min_val = float("inf")
	for v in arr:
		if arr[v] < min_val:
			min_val = arr[v]
			min_id = v
	return min_id

def getNeighbors(chest_id):
	with open("static/neighbors/%s/neighbors.txt" % chest_id) as f:
		content = f.readlines()
	neighbor_arr = [x.strip() for x in content]
	all_neighbors = []

	for chest in neighbor_arr:
		neighbor_id,neighbor_dist = chest.split(",")
		all_neighbors.append({"id": neighbor_id, "dist": float(neighbor_dist)})
	return all_neighbors

def getAllChests():
	with open("static/chest_locations.txt") as f:
		content = f.readlines()
	chest_arr = [x.strip() for x in content]
	all_chests = []

	chest_num = 0
	for chest in chest_arr:
		coords = chest.split(",")
		all_chests.append({"x": int(coords[0]) - 11, "y": int(coords[1]) - 11, "id": chest_num})
		chest_num += 1
	return all_chests


def dijkstra(graph, source):
	vertex_set = set()
	dist = {}
	prev = {}

	for v in graph:
		dist[v["id"]] = float("inf")
		prev[v["id"]] = -1 #undefined
		vertex_set.add(v["id"])

	dist[source["id"]] = 0

	while len(vertex_set) > 0:
		min_id = findMin(dist)

		vertex_set.remove(min_id)
		neighbors = getNeighbors(min_id)

		for n in neighbors:
			alt = dist[min_index] + n["dist"]
			if alt < dist[n["id"]]:
				dist[v["id"]] = alt
				prev[v["id"]] = min_id
	return dist,prev


def dist(x0,y0,x1,y1):
	return pow(pow(x0 - x1, 2) + pow(y0 - y1, 2), .5)

def findClosestChest(coords,opened_chests,all_chests):
	closest_idx = 0
	min_d = 1000
	for i in range(0,len(all_chests)):
		chest = all_chests[i]
		d = dist(chest["x"],chest["y"],coords[0],coords[1])

		if chest["id"] not in opened_chests and d < min_d:
			closest_idx = i
			min_d = d

	return closest_idx,min_d

def findClosestPoint(x0,y0,h,k,r):
	Px = x0 - h
	Py = y0 - k
	Plen = pow(pow(Px,2) + pow(Py,2), .5)
	Px = h + Px / Plen * r
	Py = k + Py / Plen * r
	return dist(x0,y0,Px,Py)

def returnArray(opened_chests,all_chests):
	chest_arr = []

	for chest_num in opened_chests:
		chest_x = all_chests[chest_num]["x"]
		chest_y = all_chests[chest_num]["y"]
		chest_arr.append({"id": chest_num, "x": chest_x, "y": chest_y})

	return chest_arr

@path.route('/path',methods=["GET"])
def path_route():
	all_chests = getAllChests()

	px_per_box = 81
	time_remaining = 60 * 3
	px_per_sec = px_per_box / 45
	chest_open_time = 10

	curr_coords = [float(request.args["starting_x"]),float(request.args["starting_y"])]
	circle_radius = int(request.args["circle_r"])
	circle_x = float(request.args["circle_x"])
	circle_y = float(request.args["circle_y"])


	opened_chests = []

	while (time_remaining > 0):
		closest_chest,dist = findClosestChest(curr_coords,opened_chests,all_chests)
		chest_dist_to_circle = findClosestPoint(all_chests[closest_chest]["x"],all_chests[closest_chest]["y"],circle_x,circle_y,circle_radius)
		

		time_to_chest = dist / px_per_sec
		time_from_chest = chest_dist_to_circle / px_per_sec

		#print(closest_chest,chest_dist_to_circle,time_to_chest,time_from_chest,time_remaining)
		#if not enough time to open chest, return path
		if time_to_chest + time_from_chest > time_remaining:
			return jsonify(returnArray(opened_chests,all_chests))

		#add to opened, subtract time from remaining
		opened_chests.append(closest_chest)
		curr_coords[0] = all_chests[closest_chest]["x"]
		curr_coords[1] = all_chests[closest_chest]["y"]
		
		time_remaining -= (5 + time_to_chest)

	return jsonify(returnArray(opened_chests,all_chests))