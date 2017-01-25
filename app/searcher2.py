import time
import rauth
import csv
import os

class RestaurantNames(object):
	"""extract restaurant names from a csv file"""
	def __init__(self):
		self.names = []
	def read_csv(self, filename):
		"""will have to call 
		RestaurantNames.read_csv('c:/.../csvfilename.csv')"""
		with open(filename, 'r') as f:
			read = f.read()
			self.names = [x for x in read.split('\n') if x]
		return self.names


class APICrawler(object):
	def __init__(self, names):
		"""takes names from RestaurantNames class"""
		self.names = names
		self.results = []

	def get_search_parameters(self, name):
		"""set the parameters for yelp API"""
		params = {}
		params["term"] = str(name)
		params["sort"] = "0"
		params["radius.filter"] = "2000"
		params["limit"] = "1" #return the first search item
		params["location"] = "Mesa, AZ"
		return params
	
	def api_connect(self, params):
		"""API keys, session authentication"""
		consumer_key = "XwD3f3Yoe2GcjqXSd5kRkA"
		consumer_secret = "VtZMCNmBNEardBkIXo-RU7De-wU"
		token = "JymbFW3SgkWemf6aTEHUvsNoPg9Nh7hZ"
		token_secret = "S4XUSKiIcUCYnlC3q7FYgUC47co"
		
		session = rauth.OAuth1Session(consumer_key = consumer_key,
		consumer_secret = consumer_secret,
		access_token = token,
		access_token_secret = token_secret,
		)
		
		request = session.get("http://api.yelp.com/v2/search",params=params)
		
		data = request.json()
		session.close()
		
		return data

	def main(self, name):
		"""bridge the connection between Yelp API, get_results and 
		get_search_parameters functions. Returns one result at a 
		time since we are expecting top result per name searched"""
		api_results = [] 
		params = self.get_search_parameters(name)
		api_results.append(self.api_connect(params))
		time.sleep(1.0)
		key = api_results[0]['business']
		business_information = [key[u'name'], self.phone_number_organizer(key), key[u'rating'],\
		key[u'review_count']]
		return business_information

	def phone_number_organizer(self, key):
		"""phone numbers should be correctly formatted, and some 
		searches were returning errors from missing numbers"""
		try:
			phone_number = key[u'phone']
			format_number = '(' + phonenum[0:3] + ') ' + phonenum[3:6] + '-' + phonenum[6:]
			return format_number
		except KeyError:
			print [u'name'], "requires manual phone number verification."
			return "Manual Input"	

	def results_aggregator(self, names):
		"""iterate through each restaurant name from restaurant names
		and aggregate to results"""
		for name in names:
			result = self.main(name)
			self.results.append(result)
			print("'%s' has been written to the file." % result[u'name'])

	def results_writer(self):
	  #writes to csv file. '\n' is a row break. I should write a for loop for
	  #multiple API calls, and include '\n' after each loop.
	  #Also, I may want to figure out how to separate values to columns.
		with open('yelp test.csv', 'w') as csvfile:
			resultwriter = csv.writer(csvfile)
			for business in self.results:
				resultwriter.writerow([business[0].encode('utf-8'), business[1], business[2], business[3]])
		print("Writing to CSV file complete.")

f = RestaurantNames()
#names = f.read_csv(input("> Indicate path and filename of restaurant names csv file: "))
names = f.read_csv('c:/projects/retail-crawl/app/input_names.csv')
a = APICrawler(names)
a.results_aggregator(names)
a.results_writer()