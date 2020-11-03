# Script to download all the openData Trentino common interest locations of the town

from lxml import html
import requests
from os import path
import time
from sys import argv
import json

REQUEST_DELAY = 1.5  # Delay in seconds to delay between downloads, preventing the crashing of opendata Trentino website
OUT_FOLDER = "./dataset/Informal Modeling/metadata/"


def exist(name):
	return path.exists(name + ".json") and path.exists(name + " GEO.json") and path.exists(name + " CLASSES.json")


def extractData(page, name):
	tree = html.fromstring(page.content)

	pageHrefs = tree.xpath('//a[@class="resource-url-analytics"]')
	if len(pageHrefs) < 1:
		print("--- Links not found, is OpenData Trentino crashed? ---")

		for l in pageHrefs:
			link = l.attrib['href']
			if "v2/content" in link and not path.exists(name + ".json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(OUT_FOLDER + name + '.json', 'w') as file:
						file.write(r.text)
				except:
					print(name + ": Error during the download of DATA")
			if "v2/geo" in link and not path.exists(name + " GEO.json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(OUT_FOLDER + name + ' GEO.json', 'w') as file:
						file.write(r.text)
				except:
					print(name + ": Error during the download of DATA GEO")
			if "v2/classes" in link and not path.exists(name + " CLASSES.json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(OUT_FOLDER + name + ' CLASSES.json', 'w') as file:
						file.write(r.text)
				except:
					print(name + ": Error during the download of METADATA")


def extractMetadata(page, url):
	tree = html.fromstring(page.content)
	rows = tree.xpath('//section[@class="additional-info"]')
	rows = rows[0].xpath('table/tbody/tr')
	metadatas = {
		"source": url,
		"format": "json",
		"fields": {
			"id": {
				"type": "string",
				"description": ""
			},
			"name": {
				"type": "string",
				"description": ""
			},
			"geo": {
				"type": "string",
				"description": ""
			},
			"geometry": {
				"type": "map",
                            "description": "geometrical features",
                            "fields": {
                    "type": {
						"type": "string",
						"description": "type of geometry"
					},
                    "coordinates": {
						"type": "array",
						"description": "array the points which compose the polygon"
					}
                }
			}
		}
	}
	for i, r in enumerate(rows):
		fieldName = r.xpath('th')[0].text
		fieldValue = r.xpath('td')[0].text
		if fieldValue == None:
			metadatas[fieldName] = str(r.xpath('td/a')[0].attrib['href'])
		elif len(fieldValue.strip()) < 1:
			spans = r.xpath('td/span')
			if len(spans) > 2:
				metadatas[fieldName] = {}
				for i2, subr in enumerate(spans):
					if i2 % 2 == 0:
						metadatas[fieldName][subr.text] = spans[i2 + 1].text
			else:
				metadatas[fieldName] = ""
				for subr in spans:
					metadatas[fieldName] += subr.text
		else:
			metadatas[fieldName] = fieldValue.strip()
	return metadatas


def tryGet(url):
	status = False
	page = requests.get(url)
	if page.status_code == 503:
			print("--- OpenData Trentino crashed, attempting a new request... ---")
			time.sleep(REQUEST_DELAY)
	else:
		status = True
	while(not status):
		page = requests.get(url)
		if page.status_code == 503:
			print("--- OpenData Trentino crashed, attempting a new request... ---")
			time.sleep(REQUEST_DELAY)
		else:
			status = True
	return page


metadatas = {}
for i in range(1, 9):
	print("page: " + str(i))
	url = 'https://dati.trentino.it/dataset?tags=luoghi+e+punti+di+interesse&page=' + str(i)
	page = tryGet(url)
	tree = html.fromstring(page.content)

	hrefs = tree.xpath(
		'//a[contains(text(),"Luoghi") and contains(text(),"interesse")]')
	if len(hrefs) < 1:
		print("--- Links not found, is OpenData Trentino crashed? ---")

	for l in hrefs:
		name = l.text[32:]
		print(name)
		if exist(name):
			continue

		time.sleep(REQUEST_DELAY)
		url = 'https://dati.trentino.it' + l.attrib['href']
		page = tryGet(url)

		# extractData(page, name)

		metadatas[name] = extractMetadata(page, url)

# print(metadatas)
with open(OUT_FOLDER + "luoghi_e_punti_di_interesse_per_comune_METADATA.json", 'w+') as file:
	json.dump(metadatas, file)
