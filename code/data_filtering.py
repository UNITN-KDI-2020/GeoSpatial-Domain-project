# script to filter out useless data

import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Scope Definition & Inception/data/"
OUT_FOLDER = "./dataset/Informal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

filterMap = json.load(open("./code/data_filtering_config.json", "r"))


for mapIndex, (k, v) in enumerate(filterMap.items()):
	if ignore_existing and (path.exists(OUT_FOLDER + k) or path.exists(OUT_FOLDER + k.split('.')[0] + ".json")):
		continue

	IsJSON = False if k.split('.')[1] == "csv" else True
	data = None
	dataset = open(IN_FOLDER + k, "r")
	filteredData = {"records": []}

	print(k)

	if IsJSON:
		data = json.load(dataset)
		for it in v["iterator"].split('.'):
			if len(it) > 0:
				data = data[it]
		for d_i, d in enumerate(data):
			newRecord = {}
			for prop in v["props"]:
				fields = prop.split('.')
				subFieldRef = d
				for j, subfield in enumerate(fields):
					if j < len(fields) - 1:
						subFieldRef = subFieldRef[subfield]
					elif subfield in subFieldRef:
						newRecord[subfield] = subFieldRef[subfield]
			filteredData["records"].append(newRecord)

		with open(OUT_FOLDER + k, 'w+') as file:
			json.dump(filteredData, file)

	else:
		data = csv.reader(dataset, delimiter=";")
		filedsToSave = v["props"]
		fields = []
		fieldsIndex = []
		for row_i, row in enumerate(data):
			newRecord = {}
			if row_i == 0:
				fields = row
				for i, d in enumerate(row):
					if d in filedsToSave:
						fieldsIndex.append(i)
			else:
				for i, d in enumerate(row):
					if i in fieldsIndex and len(d) > 0:
						newRecord[fields[i]] = d
				filteredData["records"].append(newRecord)
		
		with open(OUT_FOLDER + k.split('.')[0] + ".json", 'w+') as file:
			json.dump(filteredData, file)

# Luoghi e punti di interesse GEO

for count, filename in enumerate(listdir(IN_FOLDER + "luoghi_e_punti_di_interesse_per_comune/")):
	
	if not "GEO" in filename or "di Ala" in filename or "Ossana" in filename or "Michele" in filename or(ignore_existing and path.exists(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune/" + filename)):
		continue

	dataset = open(IN_FOLDER  + "luoghi_e_punti_di_interesse_per_comune/" + filename, "r")
	filteredData = {"records": []}

	print(filename)

	data = json.load(dataset)
	data = data["features"]
	for d_i, d in enumerate(data):
		newRecord = {}
		newRecord["id"] = d["id"]
		newRecord["geometry"] = d["geometry"]
		newRecord["name"] = d["properties"]["name"]
		if "geo" in d["properties"]:
			newRecord["geo"] = d["properties"]["geo"]
		filteredData["records"].append(newRecord)

	with open(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune/" + filename, 'w+') as file:
		json.dump(filteredData, file)

# Luoghi e punti di interesse non GEO

for count, filename in enumerate(listdir(IN_FOLDER + "luoghi_e_punti_di_interesse_per_comune/")):
	
	if "GEO" in filename or path.exists(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune/" + filename.split('.')[0]+" GEO.json") or "Tassullo" in filename or "Sagron" in filename or "di Ala" in filename or "Ossana" in filename or "Michele" in filename or(ignore_existing and path.exists(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune/" + filename)):
		continue

	dataset = open(IN_FOLDER  + "luoghi_e_punti_di_interesse_per_comune/" + filename, "r")
	filteredData = {"records": []}

	print(filename)

	data = json.load(dataset)
	data = data["searchHits"]
	for d_i, d in enumerate(data):
		newRecord = {}
		newRecord["id"] = d["metadata"]["id"]
		newRecord["name"] = d["data"]["ita-IT"]["title"]
		if "geo" in d["data"]["ita-IT"]:
			newRecord["geo"] = d["data"]["ita-IT"]["geo"]
		filteredData["records"].append(newRecord)

	with open(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune/" + filename, 'w+') as file:
		json.dump(filteredData, file)

# Building

for count, filename in enumerate(listdir(IN_FOLDER + "building/")):
	
	if (ignore_existing and path.exists(OUT_FOLDER + "building/" + filename)):
		continue

	dataset = open(IN_FOLDER  + "building/" + filename, "r")
	filteredData = {"records": []}

	print(filename)

	data = json.load(dataset)
	data = data["features"]
	for d_i, d in enumerate(data):
		newRecord = {}
		newRecord["id"] = d["id"]
		newRecord["geometry"] = d["geometry"]
		filteredData["records"].append(newRecord)

	with open(OUT_FOLDER + "building/" + filename, 'w+') as file:
		json.dump(filteredData, file)