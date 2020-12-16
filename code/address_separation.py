import json
import re
from os import path, listdir
import warnings
warnings.filterwarnings("ignore", category=Warning)

alreadyParsed = ["internet_quality_trento.json"]

exceptions = [] # "buildings.json", "trails.json"

file_comuni = open("./code/italia_comuni.json", "r")
regioni = json.load(file_comuni)["regioni"]
trentino = [x for x in regioni if x["nome"] == "Trentino-Alto Adige"][0]
comuni = [x["nome"] for x in trentino["province"][0]["comuni"]]
comuni.extend([x["nome"] for x in trentino["province"][1]["comuni"]])
comuni.remove('Don')


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def extractCity(address):
	for c in comuni:
		if (c.lower()+" ") in address.lower():
			return True, c
		if (" "+c.lower()) in address.lower():
			return True, c
		if len(c)>3 and c.lower() in address.lower():
			return True, c
	return False, None

def parse(address, city):
	out = {}
	prefixes = ["via", "piazza", "corso", "piaz", "strada provinciale", "strada", "vicolo", "cort", "cianton", "localita'", "viale", "piazzale", "p.za", "p.le", "c.so", "porta", "largo", "piaza", "piazzetta"]
	if city == None:
		res, city = extractCity(address)
		if res:
			out["city"] = city
			address = address.replace(city, "")
	else:
		address = address.replace(city, "")
	subaddr = re.split("[,;-]+", address)
	searchForStreet = -1
	street = ""
	for a_i, addr in enumerate(subaddr):
		splittedAddr = addr.split()
		if a_i - 1 == searchForStreet and searchForStreet >= 0:
			out["StreetName"] = street
			street = ""
			searchForStreet = -2
		for w_i, word in enumerate(splittedAddr):
			if word.lower() in prefixes:
				out["StreetType"] = word
				if searchForStreet >= 0:
					out["StreetName"] = street
					street = ""
					searchForStreet = -2
				if w_i == 0 and a_i == 0:
					searchForStreet = a_i
			elif RepresentsInt(word):
				if len(word) > 3:
					out["postal_code"] = word
				else:
					out["HouseNumber"] = word
				if searchForStreet >= 0:
					out["StreetName"] = street
					street = ""
					searchForStreet = -2
			elif searchForStreet >= 0:
				if a_i == searchForStreet:
					street += ("" if street == "" else " ") + word
					if a_i+1 == len(subaddr) and w_i+1==len(splittedAddr) and street != "":
						out["StreetName"] = street
				else:
					out["StreetName"] = street
					street = ""
					searchForStreet = -2
	if len(out.keys()) == 0:
		return None
	else:
		return out
	

IN_FOLDER = "./dataset/Formal Modeling/data/"
OUT_FOLDER = "./dataset/Data Integration/data/"

countAddress = 0
countValid = 0

# Parsing test
print(parse("Piazza Cesare Battisti - Cavalese", None))

for count, filename in enumerate(listdir(IN_FOLDER)):
	# Check if the file it is not in the 
	if not ".json" in filename or filename in exceptions or filename in alreadyParsed:
		continue
	print(filename)
	
	#open dataset
	dataset = open(IN_FOLDER + filename, "r")
	data = json.load(dataset)
	if "records" in data:
		data = data["records"]

	newDataset = {"records": []}

	countAddress = 0
	countValid = 0

	for d_i, d in enumerate(data):

		if "city" in d:
			d.pop("city")
		if "StreetType" in d:
			d.pop("StreetType")
		if "StreetName" in d:
			d.pop("StreetName")
		if "postal_code" in d:
			d.pop("postal_code")
		if "housenumber" in d:
			d.pop("housenumber")
		if "HouseNumber" in d:
			d.pop("HouseNumber")
		if "PostalCode" in d:
			d.pop("PostalCode")
		if "address_additional_information" in d:
			d.pop("address_additional_information")
		if "address" in d:
			d.pop("address")
			# countAddress += 1
			# address = parse(d["address"], d["city"] if "city" in d else None)
			# # print("\t"+d["address"]+"\t"+str(address))
			# if address != None:
			# 	countValid += 1
			# 	for k in address.keys():
			# 		d[k] = address[k]
			# 	d.pop("address")
			# else:
			# 	d["address_additional_information"] = d.pop("address")
			
		newDataset["records"].append(d)
	# if countAddress > 0:
		# print("\t"+ str(countValid/countAddress*100)+"%" )
	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newDataset, file)