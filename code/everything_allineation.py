# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

exceptions = ["SAT_trails.json", "skiresort.json","skiResorts_currentState.json"]

for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or filename in exceptions:
		continue

	dataset = open(IN_FOLDER + filename, "r")
	newDataset = {"records":[]}

	print(filename)

	data = json.load(dataset)["records"]

	for d_i, d in enumerate(data):
		if "geometry" in d:
			d["GeoShape"] = d.pop("geometry")
			if "coordinates" in d["GeoShape"]:
				d["GeoShape"]["GeoCoordinate"] = d["GeoShape"].pop("coordinates")
		if "@id" in d:
			d["id"] = d.pop("@id")
		if "via" in d:
			d["address"] = d.pop("via")
		if "comune" in d:
			d["city"] = d.pop("comune")
		if "civico" in d:
			d["HouseNumber"] = d.pop("civico")
		if "barrato" in d:
			d["BarNumber"] = d.pop("barrato")
		newDataset["records"].append(d)

	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newDataset, file)