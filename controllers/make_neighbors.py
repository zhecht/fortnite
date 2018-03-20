import operator
import os

def dist(x0,y0,x1,y1):
	return pow(pow(x0 - x1, 2) + pow(y0 - y1, 2), .5)

with open("static/chest_locations.txt") as f:
	content = f.readlines()
chest_arr = [x.strip() for x in content]
all_chests = []

chest_num = 0
for chest in chest_arr:
	coords = chest.split(",")
	all_chests.append({"x": int(coords[0]) - 11, "y": int(coords[1]) - 11, "id": chest_num})
	chest_num += 1


for chest in all_chests:
	x_loc = chest["x"]
	y_loc = chest["y"]
	chest_id = chest["id"]

	all_neighbors = []
	for neighbor in all_chests:
		if neighbor["id"] != chest_id:
			d = dist(neighbor["x"],neighbor["y"],x_loc,y_loc)
			all_neighbors.append({"id": neighbor["id"],"dist": d, "x": neighbor["x"], "y": neighbor["y"]})
	all_neighbors = sorted(all_neighbors, key=operator.itemgetter("dist"))
	
	directory = "static/neighbors/%s" % chest_id
	if not os.path.exists(directory):
		os.makedirs(directory)

	file = open("%s/neighbors.txt" % directory, "w")
	for neighbor in all_neighbors:
		file.write("%s,%s,%s,%s\n" % (neighbor["id"], neighbor["x"], neighbor["y"],neighbor["dist"]))
	file.close()
