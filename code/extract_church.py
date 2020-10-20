# import overpass
import requests
import geojson
import unicodedata
from osmtogeojson import osmtogeojson
import re
import os
import time

# api = overpass.API()
url = "http://overpass-api.de/api/interpreter"

building_query = """
[out:json][timeout:25];
// fetch area “Trentino” to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
(
  // query part for: “building=yes”
  node["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
  way["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
  relation["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
);
// print results
out body;
>;
out skel qt;
"""
print(building_query)
r = requests.get(url, params={'data': building_query})
# res = api.get(building_query)

result = osmtogeojson.process_osm_json(r.json())
with open('./church.geojson',mode="w") as f:
  geojson.dump(result,f)
