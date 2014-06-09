import requests
from bs4 import BeautifulSoup
import json
import time
import re

base_url = "http://www.mallsinfo.com"
all_malls_url ="http://www.mallsinfo.com/all-malls"
malls_data_dict_list = [] #List of all the dictionaries of malls. One "mall dictionary" contains info about one mall

#Regular Expression Code to find the Longitude and Latitude in the html document
re1='(LatLng)'	# Word 1
re2='.*?'	# Non-greedy match on filler
re3='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 1
re4='.*?'	# Non-greedy match on filler
re5='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 2
rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)


def get_malls_urls():

	# Downloaded the source of the page all-malls.htm from "http://www.mallsinfo.com/all-malls".
	# It contains a list of all the malls with a link to the mall detailed page -page that gives detailed 
	# info about the mall, mainly its stores.
	html = open('all-malls.htm','r')
	soup = BeautifulSoup(html)
	mall_urls = [a.attrs.get('href') for a in soup.select('.mylinks a')]
	mallsfile = open('mall_urls.txt','w')
	for url in mall_urls:
		mallsfile.write(url+'\n')
	mallsfile.close()
	return mall_urls



def get_malls_data(mall_url):

	
	malls_data = {} #"mall dictionary"
	response = requests.get(base_url + mall_url)
	soup = BeautifulSoup(response.text)
	m = rg.search(response.text)
	# statehtml = soup.select('dd:nth-of-type(3)')
	# (statehtml[0]) returns an element of type Tag, therefore in order to get the text, I use the get_text() method of Tag elements. Therefore, in
	# one line the code becomes: (soup.select("div.product-price span"))[0].get_text().
	malls_data['mall_name'] = (soup.select("div.product-price span"))[0].get_text()
	malls_data['mall_state'] = (soup.select('dd:nth-of-type(3)'))[0].get_text()
	malls_data['mall_address'] = (soup.select('dd:nth-of-type(1)'))[0].get_text()
	malls_data['mall_phone'] = (soup.select('dd:nth-of-type(2)'))[0].get_text()
	if m:
		malls_data['mall_latitude'] = m.group(2)
		malls_data['mall_longitude'] = m.group(3)
	else:
		malls_data['mall_latitude'] = ''
		malls_data['mall_longitude'] = ''

	malls_data['mall_number_of_stores'] = (soup.select('dd:nth-of-type(4)'))[0].get_text()
	malls_data['mall_stores_list'] = [a.get_text() for a in soup.select('#stores a')]

	malls_data_dict_list.append(malls_data) #add each "mall dictionary to the List, this is to avoid problem when dumping/load the data in JSON"

	return malls_data





mallsfile = open('mall_urls.txt', 'r')

mallsdatafile = open("mallsdata.txt","a")



for url in mallsfile:
	print get_malls_data(url.strip("\n"))
	time.sleep(2) #Delay of 5 seconds between requests

json.dump(malls_data_dict_list, mallsdatafile) #dump the data in JSON format.

mallsdatafile.close()

mallsfile.close()