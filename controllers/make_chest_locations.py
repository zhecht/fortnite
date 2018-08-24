
from bs4 import BeautifulSoup as BS
import urllib.request as urllib
import time, operator



def get_chest_coords(css):
	all_coords = css.split("transform: translate3d(")[1].split(")")[0].split(", ")
	return int(all_coords[0][:-2]), int(all_coords[1][:-2])

def get_distance(x, y):
	return pow((pow(x,2) + pow(y,2)), .5)

#url = "http://www.fortnitechests.info"

#html = urllib.urlopen(url)
#soup = BS(html.read(), "lxml")


soup = BS(open("static/fortnite_chests.htm", "r"), "lxml")
all_chests = soup.find_all("img", class_="leaflet-marker-icon")

chest_arr = []
for chest in all_chests:
	style = chest["style"]
	x_coord, y_coord = get_chest_coords(style)
	chest_arr.append({"x": x_coord, "y": y_coord, "dist": get_distance(x_coord, y_coord)})


chest_arr = sorted(chest_arr, key=operator.itemgetter("dist"))

file = open("static/chest_locations.txt", "w")
for chest in chest_arr:
	file.write("%s,%s\n" % (chest["x"], chest["y"]))
file.close()