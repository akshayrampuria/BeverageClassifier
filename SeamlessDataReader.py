import csv 
from SimilarityFinder import edit_distance_dynamic, edit_distance_naive
# from python-Levenshtein import distance
import requests, time
from xgoogle.search import GoogleSearch, SearchError
from collections import defaultdict
import wikipedia

columns = defaultdict(list) # each value in each column is appended to a list
CategoryCountMap = {}
CuisineDrinkItems = {}
NonDrinkItems = []
prev = {}
for i in xrange(7): prev[i] = ""
DrinkItems = []
items = set()
# Declaring array with words of interest to look out for in a in a category name
beverages = ["beverage", "drink", "coffee", "juice", "tea"]

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
		if any(beverage in category for beverage in beverages):
			if "stea" not in category: # eliminating steam and steak
				drink = True
				if category not in CategoryCountMap:
					CategoryCountMap[category] = 0
				CategoryCountMap[category] += 1
				for elem in row["item_name"].split(";")+row["item_name2"].split(";"):
					if row["cuisine"] not in CuisineDrinkItems:
						CuisineDrinkItems[row["cuisine"]] = set()
					CuisineDrinkItems[row["cuisine"]].add(elem)
					items.add(elem)
				# items.add(row["item_name"].split(";") + row["item_name"].split(";"))
				DrinkItems += row["item_name"].split(";")
				DrinkItems += row["item_name2"].split(";")
				for (k,v) in row.items(): # go over each column name and value 
					columns[k].append(v) # append the value into the appropriate list based on column name k
		if not drink:
			for elem in row["item_name"].split(";")+row["item_name2"].split(";"):
				NonDrinkItems += elem






# SortedCategoryNames = sorted(CategoryCountMap, key=CategoryCountMap.get)

# print CategoryCountMap
# print len(DrinkItems)
# print len(items)
def getRecommendedNames():
	while(True):
		input_item = raw_input("Enter an Item Name:")
		if input_item == "":
			break
		distances = {}
		Recos = []
		for item in items:
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

def pingGoogleForWiki():
	for item in items:
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



def pingWiki():
	for item in items:
	  	print item, wikipedia.search(item)
		 

# pingWiki()