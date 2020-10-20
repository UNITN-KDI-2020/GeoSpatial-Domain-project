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

highway_query = """
[out:json][timeout:25];
// fetch area “Trentino” to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
// gather results
(
  way["highway"="motorway"](area.searchArea);
  way["highway"="trunk"](area.searchArea);
  way["highway"="primary"](area.searchArea);
  way["highway"="secondary"](area.searchArea);
  // query part for: “highway=path”
);
// print results
out body;
>;
out skel qt;
"""
print(highway_query)
r = requests.get(url, params={'data': highway_query})
# res = api.get(building_query)
result = osmtogeojson.process_osm_json(r.json())
filepath = "./highway.geo.json"
print(filepath)
with open(filepath,mode="w") as f:
  geojson.dump(result,f)
