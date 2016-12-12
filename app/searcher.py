import time
import rauth
import csv
import os

name = ''
names = ['the harp', 'subway', 'btz sports bar', 'smashburger', 'postino']

def get_search_parameters(name):
	#set the parameters for yelp API
	params = {}
	params["term"] = str(name)
	params["sort"] = "0"
	params["radius.filter"] = "2000"
	params["limit"] = "2" #returning top 2 searches
	params["location"] = "Gilbert, AZ"
	return params
	
def get_results(params):
	consumer_key = "XwD3f3Yoe2GcjqXSd5kRkA"
	consumer_secret = "VtZMCNmBNEardBkIXo-RU7De-wU"
	token = "JymbFW3SgkWemf6aTEHUvsNoPg9Nh7hZ"
	token_secret = "S4XUSKiIcUCYnlC3q7FYgUC47co"
	
	session = rauth.OAuth1Session(consumer_key = consumer_key
	,consumer_secret = consumer_secret
	,access_token = token
	,access_token_secret = token_secret)
	
	request = session.get("http://api.yelp.com/v2/search",params=params)
	
	data = request.json()
	session.close()
	
	return data

def main():
	api_calls = [] #results of data is to be added to api_calls
	params = get_search_parameters(name)
	api_calls.append(get_results(params))
	time.sleep(1.0)
	return api_calls #returns the API call
	
def get_business_info(): #I can probably move this to main(), but i am keeping it separated for debugging sake
	business_info = []
	for key in main()[0]['businesses']:
		business_info.append("%s, %s, %s, %s" %(key[u'name'], key[u'phone'], key[u'rating'], key[u'review_count']))
		#Need to change the way business_info saves to the list so that I can separate into columns with writer.
	return business_info

def writer():
	#writes to csv file. '\n' is a row break. I should write a for loop for 
	#multiple API calls, and include '\n' after each loop.
	#Also, I may want to figure out how to separate values to columns.
	with open('yelp test.csv', 'ab') as csvfile:
		resultwriter = csv.writer(csvfile)
		for business in get_business_info():
			resultwriter.writerow([business])

def multi_write(names):
	for i in names:
		global name
		name = i
		writer()
	
		
def start():
	if raw_input("Ready to start? Reply 'yes' or 'no' without the quotations>> ") == 'yes':
		multi_write(names)
	else: 
		exit()
	
start()