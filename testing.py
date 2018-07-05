import urllib.request
import requests
from bs4 import BeautifulSoup
import socket
import cfscrape
from multiprocessing import Pool, Queue, Manager, Process
from multiprocessing import freeze_support
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import sys
import csv

team_scores_and_names_dict = {}

team_scores_and_names_dict['1'] = "watashiwa"
team_scores_and_names_dict['2'] = 'sadasdasd'
with open('test.csv', 'w', newline = '') as csv_file:
	writer = csv.writer(csv_file)
	for key in list(team_scores_and_names_dict.keys()):
		writer.writerow([key, team_scores_and_names_dict.get(key)])
