import time
import rauth
import csv
import os

name = ''
names = ["Monarch",
"Butterfields Pancake House",
"Virtu",
"Eddie V\'s Prime Seafood",
"Fogo de Chao Brazilian Steakhouse",
"Butters Pancakes & Cafe",
"deseo at Westin Kierland Resort and Spa",
"Grassroots kitchen and Tap",
"Rehab Burger Therapy",
"Roaring Fork",
"True Food Kitchen",
"Bandera",
"Franco\'s Italian Caffe",
"Mastro\'s City Hall",
"Citizen Public House",
"Coconut\'s Fish Cafe",
"Olive & Ivy"]
result = []

def get_search_parameters(name):
	#set the parameters for yelp API
	params = {}
	params["term"] = str(name)
	params["sort"] = "0"
	params["radius.filter"] = "2000"
	params["limit"] = "1" #returning top #1 search
	params["location"] = "Scottsdale, AZ"
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

def phone_key_finder(key):
  try:
    phonenum = key[u'phone']
    format_phonenum = '(' + phonenum[0:3] + ') ' + phonenum[3:6] + '-' + phonenum[6:]
    return format_phonenum
  except KeyError:
    print [u'name'], "needs manual phone number verification."
    return "Manual Input"
	
def get_business_info(): #I can probably move this to main(), but i am keeping it separated for debugging sake
  for key in main()[0]['businesses']:
    info_results = [key[u'name'], phone_key_finder(key), key[u'rating'], key[u'review_count']]
    global result
    result.append(info_results)
    print "'%s' added to the documentation file." %key[u'name']

def writer():
  #writes to csv file. '\n' is a row break. I should write a for loop for
  #multiple API calls, and include '\n' after each loop.
  #Also, I may want to figure out how to separate values to columns.
  with open('yelp test.csv', 'ab') as csvfile:
		resultwriter = csv.writer(csvfile)
		for business in result:
		  resultwriter.writerow([business[0].encode('utf-8'), business[1], business[2], business[3]])
  print "Writing to CSV file complete."

def multi_write(names):
	for i in names:
		global name
		name = i
		get_business_info()
	print result
	print "Would you like to write the above businesses to the document?"
	print "'yes' to proceed"
	if raw_input("> ") == 'yes':
		return writer()
	else:
		print "Exiting the program."
		exit()
		
def start():
  print "Running yelp scanner for %s" %names
  if raw_input("Ready to start? Reply 'yes' or 'no' without the quotations. ") == 'yes':
    return multi_write(names)
  else: 
    exit()
	
start()



