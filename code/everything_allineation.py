# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

exceptions = ["SAT_trails.json","skiResorts_currentState.json"]

for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or (ignore_existing and path.exists(OUT_FOLDER + filename)) or filename in exceptions:
		continue

	print(filename)
	dataset = open(IN_FOLDER + filename, "r")
	data = json.load(dataset)["records"]

	newDataset = {"records":[]}

	if "skiresort.json" in filename:
		for d_i, d in enumerate(data):
			d["Total lenght"] = d["Total lenght"][7:] # "Total: " removing
			d["Number of lifts"] = d["Number of lifts"][7:] # "Total: " removing
			d["raiting"] = d["raiting"][:-15] # " stars out of 5" removing

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
		if "fumetto" in d:
			d["address"] = d.pop("fumetto")
		if "desvia" in d:
			d["address"] = d.pop("desvia")
		if "sobborgo" in d:
			d["city"] = d.pop("sobborgo")
		newDataset["records"].append(d)

	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newDataset, file)