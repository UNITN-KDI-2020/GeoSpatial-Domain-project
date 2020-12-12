# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/bikesharing_stations/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

bikesharing_stations = {"records":[]}


for count, filename in enumerate(listdir(IN_FOLDER)):
	dataset = open(IN_FOLDER + filename, "r")

	print(filename)
	cityname = filename[:-5]

	data = json.load(dataset)["records"]

	for d_i, d in enumerate(data):
		if "position" in d:
			d["GeoShape"] = {"type":"Point", "GeoCoordinate": { "longitude" : d["position"][0], "latitude" : d["position"][1] } }
			d.pop("position")
		if cityname != "":
			d["city"] = cityname
		if "id" in d:
			d.pop("id")
		bikesharing_stations["records"].append(d)

with open(OUT_FOLDER + "bikesharing_stations.json", 'w+') as file:
	json.dump(bikesharing_stations, file)