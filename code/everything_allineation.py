# script to allineate point of interests

import json
import csv
import numpy as np
import math
from os import path, listdir
from sys import argv
import pyproj as pj
import warnings
warnings.filterwarnings("ignore", category=Warning)

IN_FOLDER = "./dataset/Informal Modeling/data/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

exceptions = ["SAT_trails.json", "skiResorts_currentState.json", "areaski.json", "railway.json", "skislopes.json", "piste_ciclabili.json", "trails.json", "roads.json"]

inProj = pj.Proj('PROJCS["ETRS89_UTM_zone_32N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')
outProj = pj.Proj(init='epsg:4326')

# Data

def computeDistance(a,b):
	R = 6373.0
	dlat = b[0] - a[0]
	dlon = b[1] - a[1]

	temp1 = a = math.sin(dlat / 2)**2 + math.cos(a[0]) * math.cos(b[0]) * math.sin(dlon / 2)**2
	temp2 = 2 * math.atan2(math.sqrt(temp1), math.sqrt(1 - temp1))

	return R * temp2

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
				length = 0
				for i, coor in enumerate(coordinatesWKT):
					coor = coor.split(" ")
					y, x = pj.transform(inProj, outProj, coor[0], coor[1])
					coordinates.append([x, y])
					if i > 0:
						length = length + computeDistance(precCoord, np.array([x,y]))
					precCoord = np.array([x,y])
				d["totalLength"] = length
				d["GeoShape"] = {"type": "Line", "GeoCoordinate": coordinates}

	for d_i, d in enumerate(data):
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
			

		if "@id" in d:
			d.pop("@id")
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
		if "addr:city" in d:
			d["city"] = d.pop("addr:city")
		if "addr:housenumber" in d:
			d["housenumber"] = d.pop("addr:housenumber")
		if "addr:postcode" in d:
			d["postal_code"] = d.pop("addr:postcode")
		if "addr:street" in d:
			d["address"] = d.pop("addr:street")
		if "addr:province" in d:
			d["province"] = d.pop("addr:province")
		if "atm" in d:
			d["hasAtm"] = d.pop("atm")
		newDataset["records"].append(d)

	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newDataset, file)

# Metadata

IN_FOLDER = "./dataset/Informal Modeling/metadata/"
OUT_FOLDER = "./dataset/Formal Modeling/metadata/"

exceptions = ["skiResorts_static_METADATA.json","healthcare_METADATA.json","SAT_trails_METADATA.json", "skiResorts_currentState_METADATA.json", "elementari_METADATA.json","medie_METADATA.json","materne_METADATA.json","superiori_METADATA.json","luoghi_e_punti_di_interesse_per_comune_METADATA.json"]


for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or (ignore_existing and path.exists(OUT_FOLDER + filename)) or filename in exceptions:
		continue

	print(filename)
	metadata = open(IN_FOLDER + filename, "r")
	data = json.load(metadata)

	newMetadata = {}

	for i, (k, v) in enumerate(data.items()):
		if "fields" == k:
			if "properties" in v:
				newMetadata[k] = v["properties"]["fields"]
			else:
				newMetadata[k] = v
			newMetadata[k]["GeoShape"] = {
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
			if "WKT" in d:
				d.pop("WKT")
			if "addr:city" in d:
				d["city"] = d.pop("addr:city")
			if "addr:housenumber" in d:
				d["housenumber"] = d.pop("addr:housenumber")
			if "addr:postcode" in d:
				d["postal_code"] = d.pop("addr:postcode")
			if "addr:street" in d:
				d["address"] = d.pop("addr:street")
			if "addr:province" in d:
				d["province"] = d.pop("addr:province")
			if "atm" in d:
				d["hasAtm"] = d.pop("atm")
			newMetadata["fields"] = d
		
		else:
			newMetadata[k] = v

	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newMetadata, file)
