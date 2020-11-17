# script to allineate point of interests

import json
import csv
from os import path, listdir
from sys import argv
import pyproj as pj
import warnings
warnings.filterwarnings("ignore", category=Warning)

IN_FOLDER = "./dataset/Informal Modeling/data/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

exceptions = ["SAT_trails.json", "skiResorts_currentState.json"]

inProj = pj.Proj('PROJCS["ETRS89_UTM_zone_32N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')
outProj = pj.Proj(init='epsg:4326')

# Data

for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or (ignore_existing and path.exists(OUT_FOLDER + filename)) or filename in exceptions:
		continue

	print(filename)
	dataset = open(IN_FOLDER + filename, "r")
	data = json.load(dataset)["records"]

	newDataset = {"records": []}

	if "skiresort.json" in filename:
		for d_i, d in enumerate(data):
			d["Total lenght"] = d["Total lenght"][7:]  # "Total: " removing
			d["Number of lifts"] = d["Number of lifts"][7:]  # "Total: " removing
			d["raiting"] = d["raiting"][:-15]  # " stars out of 5" removing

	if "piste_ciclabili.json" in filename:
		for d_i, d in enumerate(data):
			d["type"] = d.pop("tipologia")
			d["path type"] = d.pop("tipo")
			if "WKT" in d:
				coordinatesWKT = d["WKT"].replace(
				    "LINESTRING (", "").replace(")", "").split(",")
				coordinates = []
				d.pop("WKT")
				for coor in coordinatesWKT:
					coor = coor.split(" ")
					y, x = pj.transform(inProj, outProj, coor[0], coor[1])
					coordinates.append([x, y])
				d["GeoShape"] = {"type": "Line", "GeoCoordinate": coordinates}

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

# Metadata

IN_FOLDER = "./dataset/Informal Modeling/metadata/"
OUT_FOLDER = "./dataset/Formal Modeling/metadata/"

exceptions = ["SAT_trails.json", "skiResorts_currentState.json"]


for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or (ignore_existing and path.exists(OUT_FOLDER + filename)) or filename in exceptions:
		continue

	print(filename)
	metadata = open(IN_FOLDER + filename, "r")
	data = json.load(metadata)

	newMetadata = {"records": []}

	for i, (k, v) in enumerate(data.items()):
		if "fields" == k:
			newMetadata[k] = v["properties"]["fields"]
			newMetadata["GeoShape"] = {
					"type": "GeoShape",
					"description": "object containing location information",
					"data_definition": "Common",
					"fields": 
						{
							"type": 
								{
									"type": "string",
									"description": "type of GeoShape (Line, Polygon, Point)",
									"data_definition": "Common"
								},
							"GeoCoordinates": 
								{
									"type": "int[2]",
									"description": "Coordinates of the location in EPSG 4326 projection standard",
									"data_definition": "Common"
								}
						}
					}
			d = newMetadata["fields"] 
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
			newMetadata["fields"] = d
		
		else:
			newMetadata[k] = v

	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newMetadata, file)
