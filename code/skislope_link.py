import json
from operator import contains
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
import numpy as np

newDataset = {"records": []}

def get_mean(m):
	x = 0
	y = 0
	i = 0
	for c in m:
		x += c[0]
		y += c[1]
		i += 1
	return np.array([x/i,y/i])

def find_skiarea(slopeCoords, point, slope, skiarea):
	nearest = None
	areaNearest = []
	valNearest = 1000000000
	area2 = []
	for areas in skiarea:
		for area in areas["GeoShape"]["GeoCoordinate"]:
			name = (areas["name"] if "name" in areas else "-")
			shape = np.array(area).shape
			area2 = area
			if len(shape) != 2:
				area2 = area[0]
				for i in range(1,len(area)):
					area2.extend(area[i])
			mean = get_mean(area2)
			if valNearest > np.linalg.norm(mean-np.array(point)):
				nearest = name
				areaNearest = area2
				valNearest = np.linalg.norm(mean-np.array(point))
				# print(name + "\t" + str(valNearest))
	found = False
	if len(slopeCoords) > 2:
		p1 = Polygon(slopeCoords)
		p2 = Polygon(areaNearest)
		found = p1.intersects(p2)
	elif len(slopeCoords) == 2:
		p1 = LineString(slopeCoords)
		p2 = Polygon(areaNearest)
		found = p1.intersects(p2)
	if nearest != None and nearest != "-" and found:
		slope["skiarea"] = nearest
		slope.pop("id")
		if slope["GeoShape"]["type"] == "LineString":
			slope["GeoShape"]["type"] = "Line"
		newDataset["records"].append(slope)
		return True
	newDataset["records"].append(slope)
	return False

IN_FOLDER = "./dataset/Formal Modeling/data/"

dataset = open(IN_FOLDER + "areaski.json", "r")
skiarea = json.load(dataset)["records"]

dataset = open(IN_FOLDER + "skislopes.json", "r")
skislopes = json.load(dataset)["records"]
found = False
count = 0

for slope in skislopes:
	slopeCoords = np.array(slope["GeoShape"]["GeoCoordinate"], dtype=object)	
	if len(slopeCoords.shape) != 2:
		slopeCoords = np.array(slopeCoords[0])
	# 	print(slopeCoords)
	if slope["GeoShape"]["type"] != "Point":
		mean = get_mean(slopeCoords)
		if find_skiarea(slopeCoords, Point(mean), slope, skiarea):
			count += 1
		print(slope["name"] if "name" in slope else "---")
	else:
		slope["GeoCoordinate"] = slope["GeoShape"]["GeoCoordinate"]
		slope.pop("GeoShape")
print("\nNumber of intersections: " + str(count))


with open(IN_FOLDER + "skislopes2.json", 'w+') as file:
	json.dump(newDataset, file)