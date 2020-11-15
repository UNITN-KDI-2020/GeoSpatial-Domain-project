# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/building/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

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
			d["GeoShape"] = d.pop("geometry")
			if "coordinates" in d["GeoShape"]:
				d["GeoShape"]["GeoCoordinate"] = d["GeoShape"].pop("coordinates")
		if cityname != "":
			d["city"] = cityname
		buildings["records"].append(d)



with open(OUT_FOLDER + "buildings.json", 'w+') as file:
	json.dump(buildings, file)