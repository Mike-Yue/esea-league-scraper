from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

league_standings_url = "https://play.esea.net/index.php?s=league&d=standings&division_id=3121"
base_url = "https://play.esea.net"
team_urls = []
team_names = []
team_scores_and_names_dict = {}
team_stats_list = []
unupdated_team_list = []


if __name__ == '__main__':
	print("Import done")
	counter = 0
	driver = webdriver.Chrome()
	driver.implicitly_wait(30)
	driver.get(league_standings_url)


	#########################################################################################################
	#  Opens the league standings page and gets all the team names and their URLs and puts them into lists  #
	#  Modifies: team_names, team_urls                                                                      #
	#########################################################################################################
	try:
		element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "league-standings")))
		print("done")

		league_standings = BeautifulSoup(driver.page_source, 'html.parser')
		table_rows = league_standings.find("table").find('tbody').find_all("tr", {"class": ["row1", "row2"]})
		
		print (len(table_rows))

		for i in range(0, len(table_rows)):
			cells = table_rows[i].find_all("td")
			anchors = cells[0].find_all("a")
			team_names.append(anchors[len(anchors) - 1].text)
			team_urls.append(base_url + str(anchors[len(anchors) - 1]['href']))

		button = driver.find_element_by_class_name("accept")
		button.click()

		for name in team_names:
			if(name == "DuSt  Gaming"):
				name = "DuSt Gaming"
			if(name == "Erupt  eSports"):
				name = "Erupt eSports"
			link = driver.find_element_by_link_text(name)
			link.location_once_scrolled_into_view
			link.click()
			try:
				element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "profile-header")))

				team_stats = [0, 0, 0, 0, '']

				team_page = BeautifulSoup(driver.page_source, "html.parser")
				team_name = team_page.find('h1').text
				print(team_name)
				team_stats[4] = team_name
				table_rows = team_page.find("table").find('tbody').find_all("tr")
				skip_first = 0
				
				for row in table_rows:
					if(skip_first == 0):
						skip_first = 1
					else:
						cells = row.find_all("td")
						if(len(cells) == 7):
							if(cells[4].find('a') == None):
								break
							if(cells[4].find('a').text == 'Win'):
								#Adds a win and 16 rounds to the team_stats
								team_stats[0] = team_stats[0] + 1
								team_stats[2] = team_stats[2] + 16

								score_breakdown = cells[5].find('a').text.split('-')
								if(int(score_breakdown[0]) < int(score_breakdown[1])):
									if(int(score_breakdown[0]) > 14):
										team_stats[3] = team_stats[3] + 15
									else:
										team_stats[3] = team_stats[3] +int(score_breakdown[0])
								else:
									if(int(score_breakdown[1]) > 14):
										team_stats[3] = team_stats[3] + 15
									else:
										team_stats[3] = team_stats[3] + int(score_breakdown[1])
							elif(cells[4].find('a').text == 'Tie'):
								pass
							else:
								team_stats[1] = team_stats[1] + 1
								team_stats[3] = team_stats[3] + 16

								score_breakdown = cells[5].find('a').text.split('-')
								if(int(score_breakdown[0]) < int(score_breakdown[1])):
									if(int(score_breakdown[0]) > 14):
										team_stats[2] = team_stats[2] + 15
									else:
										team_stats[2] = team_stats[2] + int(score_breakdown[0])
								else:
									if(int(score_breakdown[1]) > 14):
										team_stats[2] = team_stats[2] + 15
									else:
										team_stats[2] = team_stats[2] + int(score_breakdown[1])

						else:
							break

				print(team_stats)
				team_stats_list.append(team_stats)
				counter = counter + 1
				print(counter)

				driver.back()
				time.sleep(3)
			except TimeoutException as ex:
				print(ex)
				unupdated_team_list.append(name)
	finally:
		driver.quit()

	print("Teams which timed out")
	print(unupdated_team_list)

	for i in range(0, len(team_stats_list)):
		for j in range(i+1, len(team_stats_list)):
			if(team_stats_list[i][0] < team_stats_list[j][0]):
				team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
			elif(team_stats_list[i][0] == team_stats_list[j][0]):
				if(team_stats_list[i][1] > team_stats_list[j][1]):
					team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
				elif(team_stats_list[i][1] == team_stats_list[j][1]):
					if(team_stats_list[i][2] < team_stats_list[j][2]):
						team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
					elif(team_stats_list[i][2] == team_stats_list[j][2]):
						if(team_stats_list[i][3] > team_stats_list[j][3]):
							team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]


	#Prints sorted team list
	print(team_stats_list)

	counter = 1
	seeded_against = 63
	with open('IM_rankings.csv', 'w', newline = '') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['Team Ranking', 'Team Name', 'Games Won', 'Games Lost', 'Rounds Won', 'Rounds Against', 'Playing Against Seed'])
		for item in team_stats_list:
			if(seeded_against < 0):
				writer.writerow([counter, item[4], item[0], item[1], item[2], item[3]])
				counter = counter + 1
			else:
				writer.writerow([counter, item[4], item[0], item[1], item[2], item[3], team_stats_list[seeded_against][4]])
				counter = counter + 1
				seeded_against = seeded_against - 1

	'''for url in team_urls:
		driver = webdriver.Chrome()
		driver.implicitly_wait(30)
		driver.get(url)

		try:
			element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "profile-header")))

			#######################################
			#  team_stats[0]: number of wins      #
			#  team_stats[1]: number of losses    #
			#  team_stats[2]: rounds won          # 
			#  team_stats[3]: rounds lost         # 
			#######################################
			team_stats = [0, 0, 0, 0, '']

			team_page = BeautifulSoup(driver.page_source, "html.parser")
			team_name = team_page.find('h1').text
			print(team_name)
			team_stats[4] = team_name
			table_rows = team_page.find("table").find('tbody').find_all("tr")
			skip_first = 0
			
			for row in table_rows:
				if(skip_first == 0):
					skip_first = 1
				else:
					cells = row.find_all("td")
					if(len(cells) == 7):
						if(cells[4].find('a') == None):
							break
						if(cells[4].find('a').text == 'Win'):
							#Adds a win and 16 rounds to the team_stats
							team_stats[0] = team_stats[0] + 1
							team_stats[2] = team_stats[2] + 16

							score_breakdown = cells[5].find('a').text.split('-')
							if(int(score_breakdown[0]) < int(score_breakdown[1])):
								if(int(score_breakdown[0]) > 14):
									team_stats[3] = team_stats[3] + 15
								else:
									team_stats[3] = team_stats[3] +int(score_breakdown[0])
							else:
								if(int(score_breakdown[1]) > 14):
									team_stats[3] = team_stats[3] + 15
								else:
									team_stats[3] = team_stats[3] + int(score_breakdown[1])
						elif(cells[4].find('a').text == 'Tie'):
							pass
						else:
							team_stats[1] = team_stats[1] + 1
							team_stats[3] = team_stats[3] + 16

							score_breakdown = cells[5].find('a').text.split('-')
							if(int(score_breakdown[0]) < int(score_breakdown[1])):
								if(int(score_breakdown[0]) > 14):
									team_stats[2] = team_stats[2] + 15
								else:
									team_stats[2] = team_stats[2] + int(score_breakdown[0])
							else:
								if(int(score_breakdown[1]) > 14):
									team_stats[2] = team_stats[2] + 15
								else:
									team_stats[2] = team_stats[2] + int(score_breakdown[1])

					else:
						break

			print(team_stats)
			team_stats_list.append(team_stats)
			counter = counter + 1
			print(counter)

		finally:
			driver.back()

	#Prints unsorted team list
	print(team_stats_list)
	print('\n\n')

	#Selection Sort on the list
	for i in range(0, len(team_stats_list)):
		for j in range(i+1, len(team_stats_list)):
			if(team_stats_list[i][0] < team_stats_list[j][0]):
				team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
			elif(team_stats_list[i][0] == team_stats_list[j][0]):
				if(team_stats_list[i][1] > team_stats_list[j][1]):
					team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
				elif(team_stats_list[i][1] == team_stats_list[j][1]):
					if(team_stats_list[i][2] < team_stats_list[j][2]):
						team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]
					elif(team_stats_list[i][2] == team_stats_list[j][2]):
						if(team_stats_list[i][3] > team_stats_list[j][3]):
							team_stats_list[i], team_stats_list[j] = team_stats_list[j], team_stats_list[i]


	#Prints sorted team list
	print(team_stats_list)

	counter = 1
	seeded_against = 63
	with open('IM_rankings.csv', 'w', newline = '') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['Team Ranking', 'Team Name', 'Games Won', 'Games Lost', 'Rounds Won', 'Rounds Against', 'Playing Against Seed'])
		for item in team_stats_list:
			if(seeded_against < 0):
				writer.writerow([counter, item[4], item[0], item[1], item[2], item[3]])
				counter = counter + 1
			else:
				writer.writerow([counter, item[4], item[0], item[1], item[2], item[3], team_stats_list[seeded_against][4]])
				counter = counter + 1
				seeded_against = seeded_against - 1'''