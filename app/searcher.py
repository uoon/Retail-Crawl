import time
import rauth
import csv
import os

name = ''
names = ["Ko' Sin",
"El Zocalo Mexican Grill",
"Spinato's Pizza",
"Caffe Boa",
"The Normal Diner",
"Cafe Lalibela",
"Ted's Hot Dogs",
"Market Cafe",
"Curry Corner",
"Kings Fish House",
"Sweet Tomatoes",
"Thai Basil",
"Casey Moore's Oyster House",
"Texas Roadhouse",
"Mijana Restaurant",
"Genghis Grill",
"Denny's",
"Joe's Crab Shack",
"Mission Grille",
"LA Fonda Mexican Foods",
"El Ranchero Mexican Grill",
"Aj's Fine Foods",
"The Living Room",
"Benihana",
"Taste - An American Bistro",
"Fatburger",
"Chili's Grill & Bar",
"U.S Egg",
"Moreno's",
"Barro's Pizza",
"Freddy's Frozen Custard & Steakburgers",
"Jimmy John's",
"Los Favoritos Taco Shop",
"Red Robin Gourmet Burgers",
"Turkdish Mediterranean Cuisine",
"La Famiglia Pizza & Pasta",
"Hot Pot Caribbean Cuisine",
"Ocean Blue Caribbean Restaurant and Bar",
"Biscuits Cafe",
"AZ Food Crafters",
"Grimaldis Pizzeria",
"Amalfi Pizzeria",
"Famous Dave's",
"Mimi's Cafe",
"Elmer's Tacos",
"Hangar Cafe",
"Chodong",
"Saigon Pho",
"Don Shula's",
"YC's Mongolian Grill",
"TOTT's Asian Diner",
"Fringo's Kitchen",
"Talebu Coffee and Wine Cafe",
"Good Time Charlie's Neighborhood Craft Pub",
"Charm Thai Cuisine",
"NYPD Pizza",
"Teakwoods Tavern & Grille",
"Cafe Cornucopia",
"Beijing",
"Rumbi Island Grill",
"Sidelines Tavern and Grill",
"Rubio's",
"Szechwan Garden",
"Blooming Beets Kitchen",
"East Wind",
"Crisp Greens",
"Yangtse Chinese Bistro",
"Munchies",
"Juan Jaime's Tacos and Tequila",
"Food City",
"Opa Life Greek Cafe",
"Phoenicia Cafe",
"Boulders on Broadway"]
result = []

def get_search_parameters(name):
	#set the parameters for yelp API
	params = {}
	params["term"] = str(name)
	params["sort"] = "0"
	params["radius.filter"] = "2000"
	params["limit"] = "1" #returning top #1 search
	params["location"] = "Chandler, AZ"
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
		return key[u'phone']
	except KeyError:
		print key[u'name'], "needs manual phone number verification"
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



