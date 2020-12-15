# script to allineate point of interests

import json
import csv
from os import path,listdir
from sys import argv
import pyproj as pj
import warnings
warnings.filterwarnings("ignore", category=Warning)

IN_FOLDER = "./dataset/Informal Modeling/data/schools/"
OUT_FOLDER = "./dataset/Formal Modeling/data/"
ignore_existing = argv[1] if len(argv) > 1 else True

schools = {"records":[]}

inProj = pj.Proj('PROJCS["ETRS89_UTM_zone_32N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')
outProj = pj.Proj(init='epsg:4326')
x1,y1 = 663007.733371042530052, 5111238.711814826354384
y2,x2 = pj.transform(inProj,outProj,x1,y1)
print(str(x2)+", "+str(y2))


# Data

for count, filename in enumerate(listdir(IN_FOLDER)):
	dataset = open(IN_FOLDER + filename, "r")

	print(filename)
	school = "elementary"
	if filename == "materne.json":
		school = "nursery"
	if filename == "medie.json":
		school = "middle"
	if filename == "superiori.json":
		school = "high"

	data = json.load(dataset)["records"]

	for d_i, d in enumerate(data):
		if "WKT" in d:
			coordinates = d["WKT"].replace("POINT (", "").replace(")","").split(" ")
			d.pop("WKT")
			y,x = pj.transform(inProj,outProj,coordinates[0],coordinates[1])
			d["GeoCoordinate"] = { "longitude" : y, "latitude" : x }
		if "civico_alf" in d:
			d["HouseNumber"] = d.pop("civico_alf")
		if "destra" in d:
			d["address"] = d.pop("destra")
		if "sobborgo" in d:
			d["city"] = d.pop("sobborgo")
		if "scuola" in d:
			d["name"] = d.pop("scuola")
		if "school type" in d:
			d.pop("school type")
		d["SchoolType"] = school
		schools["records"].append(d)

with open(OUT_FOLDER + "schools.json", 'w+') as file:
	json.dump(schools, file)

