from flask import *
main = Blueprint('main', __name__, template_folder='views')

@main.route('/',methods=["GET"])
def main_route():
	with open("static/chest_locations.txt") as f:
		content = f.readlines()
	chest_arr = [x.strip() for x in content]
	all_chests = []

	chest_num = 0
	for chest in chest_arr:
		coords = chest.split(",")
		all_chests.append({"x": int(coords[0]) - 11, "y": int(coords[1]) - 11, "id": chest_num})
		chest_num += 1

	
	return render_template("main.html", all_chests=all_chests)