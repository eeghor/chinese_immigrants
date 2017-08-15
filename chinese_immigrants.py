
#import selenium
import string
import itertools
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
from random import randint
import time
# from selenium.webdriver.common.keys import Keys
# import time
# import sys
# import pandas as pd
# from collections import namedtuple

collected_names = set()

def get_names_from_page():

	names_on_this_page = set()

	result_table = driver.find_element_by_xpath("//table[@id='result_table']")
	# look at each table row
	for tr in result_table.find_elements_by_xpath("//tr"):
		for i, td in enumerate(tr.find_elements_by_xpath("./td")):
			# grab the name from there
			if i == 1:
				name = td.text.strip().lower()
				names_on_this_page.add(name)
				continue
	return names_on_this_page 

def another_page():

	try:
		driver.find_element_by_id("nextPage")
		another_page_flag = True
	except NoSuchElementException:
		another_page_flag = False

	return another_page_flag

# full path to the webdriver to use; use webdriver.PhantomJS() for invisible browsing
driver = webdriver.Chrome('/Users/ik/Codes/chinese_immigrants/webdriver/chromedriver')

WAIT_TIME = 30
# base URL
DB_SEARCH_URL = "http://www.bac-lac.gc.ca/eng/discover/immigration/immigration-records/immigrants-china-1885-1949/Pages/search.aspx"

for pair in itertools.product(string.ascii_lowercase, repeat=2):   # 'abcdefghijklmnopqrstuvwxyz'
	
	# page to go to first
	driver.get(DB_SEARCH_URL)

	# find the name input
	enter_name_input = driver.find_element_by_xpath("//input[contains(@title,'Enter') and contains(@title, 'Name')]")
	enter_name_input.clear()
	enter_name_input.send_keys("".join(pair) + "*")
	# find and click the search button
	driver.find_element_by_xpath("//input[@type='submit']").click()
	# wait until the results show up
	how_many_found = WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CLASS_NAME, "search_term_value")))
	
	try:
		nresults = int(how_many_found.text.strip().split()[0])
		if nresults > 0:
			print("search results: {}".format(nresults))
		else:
			print("found nothing, moving on...")
			continue
	except:

		print("ERROR: didn\'t get any search results at all. exiting..")
		sys.exit(0)
	
	collected_names.update(get_names_from_page())
	# see if there's another page

	while another_page():

		driver.find_element_by_id("nextPage").click()
		WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "previousPage")))
		collected_names.update(get_names_from_page())

	time.sleep(randint(1,5))
	continue  # move on to the next letter triple

# save the collected names to a file
with open("chinese_immigrant_names.txt", "w") as f:
	for name in collected_names:
		f.write("{}\n".format(name))
print("collected a list of {} unique names".format(len(collected_names)))
	
	
	