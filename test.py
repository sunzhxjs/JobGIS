#!/usr/bin/env python

import re, urlparse, csv, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from time import sleep

link = "https://www.linkedin.com/job/?trk=jobs-home-leo-redirect"
#link_glassdoor = "https://www.glassdoor.com/Job/index.htm"
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)
driver = webdriver.PhantomJS(desired_capabilities=dcap)

languageList = ['JAVA','C/C++ engineer','Javascript','Python','PHP','C#/Net','Ruby','Object-C','Perl','R language']

with open('./us_state.json') as sf:
	states = json.load(sf)
sf.close()
with open('./amount.csv','w') as sfw:
    writer=csv.DictWriter(sfw, fieldnames=['state']+languageList)
    writer.writeheader()
    for i in range(len(states['features'])):
		state=states['features'][i]['properties']['name']
		state_ls = {'state':state}
		for l in languageList:
			driver.get(link)
			#print driver.page_source
			keyword = driver.find_element_by_id("field-keyword-name")
			keyword.send_keys(l)
			location = driver.find_element_by_id("field-location-name")	
			location.send_keys(state)
			location.submit()
			try:
				element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "results-context")))
			except Exception as e:
				print type(e)
				state_ls[l]=0
			else:
				pageSource = driver.page_source
				bsObj = BeautifulSoup(pageSource,"html.parser")
				print((bsObj.find(class_="results-context").get_text().split(' '))[0]+" jobs in "+state)
				state_ls[l]=int(bsObj.find(class_="results-context").get_text().split(' ')[0].replace(',',''))
		writer.writerow(state_ls);		

with open('./static/us_city_for_python.csv') as cf:
	cities = csv.DictReader(cf)

	with open('./amount_city.csv','w') as cfw:
		writer=csv.DictWriter(cfw, fieldnames=['city']+languageList)
		writer.writeheader()
		for row in cities:
			city=row['Place']
			city_ls = {'city':city}
			for l in languageList:
				driver.get(link)
				keyword = driver.find_element_by_id("field-keyword-name")
				keyword.send_keys(l)
				location = driver.find_element_by_id("field-location-name")	
				location.send_keys(city)
				location.submit()
				try:
					element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "results-context")))
				except Exception as e:
					print type(e)	
				else:
					pageSource = driver.page_source
					bsObj = BeautifulSoup(pageSource,"html.parser")
					print((bsObj.find(class_="results-context").get_text().split(' '))[0]+" jobs in "+city)
					city_ls[l]=int(bsObj.find(class_="results-context").get_text().split(' ')[0].replace(',',''))
			writer.writerow(city_ls);

driver.close();












