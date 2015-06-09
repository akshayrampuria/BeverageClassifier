import csv 
from SimilarityFinder import edit_distance_dynamic, edit_distance_naive
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
CategoryCountMap = {}
prev = {}
for i in xrange(7): prev[i] = ""
itemnames = []
items = set()
# Declaring array with words of interest to look out for in a in a category name
beverages = ["beverage", "drink", "coffee", "juice", "tea"]

with open('import-io-seamless.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
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
				if category not in CategoryCountMap:
					CategoryCountMap[category] = 0
				CategoryCountMap[category] += 1
				for elem in row["item_name"].split(";")+row["item_name2"].split(";"):
					items.add(elem)
				# items.add(row["item_name"].split(";") + row["item_name"].split(";"))
				itemnames += row["item_name"].split(";")
				itemnames += row["item_name2"].split(";")
        		for (k,v) in row.items(): # go over each column name and value 
					columns[k].append(v) # append the value into the appropriate list based on column name k



# SortedCategoryNames = sorted(CategoryCountMap, key=CategoryCountMap.get)

# print CategoryCountMap
# print len(itemnames)
# print len(items)
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
			ed = edit_distance_naive(item.lower(), input_item, len(item), len(input_item), int(len(input_item)/1.5))
		# ed = EditDistanceDP(item.lower(), input_item)
			distances[item] = ed

	Recommendations = sorted(distances, key=distances.get)[:10]
	print Recos
	print Recommendations