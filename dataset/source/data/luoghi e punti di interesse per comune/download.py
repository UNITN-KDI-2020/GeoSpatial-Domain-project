from lxml import html
import requests
from os import path
import time

# Script to download all the openData Trentino common interest locations of the town

REQUEST_DELAY = 1 # Delay in seconds to delay between downloads, preventing the crashing of opendata Trentino website

def exist(name):
	return path.exists(name+".json") and path.exists(name+" GEO.json") and path.exists(name+" CLASSES.json")

for i in range(1,9):
	print("page: "+str(i))
	page = requests.get('https://dati.trentino.it/dataset?tags=luoghi+e+punti+di+interesse&page='+str(i))
	tree = html.fromstring(page.content)

	hrefs = tree.xpath('//a[contains(text(),"Luoghi") and contains(text(),"interesse")]')
	if len(hrefs) < 1:
		print("--- Links not found, is OpenData Trentino crashed? ---")

	for l in hrefs:
		name = l.text[32:]
		print(name)
		if exist(name):
			continue
		
		time.sleep(REQUEST_DELAY)
		page = requests.get('https://dati.trentino.it'+l.attrib['href'])
		tree = html.fromstring(page.content)

		pageHrefs = tree.xpath('//a[@class="resource-url-analytics"]')
		if len(pageHrefs) < 1:
			print("--- Links not found, is OpenData Trentino crashed? ---")

		for l in pageHrefs:
			link = l.attrib['href']
			if "v2/content" in link and not path.exists(name+".json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(name+'.json', 'w') as file:
						file.write(r.text)
				except:
					print(name+": Error during the download of DATA")
			if "v2/geo" in link and not path.exists(name+" GEO.json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(name+' GEO.json', 'w') as file:
						file.write(r.text)
				except:
					print(name+": Error during the download of DATA GEO")
			if "v2/classes" in link and not path.exists(name+" CLASSES.json"):
				try:
					time.sleep(REQUEST_DELAY)
					r = requests.get(link)
					with open(name+' CLASSES.json', 'w') as file:
						file.write(r.text)
				except:
					print(name+": Error during the download of METADATA")