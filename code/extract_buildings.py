# import overpass
import requests
import geojson
import unicodedata
from osmtogeojson import osmtogeojson
import re
import os
import time

comuni = [
#  "Ala",
#  "Albiano",
#  "Aldeno",
#  "Altavalle",
#  "Altopiano della Vigolana",
#  "Amblar-Don",
#  "Andalo",
  "Arco",
#  "Avio",
#  "Baselga di Piné",
#  "Bedollo",
#  "Besenello",
#  "Bieno",
#  "Bleggio Superiore",
#  "Bocenago",
#  "Bondone",
#  "Borgo Chiese",
#  "Borgo d'Anaunia",
#  "Borgo Lares",
#  "Borgo Valsugana",
#  "Brentonico",
#  "Bresimo",
#  "Caderzone Terme",
#  "Calceranica al Lago",
#  "Caldes",
#  "Caldonazzo",
#  "Calliano",
#  "Campitello di Fassa",
#  "Campodenno",
#  "Canal San Bovo",
#  "Canazei",
#  "Capriana",
#  "Carisolo",
#  "Carzano",
#  "Castel Condino",
#  "Castel Ivano",
#  "Castello-Molina di Fiemme",
#  "Castello Tesino",
#  "Castelnuovo",
#  "Cavalese",
#  "Cavareno",
#  "Cavedago",
#  "Cavedine",
#  "Cavizzana",
#  "Cembra Lisignago",
#  "Cimone",
#  "Cinte Tesino",
#  "Cis",
#  "Civezzano",
#  "Cles",
#  "Comano Terme",
#  "Commezzadura",
#  "Contà",
#  "Croviana",
#  "Dambel",
#  "Denno",
#  "Dimaro Folgarida",
#  "Drena",
#  "Dro",
#  "Fai della Paganella",
#  "Fiavé",
#  "Fierozzo - Vlarotz",
#  "Folgaria",
#  "Fornace",
#  "Frassilongo - Garait",
#  "Garniga Terme",
#  "Giovo",
#  "Giustino",
#  "Grigno",
#  "Imer",
#  "Isera",
#  "Lavarone",
#  "Lavis",
#  "Ledro",
#  "Levico Terme",
#  "Livo",
#  "Lona-Lases",
#  "Lusérn - Luserna",
#  "Madruzzo",
#  "Malé",
#  "Massimeno",
#  "Mazzin",
#  "Mezzana",
#  "Mezzano",
#  "Mezzocorona",
#  "Mezzolombardo",
#  "Moena",
#  "Molveno",
#  "Mori",
#  "Nago-Torbole",
#  "Nogaredo",
#  "Nomi",
#  "Novaledo",
#  "Novella",
#  "Ospedaletto",
#  "Ossana",
#  "Palù del Fersina - Palai en Bersntol",
#  "Panchià",
#  "Peio",
#  "Pellizzano",
#  "Pelugo",
#  "Pergine Valsugana",
#  "Pieve di Bono-Prezzo",
#  "Pieve Tesino",
#  "Pinzolo",
#  "Pomarolo",
#  "Porte di Rendena",
#  "Predaia",
#  "Predazzo",
#  "Primiero San Martino di Castrozza",
#  "Rabbi",
#  "Riva del Garda",
#  "Romeno",
#  "Roncegno Terme",
#  "Ronchi Valsugana",
#  "Ronzo-Chienis",
#  "Ronzone",
#  "Roveré della Luna",
#  "Rovereto",
#  "Ruffré-Mendola",
#  "Rumo",
#  "Sagron Mis",
#  "Samone",
#  "San Lorenzo Dorsino",
#  "San Michele all'Adige",
#  "Sant'Orsola Terme",
#  "Sanzeno",
#  "Sarnonico",
#  "Scurelle",
#  "Segonzano",
#  "Sella Giudicarie",
  "San Giovanni di Fassa",
#  "Sfruz",
#  "Soraga di Fassa",
#  "Sover",
#  "Spiazzo",
#  "Spormaggiore",
#  "Sporminore",
#  "Stenico",
#  "Storo",
#  "Strembo",
#  "Telve",
#  "Telve di Sopra",
#  "Tenna",
#  "Tenno",
#  "Terragnolo",
#  "Terre d'Adige",
#  "Terzolas",
#  "Tesero",
#  "Tione di Trento",
#  "Ton",
#  "Torcegno",
#  "Trambileno",
#  "Tre Ville",
#  "Trento",
#  "Valdaone",
#  "Valfloriana",
#  "Vallarsa",
#  "Vallelaghi",
#  "Vermiglio",
#  "Vignola Falesina",
#  "Villa Lagarina",
#  "Ville d'Anaunia",
#  "Ville di Fiemme",
#  "Volano",
#  "Ziano di Fiemme",
]

# api = overpass.API()
url = "http://overpass-api.de/api/interpreter"

for comune in comuni:
  building_query = """
  [out:json][timeout:25];
  // fetch area “Trentino” to search in
  ( area["name"="Provincia di Trento"]; )->.externalBoundary;
  ( area["name"="{}"]; )->.searchArea;
  (
    // query part for: “building=yes”
    node["building"="yes"](area.searchArea)(area.externalBoundary);
    way["building"="yes"](area.searchArea)(area.externalBoundary);
    relation["building"="yes"](area.searchArea)(area.externalBoundary);
  );
  // print results
  out body;
  >;
  out skel qt;
  """.format(comune)
  print(building_query)
  r = requests.get(url, params={'data': building_query})
  # res = api.get(building_query)
  try:
    result = osmtogeojson.process_osm_json(r.json())
    comune_clean = str(re.sub('[^\w\s-]', '', comune).strip().lower())
    comune_clean = str(re.sub('[-\s]+', '-', comune_clean))
    comune_clean = unicodedata.normalize('NFKD', comune_clean).encode('ascii', 'ignore')
    comune_clean = comune_clean.decode('utf-8')
    filepath = os.path.join('./building', "{}.geo.json".format(comune_clean))
    print(filepath)
    with open(filepath,mode="w") as f:
      geojson.dump(result,f)
  except e:
    print("Error during the extraction of comune {}".format(comune))
    print(r.content)
  time.sleep(5)
