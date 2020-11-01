import json
import csv
from os import path,listdir
from sys import argv

IN_FOLDER = "./dataset/Scope Definition & Inception/metadata/"
OUT_FOLDER = "./dataset/Informal Modeling/metadata/"
ignore_existing = argv[1] if len(argv) > 1 else True

filterMap = json.load(open("./code/data_filtering_config.json", "r"))

for mapIndex, (k, v) in enumerate(filterMap.items()):
	if ignore_existing and (path.exists(OUT_FOLDER + k.split('.')[0] + "_METADATA.json")):
		continue
	metadataFile = k.split('.')[0] + "_METADATA.json"
	metadata = open(IN_FOLDER + metadataFile, "r")
	filteredData = {"records": []}

	print(metadataFile)

	data = json.load(metadata)
	propsToKeep = v["props"]
	newMetadata = {}
	for index, (field, value) in enumerate(data.items()):
		if field != "fields":
			newMetadata[field] = value
		else:
			newFields = {"properties" : {"fields":{}}}
			for i, (f, fv) in enumerate(value.items()):
				if f != "id":
					if f == "properties":
						for i2, (f2, fv2) in enumerate(fv.items()):
							if f2 == "fields":
								for i3, (f3, fv3) in enumerate(fv2.items()):
									contained = False
									for p in propsToKeep:
										ps = p.split('.')
										p = ps[len(ps)-1]
										if f3 == p:
											contained = True
											break
									if contained:
										newFields["properties"]["fields"][f3] = fv3
							else:
								newFields["properties"][f2] = fv2
					else:
						newFields[f] = fv
			newMetadata["fields"] = newFields
	
	with open(OUT_FOLDER + metadataFile, 'w+') as file:
			json.dump(newMetadata, file)
