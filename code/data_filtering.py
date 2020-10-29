# script to filter out useless data

import json
from os import path
from sys import argv

IN_FOLDER = "./dataset/Scope Definition & Inception/data/"
OUT_FOLDER = "./dataset/Informal Modeling/data/"
ignore_existing =  argv[1] if len(argv) > 1 else False

filterMap = json.load(open("./code/data_filtering_config.json", "r"))

for i, (k, v) in enumerate(filterMap.items()):
	if ignore_existing and path.exists(OUT_FOLDER + k):
		continue
	dataJson = open(IN_FOLDER + k, "r")
	data = json.load(dataJson)
	for it in v["iterator"].split('.'):
		data = data[it]

	filteredData = {"records": []}

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
