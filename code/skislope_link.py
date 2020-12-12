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
		# print(c)
		x += c["longitude"]
		y += c["latitude"]
		i += 1
	return np.array([x/i,y/i])

def toArray(m):
	out = []
	for i in m:
		out.append([i["longitude"],i["latitude"]])
	return np.array(out)

def find_skiarea(slopeCoords, point, slope, skiarea):
	slopeCoords = toArray(slopeCoords)
	nearest = None
	areaNearest = []
	valNearest = 1000000000
	area2 = []
	for areas in skiarea:
		for area in areas["GeoShape"]["GeoCoordinate"]:
			name = (areas["name"] if "name" in areas else "-")
			shape = np.array(area).shape
			# print(str(shape) + "\t"+ name)
			area2 = area
			if len(shape) != 1:
				area2 = area[0]
				for i in range(1,len(area)):
					area2.extend(area[i])
			mean = get_mean(area2)
			if valNearest > np.linalg.norm(mean-np.array(point)):
				nearest = name
				areaNearest = toArray(area2)
				valNearest = np.linalg.norm(mean-np.array(point))
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
	if "GeoShape" in slope:
		slopeCoords = np.array(slope["GeoShape"]["GeoCoordinate"], dtype=object)
		if len(slopeCoords[0]) > 2:
			slopeCoords = slopeCoords[0]
		mean = get_mean(slopeCoords)
		
		if find_skiarea(slopeCoords, Point(mean), slope, skiarea):
			count += 1
print("\nNumber of intersections: " + str(count))


with open(IN_FOLDER + "skislopes2.json", 'w+') as file:
	json.dump(newDataset, file)