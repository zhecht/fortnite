from flask import *
import operator

find_path = Blueprint('find_path', __name__, template_folder='views')

px_per_box = 81
time_left = 380
px_per_sec = px_per_box / 45
chest_open_time = 5

def getNeighbors(chest_id,chests):
	with open("static/neighbors/%s/neighbors.txt" % chest_id) as f:
		content = f.readlines()
	neighbor_arr = [x.strip() for x in content]
	all_neighbors = []

	for chest in neighbor_arr:
		neighbor_id,neighbor_x,neighbor_y,neighbor_dist = chest.split(",")
		if int(neighbor_id) in chests:
			all_neighbors.append({"id": int(neighbor_id),  "x": float(neighbor_x), "y": float(neighbor_y),"dist": float(neighbor_dist)})
	return all_neighbors

def getStartingNeighbors(all_chests,source):
	x_loc = source["x"]
	y_loc = source["y"]

	all_neighbors = []
	for neighbor in all_chests:
		d = dist(neighbor["x"],neighbor["y"],x_loc,y_loc)
		all_neighbors.append({"id": int(neighbor["id"]), "x": float(neighbor["x"]), "y": float(neighbor["y"]),"dist": float(d)})
	
	all_neighbors = sorted(all_neighbors, key=operator.itemgetter("dist"))
	return all_neighbors


def getAllChests():
	with open("static/chest_locations.txt") as f:
		content = f.readlines()
	chest_arr = [x.strip() for x in content]
	all_chests = []

	chest_num = 0
	for chest in chest_arr:
		coords = chest.split(",")
		all_chests.append({"x": float(coords[0]) - 11, "y": float(coords[1]) - 11, "id": chest_num})
		chest_num += 1
	return all_chests


def dist(x0,y0,x1,y1):
	return pow(pow(x0 - x1, 2) + pow(y0 - y1, 2), .5)

def distToCircle(x,y,h,k,r):
	Vx = x - h
	Vy = y - k
	magV = pow(Vx * Vx + Vy * Vy, .5)
	Ax = h + Vx / magV * r
	Ay = k + Vy / magV * r
	return pow(pow(x - Ax, 2) + pow(y - Ay, 2), .5)


def returnArray(opened_chests,all_chests):
	chest_arr = []

	for chest_num in opened_chests:
		chest_x = all_chests[chest_num]["x"]
		chest_y = all_chests[chest_num]["y"]
		chest_arr.append({"id": chest_num, "x": chest_x, "y": chest_y})

	return chest_arr

def findPath(chest_ids,neighbors,path,optimal_path,circle_x,circle_y,time,idx):

	for n in neighbors[:5]:
		
		if n["id"] not in path:
			path.append(n["id"])
			time_to_chest = n["dist"] / px_per_sec
			time_to_circle = distToCircle(n["x"],n["y"],circle_x,circle_y,256) / px_per_sec

			#if n["id"] == 247:
			#	print(n["id"],path,time,time_to_chest,time_to_circle)
			
			if time - (time_to_chest + time_to_circle) <= 0:
				#end path
				return path,optimal_path

			idx += 1
			time -= time_to_chest
			
			new_path,optimal_path = findPath(chest_ids,getNeighbors(n["id"],chest_ids),path,optimal_path,circle_x,circle_y,time,idx)
			

			if len(new_path) > len(optimal_path):
				optimal_path = new_path[:]
			#print(n["id"],new_path)
			path = new_path[:-1]
	return path,optimal_path


all_chests = getAllChests()
#all_chests = [{"id": 220, "x": 643, "y": 99},{"id": 224, "x": 658, "y": 144}, {"id": 213, "x": 617, "y": 171}, {"id": 190, "x": 585, "y": 131}, {"id": 189, "x": 585, "y": 123}]

chest_ids = []
for chest in all_chests:
	chest_ids.append(int(chest["id"]))

source = {"x": 632, "y": 110}
circle = {"x": 650, "y": 480}
neighbors = getStartingNeighbors(all_chests,source)
starting_path = []
optimal_path = []

p,opt = findPath(chest_ids,neighbors,starting_path,optimal_path,circle["x"],circle["y"],time_left,0)

print(opt)