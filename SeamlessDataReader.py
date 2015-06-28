import csv 
from SimilarityFinder import edit_distance_dynamic, edit_distance_naive
# from python-Levenshtein import distance
import requests, time, pickle
from xgoogle.search import GoogleSearch, SearchError
from collections import defaultdict
import wikipedia


class DataReader:

	def __init__(self):
		self.numBev = 0
		self.numNotBev = 0
		self.columns = defaultdict(list) # each value in each column is appended to a list
		self.CategoryCountMap = {}
		self.CuisineDrinkItems = {}
		self.NonDrinkItems = []
		self.DrinkItems = []
		self.setOfDrinkItems = set()
		self.setOfNonDrinkItems = set()
		# Declaring array with words of interest to look out for in a in a category name
		self.beverages = ["beverage", "drink", "coffee", "juice", "tea"]
		self.drinkCorpusFile = "drink_corpus"
		self.nonDrinkCorpusFile = "non_drink_corpus"


	def readSeamlessData(self):
		prev = {}
		for i in xrange(7): prev[i] = ""
		with open('import-io-seamless.csv') as f:
			reader = csv.DictReader(f) # read rows into a dictionary format
			for row in reader: # read a row as {column1: value1, column2: value2,...}
				drink = False
				keys = row.keys()
				for i in xrange(7):
					key = keys[i]
					if row[key] == "":
						row[key] = prev[i]
					else:
						prev[i] = row[key]
				category = row["category"].lower()
				if any(beverage in category for beverage in self.beverages):
					if "stea" not in category: # eliminating steam and steak
						drink = True
						if category not in self.CategoryCountMap:
							self.CategoryCountMap[category] = 0
						self.CategoryCountMap[category] += 1
						for elem in row["item_name"].split(";")+row["item_name2"].split(";"):
							if row["cuisine"] not in self.CuisineDrinkItems:
								self.CuisineDrinkItems[row["cuisine"]] = set()
							self.CuisineDrinkItems[row["cuisine"]].add(elem)
							self.setOfDrinkItems.add(elem)
						# items.add(row["item_name"].split(";") + row["item_name"].split(";"))
						self.DrinkItems += row["item_name"].split(";")
						self.DrinkItems += row["item_name2"].split(";")
						for (k,v) in row.items(): # go over each column name and value 
							self.columns[k].append(v) # append the value into the appropriate list based on column name k
				if not drink:
					for elem in row["item_name"].split(";") + row["item_name2"].split(";"):
						self.NonDrinkItems.append(elem)
						self.setOfNonDrinkItems.add(elem)


	def classifyAsBeverageUsingEditDistance(self, input_item):
		nonDrinkEd = 0
		drinkEd = 0
		for item in self.NonDrinkItems:
			nonDrinkEd += edit_distance_naive(item.lower(), input_item.lower(), len(item), len(input_item), 8)
		for item in self.DrinkItems:
			drinkEd += edit_distance_naive(item.lower(), input_item.lower(), len(item), len(input_item), 8)

		if float(drinkEd/len(self.DrinkItems)) < float(nonDrinkEd/len(self.NonDrinkItems)):
			print "Beverage\n"
		else:
			print "Not Beverage\n"


	def classifyAsBeverage(self, input_item):
		keywords = input_item.split()
		keywords = [word.lower() for word in keywords]
		catchwords = ["juice", "tea", "coffee", "drink", "beverage", "water", "shake", "lemonade", "milkshake", "pellegrino", "smoothie", "coke", "milk", "latte", "iced", "soda"]
		for word in keywords:
			if word in catchwords:
				# print "Beverage"
				return True
		# print "Not Beverage"
		return False


	def getRecommendedNames(self):
		while(True):
			input_item = raw_input("Enter an Item Name:")
			if input_item == "":
				break
			distances = {}
			Recos = []
			for item in self.setOfDrinkItems:
				if input_item in item.lower():
					Recos.append(item)
				else:
					ed = edit_distance_naive(item.lower(), input_item.lower(), len(item), len(input_item), 8)
					# ed = EditDistanceDP(item.lower(), input_item)
					# ed = distance(item.lower(), input_item)
					distances[item] = ed

			Recommendations = sorted(distances, key=distances.get)[:10]
			print Recos
			print Recommendations

	def pingGoogleForWiki(self):
		for item in self.setOfDrinkItems:
			# inventory[vertical] = {}
			try:
			  # time.sleep(5)
			  gs = GoogleSearch("site:wikipedia.org "+item+" drink")
			  gs.results_per_page = 5
			  results = gs.get_results()
			  for res in results:
				# print str(res)
				# print res.title.encode("utf8")
				# print res.desc.encode("utf8")
				url = res.url.encode("utf8")
				# if len(url.rsplit('/')) - len(url.rsplit('/', 1)) == 4:
				# 	url = url.rsplit('/', 1)[0]
				# if url in visitedUrls:
				# 	continue
				if "wiki" not in url:
					continue
				else:
					print item, url
				# menu = getItems(url)
				# visitedUrls.add(url)
				# if menu:
				# 	inventory[vertical][menu['name']] = menu
			except SearchError, e:
			  print "Search failed: %s" % e
			  print "Not found for vertical %s" % item


	def pingWiki(self, item):
		item = item.strip()
		categories = ""
		if item:
			pages = wikipedia.search(item+" drink")
			# print item, pages
			for page in pages:
				print item, page
				try:
					p = wikipedia.page(page)
				except wikipedia.exceptions.DisambiguationError as e:
					print "Confused Disabmiguation", e.options
				# wp = wikipedia.WikipediaPage(title=page)
				categories += p.summary
		return categories
			 

	def commandLineCirculation(self):
		while(True):
			input_item = raw_input("Enter an Item Name:\n")
			if input_item == "":
				break
			if self.classifyAsBeverage(input_item):
				print "Beverage"
			else:
				print "Not Beverage"

	def buildWikiCorpus(self):
		self.drinkCorpus = []
		for drink in self.setOfDrinkItems:
			item = drink.strip()
			if item:
				try:
					pages = wikipedia.search(item + " drink")
				except wikipedia.exceptions.WikipediaException as e:
					print "Timeout for " + item
				summary = ""
				for page in pages:
					try:
						p = wikipedia.page(page)
					except wikipedia.exceptions.DisambiguationError as e:
						print "Confused Disabmiguation", e.options
					summary += p.summary
				self.drinkCorpus.append(summary)

		# self.nonDrinkCorpus = []
		# for nonDrink in self.setOfNonDrinkItems:
		# 	item = nonDrink.strip()
		# 	if item:
		# 		pages = wikipedia.search(item + " drink")
		# 		summary = ""
		# 		for page in pages:
		# 			p = wikipedia.page(page)
		# 			summary += p.summary
		# 		self.nonDrinkCorpus.append(summary)

		pickle.dump(self.drinkCorpus, self.drinkCorpusFile)
		# pickle.dump(self.nonDrinkCorpus, self.nonDrinkCorpusFile)

	def getWikiCorpus(self):
		self.drinkCorpus = pickle.load(self.drinkCorpusFile)
		self.nonDrinkCorpus = pickle.load(self.nonDrinkCorpusFile)

# k = -1
# freq = {}
# for item in items:
# 	# print item
# 	if classifyAsBeverage(item):
# 		numBev = numBev + 1
# 	else:
# 		# keywords = item.split()
# 		# keywords = [word.lower() for word in keywords]
# 		# print keywords
# 		# for word in keywords:
# 		# 	if word in freq:
# 		# 		freq[word] += 1
# 		# 	else:
# 		# 		freq[word] = 0
# 		print item
# 		cats = pingWiki(item)
# 		print cats
# 		numNotBev = numNotBev + 1

# print numBev, numNotBev

def main():
	d = DataReader()
	d.readSeamlessData()
	d.buildWikiCorpus()
	# print len(d.setOfDrinkItems), len(d.setOfNonDrinkItems)
	# d.commandLineCirculation()
	
if __name__ == "__main__":
	main()



# print wikipedia.search("peach iced tea")