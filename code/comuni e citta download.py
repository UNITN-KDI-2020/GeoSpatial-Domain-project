# Script to scrape comunecittá.it

from os import path
import time
from sys import argv

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

DEST_FOLDER = argv[1] if len(
	argv) > 1 else "./dataset/Data Integration/data/scuole/superiori.csv"

driver = webdriver.Chrome(
	"C:/Users/Michele/Downloads/chromedriver_win32/chromedriver.exe")
driver2 = webdriver.Chrome(
	"C:/Users/Michele/Downloads/chromedriver_win32/chromedriver.exe")
driver.get(
	'https://www.comuniecitta.it/scuole-secondarie-di-secondo-grado/comune-di-trento-22205')

content = driver.page_source
soup = BeautifulSoup(content)

linkArray = [''] * 15
name = []
address = []
schoolType = []
studyPath = []

def addStudyPath(link):
	studyPath.append('')
	length = len(studyPath)
	driver2.get('https://www.comuniecitta.it' + link)
	content2 = driver2.page_source
	soup = BeautifulSoup(content2)
	studyPaths = soup.find('span', attrs={'class': 'linea'})
	if hasattr(studyPaths, 'text'):
		for br in studyPaths.find_all("br"):
			br.replace_with(",")
		if hasattr(studyPaths, 'text'):
			studyPath[length-1] = studyPaths.text
		

for a in soup.findAll('tbody'):
	td = a.findAll('td')
	for i, r in enumerate(td):
		if i % 4 == 0:
			link = r.find('a', href=True)
			if hasattr(link, 'text'):
				name.append(link.text)
				addStudyPath(link['href'])
		elif i % 4 == 1 and len(address) < 15:
			address.append(r.text)
		elif i % 4 == 3:
			schoolType.append(r.text)

print(studyPath)

df = pd.DataFrame({'name': name, 'address': address,
                   'school type': schoolType, 'study paths': studyPath})
df.to_csv(DEST_FOLDER, index=False, encoding='utf-8', sep=';')
driver.quit()
driver2.quit()