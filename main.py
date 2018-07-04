import urllib.request
import requests
from bs4 import BeautifulSoup
import socket
import cfscrape

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


print("Import done")
league_standings_url = "https://play.esea.net/index.php?s=league&d=standings&division_id=3122"
base_url = "https://play.esea.net"
team_urls = []
team_names = []

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(league_standings_url)

try:
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "league-standings")))
	print("done")

	league_standings = BeautifulSoup(driver.page_source, 'html.parser')
	table_rows = league_standings.find( "table").find('tbody').find_all("tr", {"class": ["row1", "row2"]})
	
	print (type(list(table_rows)))
	print (len(table_rows))

	for i in range(0, len(table_rows)):
		cells = table_rows[i].find_all("td")
		print(cells)
		anchors = cells[0].find_all("a")
		team_names.append(anchors[len(anchors) - 1].text)
		team_urls.append(base_url + str(anchors[len(anchors) - 1]['href']))
		print(anchors[len(anchors) - 1].text)
	print (team_names)
	print(len(team_names))
	print(len(team_urls))
	#print(anchors[len(anchors) - 1])
	#for row in table_rows:
	#	cells = row.find("td", {"class": "stat"})
	#	print(cells)

finally:
	driver.quit()




#scraper = cfscrape.create_scraper()
#print (type(scraper.get("https://play.esea.net/index.php?s=league&d=standings&division_id=3122").content))


'''league_standings_url = "https://play.esea.net/index.php?s=league&d=standings&division_id=3122"
timeout = 10
socket.setdefaulttimeout(timeout)

req = urllib.request.Request(
    league_standings_url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
try:
	league_standings = urllib.request.urlopen(req)
except urllib.error.URLError as e:
	print(e)'''
#print(league_standings)

