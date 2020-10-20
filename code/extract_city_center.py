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
// fetch area "Trentino" to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
(
  // query part for: "building=yes"
  node["admin_level"=8](area.searchArea);
  way["admin_level"=8](area.searchArea);
  relation["admin_level"=8](area.searchArea);
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
with open('./city_center.geojson',mode="w") as f:
  geojson.dump(result,f)
