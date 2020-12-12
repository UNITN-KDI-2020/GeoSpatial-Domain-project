import json
import re
from os import path, listdir
# from address import AddressParser, Address
import warnings
warnings.filterwarnings("ignore", category=Warning)

# address = ap.parse_address('123 West Mifflin Street, Madison, WI, 53703')
# print "Address is: {0} {1} {2} {3}".format(address.house_number, address.street_prefix, address.street, address.street_suffix)

exceptions = ["buildings.json", "trails.json", "civici_web.json"]

file_comuni = open("./code/italia_comuni.json", "r")
regioni = json.load(file_comuni)["regioni"]
trentino = [x for x in regioni if x["nome"] == "Trentino-Alto Adige"][0]
comuni = [x["nome"] for x in trentino["province"][0]["comuni"]]
comuni.extend([x["nome"] for x in trentino["province"][1]["comuni"]])

# ap = AddressParser(cities=comuni)

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

def parse(address):
	out = {}
	prefixes = ["via", "piazza", "corso", "piaz", "strada provinciale", "strada", "vicolo", "cort", "cianton", "localita'", "viale", "piazzale", "p.za", "p.le", "c.so", "porta", "largo", "piaza", "piazzetta"]
	res, city = extractCity(address)
	if res:
		out["city"] = city
		address = address.replace(city, "")
	subaddr = re.split("[,;-]+", address)
	searchForStreet = -1
	street = ""
	for a_i, addr in enumerate(subaddr):
		splittedAddr = addr.split()
		for w_i, word in enumerate(splittedAddr):
			if word.lower() in prefixes:
				out["StreetType"] = word
				if w_i == 0 and a_i == 0:
					searchForStreet = a_i
			elif RepresentsInt(word):
				if len(word) > 3:
					out["postal_code"] = word
				else:
					out["HouseNumber"] = word
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

# print(parse("Via Antonio Stoppani"))

for count, filename in enumerate(listdir(IN_FOLDER)):
	if not ".json" in filename or filename in exceptions:
		continue

	print(filename)
	dataset = open(IN_FOLDER + filename, "r")
	data = json.load(dataset)
	if "records" in data:
		data = data["records"]

	newDataset = {"records": []}

	for d_i, d in enumerate(data):

		if "address" in d:
			countAddress += 1
			# address = ap.parse_address(d["address"])
			# if not "postal_code" in d and address.zip
			address = parse(d["address"])
			if address != None:
				countValid += 1
				for k in address.keys():
					d[k] = address[k]
			# 	print("\t"+d["address"]+"\t"+str(address))
			# else:
			# 	print("\t"+d["address"])
			
			
		newDataset["records"].append(d)
	
	# print()
	with open(OUT_FOLDER + filename, 'w+') as file:
		json.dump(newDataset, file)