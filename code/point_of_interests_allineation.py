# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Informal Modeling/data/luoghi_e_punti_di_interesse_per_comune/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

libraries = {"records":[]}
bars = {"records":[]}
sport_facilities = {"records":[]}
theaters = {"records":[]}
churches = {"records":[]}
ambulatories = {"records":[]}
eldery_centers = {"records":[]}

for count, filename in enumerate(listdir(IN_FOLDER)):
	dataset = open(IN_FOLDER + filename, "r")

	print(filename)
	cityname = filename[:-5] if not "GEO" in filename else filename[:-9]
	cityname = cityname[10:] if "Comune di" in cityname else ""

	data = json.load(dataset)["records"]

	for d_i, d in enumerate(data):
		if "geo" in d:
			d["address"] = d.pop("geo")
		if "geometry" in d:
			d["GeoCoordinate"] = d["geometry"].pop("coordinates")
		if cityname != "":
			d["city"] = cityname
		if d["name"] != None and "biblioteca" in d["name"].lower():
			library = {}
			library = d
			libraries["records"].append(library)
		if d["name"] != None and ("bar " in d["name"].lower() or "birr" in d["name"].lower()):
			bar = {}
			bar = d
			bars["records"].append(bar)
		if d["name"] != None and ("palazzetto" in d["name"].lower() or "sportivo" in d["name"].lower()):
			sportFacility = {}
			sportFacility = d
			sport_facilities["records"].append(sportFacility)
		if d["name"] != None and ("teatro" in d["name"].lower() or "auditorium" in d["name"].lower()):
			theater = {}
			theater = d
			theaters["records"].append(theater)
		if d["name"] != None and ("chiesa" in d["name"].lower() or "duomo" in d["name"].lower() or "basilica" in d["name"].lower() or "cappella" in d["name"].lower()):
			church = {}
			church = d
			churches["records"].append(church)
		if d["name"] != None and ("ambulatorio" in d["name"].lower() or "medico" in d["name"].lower()):
			ambulatory = {}
			ambulatory = d
			ambulatories["records"].append(ambulatory)
		if d["name"] != None and ("anziani" in d["name"].lower()):
			eldery_center = {}
			eldery_center = d
			eldery_centers["records"].append(eldery_center)


with open(OUT_FOLDER + "libraries.json", 'w+') as file:
	json.dump(libraries, file)
with open(OUT_FOLDER + "bars.json", 'w+') as file:
	json.dump(bars, file)
with open(OUT_FOLDER + "sport_facilities.json", 'w+') as file:
	json.dump(sport_facilities, file)
with open(OUT_FOLDER + "theaters.json", 'w+') as file:
	json.dump(theaters, file)
with open(OUT_FOLDER + "churches.json", 'w+') as file:
	json.dump(churches, file)
with open(OUT_FOLDER + "ambulatories.json", 'w+') as file:
	json.dump(ambulatories, file)
with open(OUT_FOLDER + "eldery_centers.json", 'w+') as file:
	json.dump(eldery_centers, file)