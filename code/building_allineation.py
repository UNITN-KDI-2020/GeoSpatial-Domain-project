# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/building/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else False

buildings = {"records":[]}


for count, filename in enumerate(listdir(IN_FOLDER)):
	dataset = open(IN_FOLDER + filename, "r")

	print(filename)
	cityname = filename.replace("-"," ")

	data = json.load(dataset)["records"]

	for d_i, d in enumerate(data):
		if "geo" in d:
			d["address"] = d.pop("geo")
		if "geometry" in d:
			d["GeoCoordinate"] = d.pop("geometry")
			if "coordinates" in d["GeoCoordinate"]:
				if d["GeoCoordinate"]["type"] == "Polygon":
					coordinates = d["GeoCoordinate"]["coordinates"]
					mediaX = 0
					mediaY = 0
					count = 0
					for edifici in coordinates:
						for edificio in edifici:
							mediaX += edificio[0]
							mediaY += edificio[1]
							count += 1
					d["GeoCoordinate"] = {"longitude" : mediaX/count, "latitude" : mediaY/count}
				elif d["GeoCoordinate"]["type"] == "Point":
					d["GeoCoordinate"] = {"longitude" : d["GeoCoordinate"]["coordinates"][0], "latitude" : d["GeoCoordinate"]["coordinates"][1]}
		if cityname != "":
			d["city"] = cityname
		buildings["records"].append(d)



with open(OUT_FOLDER + "buildings.json", 'w+') as file:
	json.dump(buildings, file)