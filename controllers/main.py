from flask import *
main = Blueprint('main', __name__, template_folder='views')

@main.route('/',methods=["GET"])
def main_route():
	with open("static/towns.txt") as f:
		content = f.readlines()
	town_arr = [x.strip() for x in content]
	all_towns = []

	for town in town_arr:
		data = town.split('\t')
		all_towns.append({"name": data[0], "x": int(data[1]), "y": int(data[2])})


	with open("static/chest_locations.txt") as f:
		content = f.readlines()
	chest_arr = [x.strip() for x in content]
	all_chests = []

	chest_num = 0
	for chest in chest_arr:
		coords = chest.split(",")
		all_chests.append({"x": int(coords[0]) - 11, "y": int(coords[1]) - 11, "id": chest_num})
		chest_num += 1

	
	return render_template("main.html", all_chests=all_chests,all_towns=all_towns, tot_chests=len(all_chests))