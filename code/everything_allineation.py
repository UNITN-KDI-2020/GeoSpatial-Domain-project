# script to allineate point of interests

# from shapely.geometry.polygon import Polygon
from functools import partial
import pyproj
# import shapely.ops as ops
import ujson
import json
import csv
import numpy as np
import math
from os import path, listdir
from sys import argv, stdout
import pyproj as pj
import timeit
import warnings
warnings.filterwarnings("ignore", category=Warning)

IN_FOLDER = "./dataset/Informal Modeling/data/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

exceptions = ["SAT_trails.json", "skiResorts_currentState.json", "trails.json"]

inProj = pj.Proj('PROJCS["ETRS89_UTM_zone_32N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')
outProj = pj.Proj(init='epsg:4326')

# Data

def get_mean(m):
	x = 0
	y = 0
	i = 0
	for c in m:
		x += c[0]
		y += c[1]
		i += 1
	return [x/i,y/i]

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
	playground = {"records": []}

	if "civici_web.json" in filename:
		length = len(data)
		for d_i, d in enumerate(data):
			# start = timeit.default_timer()
			if "geometry" in d:
				coor = d["geometry"]["coordinates"]
				d.pop("geometry")
				x, y = pj.transform(inProj, outProj, coor[0], coor[1])
				d["GeoCoordinate"] = { "longitude" : x, "latitude" : y }
			# stop = timeit.default_timer()
			if d_i % 10 == 0:
				print('\rprogress: ',round(d_i/length*100,1),"%\t",d_i,"/",length, end='')
				stdout.flush()

	if "park.json" in filename:
		for d_i, d in enumerate(data):
			if "playground" in d:
				d.pop("playground")
			if "playground:theme" in d:
				d.pop("playground:theme")
			if "opening_hours" in d:
				d.pop("opening_hours")
			if "playground:water" in d:
				d.pop("playground:water")

	if "parking.json" in filename:
		for d_i, d in enumerate(data):
			if "opening_hours" in d:
				d.pop("opening_hours")

	if "supermarket.json" in filename:
		for d_i, d in enumerate(data):
			if "geometry" in d and "Polygon" == d["geometry"]["type"]:
				poly = np.array(d["geometry"]["coordinates"])
				buildingPoly = Polygon(poly if len(poly.shape) == 2 else poly[0])
				geom_area = ops.transform(
					partial(
						pyproj.transform,
						pyproj.Proj(init='EPSG:4326'),
						pyproj.Proj(
							proj='aea',
							lat_1=buildingPoly.bounds[1],
							lat_2=buildingPoly.bounds[3])),
					buildingPoly)
				d["area"] = geom_area.area

	if "skiresort.json" in filename:
		for d_i, d in enumerate(data):
			d["Total lenght"] = d["Total lenght"][7:]  # "Total: " removing
			d["Number of lifts"] = d["Number of lifts"][7:]  # "Total: " removing
			d["raiting"] = d["raiting"][:-15]  # " stars out of 5" removing

	if "skislopes.json" in filename:
		for d_i, d in enumerate(data):
			d["GeoShape"] = d.pop("geometry")
			if "coordinates" in d["GeoShape"]:
				d["GeoShape"]["GeoCoordinate"] = d["GeoShape"].pop("coordinates")
				if d["GeoShape"]["type"] == "Polygon" or d["GeoShape"]["type"] == "MultiLineString":
					d["GeoShape"]["type"] = "Polygon"
					coordinates = d["GeoShape"]["GeoCoordinate"]
					for edifici_i, edifici in enumerate(coordinates):
						for edificio_i, edificio in enumerate(edifici):
							d["GeoShape"]["GeoCoordinate"][edifici_i][edificio_i] = { "longitude" : edificio[0], "latitude" : edificio[1] }
				elif d["GeoShape"]["type"] == "LineString" or d["GeoShape"]["type"] == "Line":
					d["GeoShape"]["type"] = "Path"
					coordinates = d["GeoShape"]["GeoCoordinate"]
					for p_i, point in enumerate(coordinates):
						d["GeoShape"]["GeoCoordinate"][p_i] = { "longitude" : point[0], "latitude" : point[1] }
				elif d["GeoShape"]["type"] == "Point":
					coordinates = d["GeoShape"]["GeoCoordinate"]
					d.pop("GeoShape")
					d["GeoCoordinate"] = {"longitude" : coordinates[0], "latitude" : coordinates[1]}
			if "piste:type" in d:
				d["SlopeType"] = d.pop("piste:type")
			if "piste:difficulty" in d:
				d["SlopeDifficultyType"] = d.pop("piste:difficulty")

	if "areaski.json" in filename:
		for d_i, d in enumerate(data):
			area2 = []
			mean = []
			for a_i, area in enumerate(d["GeoShape"]["GeoCoordinate"]):
				shape = np.array(area).shape
				area2 = area
				if len(shape) != 2:
					area2 = area[0]
					for i in range(1,len(area)):
						area2.extend(area[i])
				mean.append(get_mean(area2))
				if len(shape) != 2:
					for c_i, coordinate in enumerate(area[0]):
						d["GeoShape"]["GeoCoordinate"][a_i][0][c_i] = { "longitude" : coordinate[0], "latitude" : coordinate[1] }
				else:
					for c_i, coordinate in enumerate(area):
						d["GeoShape"]["GeoCoordinate"][a_i][c_i] = { "longitude" : coordinate[0], "latitude" : coordinate[1] }
			mean = get_mean(mean)
			d["GeoCoordinate"] = { "longitude" : mean[0], "latitude" : mean[1] }
			if "rating" in d:
				d.pop("rating")
			if "elevation" in d:
				d.pop("elevation")
			if "raiting" in d:
				d.pop("raiting")
			if "openingTime" in d:
				d.pop("openingTime")
			if "openingDate" in d:
				d.pop("openingDate")
			if "openingDate" in d:
				d.pop("openingDate")
			if "Description" in d:
				d.pop("Description")
			if "General Season" in d:
				d.pop("General Season")
		
	if "piste_ciclabili.json" in filename:
		for d_i, d in enumerate(data):
			d.pop("tipo")
			if "fumetto" in d:
				d["name"] = d.pop("fumetto")
			if "WKT" in d:
				coordinatesWKT = d["WKT"].replace(
				    "LINESTRING (", "").replace(")", "").split(",")
				coordinates = []
				d.pop("WKT")
				length = 0
				for i, coor in enumerate(coordinatesWKT):
					coor = coor.split(" ")
					y, x = pj.transform(inProj, outProj, coor[0], coor[1])
					coordinates.append({ "longitude" : y, "latitude" : x })
					if i > 0:
						length = length + computeDistance(precCoord, np.array([x,y]))
					precCoord = np.array([x,y])
				d["totalLength"] = length
				d["GeoShape"] = {"type": "Line", "GeoCoordinate": coordinates}
			if "tipologia" in d:
				tipo = d.pop("tipologia")
				d["reservedForBike"] = 1 if "Ciclopedonale" in tipo else 0
	
	if "outdooractive_trails.json" in filename:
		for d_i, d in enumerate(data):
			if "route" in d:
				d["Path"] = d.pop("route")
				d["Path"]["GeoCoordinate"] = d["Path"].pop("geoPoints")
				if "description" in d:
					d["Path"].pop("description")

	if "climb.json" in filename:
		for d_i, d in enumerate(data):
			if "opening_hours" in d:
				d.pop("opening_hours")

	if "stop_times.json" in filename:
		for d_i, d in enumerate(data):
			if "departure_time" in d:
				times = d["departure_time"].split(":")
				d["departure_time"] = {"Hours": times[0], "Minutes": times[1], "Seconds": times[2]}
			if "arrival_time" in d:
				times = d["arrival_time"].split(":")
				d["arrival_time"] = {"Hours": times[0], "Minutes": times[1], "Seconds": times[2]}
				

	for d_i, d in enumerate(data):
		if "geometry" in d:
			d["GeoCoordinate"] = d.pop("geometry")
			if "coordinates" in d["GeoCoordinate"]:
				if d["GeoCoordinate"]["type"] == "Polygon" or d["GeoCoordinate"]["type"] == "MultiLineString" or d["GeoCoordinate"]["type"] == "MultiPolygon":
					coordinates = d["GeoCoordinate"]["coordinates"]
					mediaX = 0
					mediaY = 0
					count = 0

					if d["GeoCoordinate"]["type"] == "MultiPolygon":
						coordinates = np.array(coordinates, dtype=object).ravel()

					for edifici_i, edifici in enumerate(coordinates):
						for edificio_i, edificio in enumerate(edifici):
							# d["GeoCoordinate"]["coordinates"][edifici_i][edificio_i] = { "longitude" : edificio[0], "latitude" : edificio[1] }
							mediaX += edificio[0]
							mediaY += edificio[1]
							count += 1
					
					d["GeoCoordinate"] = {"longitude" : mediaX/count, "latitude" : mediaY/count}
				elif d["GeoCoordinate"]["type"] == "LineString" or d["GeoCoordinate"]["type"] == "Line":
					coordinates = d["GeoCoordinate"]["coordinates"]
					mediaX = 0
					mediaY = 0
					count = 0
					for p_i, point in enumerate(coordinates):
						# d["GeoCoordinate"]["coordinates"][p_i] = { "longitude" : point[0], "latitude" : point[1] }
						mediaX += point[0]
						mediaY += point[1]
						count += 1
					d["GeoCoordinate"] = {"longitude" : mediaX/count, "latitude" : mediaY/count}
				elif d["GeoCoordinate"]["type"] == "Point":
					d["GeoCoordinate"] = {"longitude" : d["GeoCoordinate"]["coordinates"][0], "latitude" : d["GeoCoordinate"]["coordinates"][1]}


		if "@id" in d:
			d.pop("@id")
		if "id" in d:
			d.pop("id")
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
		
		if "park.json" in filename:
			if "leisure" in d:
				if "park" == d["leisure"]:
					d.pop("leisure")
					newDataset["records"].append(d)
				else:
					d.pop("leisure")
					playground["records"].append(d)
		else:
			newDataset["records"].append(d)

	with open(OUT_FOLDER + filename, 'w+') as file:
		ujson.dump(newDataset, file)

	if "park.json" in filename:
		with open(OUT_FOLDER + "playground.json", 'w+') as file:
			ujson.dump(playground, file)

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
