import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
CategoryMap = {}
prev = {}
for i in xrange(7): prev[i] = ""

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
				if category not in CategoryMap:
					CategoryMap[category] = 0
				CategoryMap[category] += 1
        		for (k,v) in row.items(): # go over each column name and value 
					columns[k].append(v) # append the value into the appropriate list based on column name k



SortedCategoryNames = sorted(CategoryMap, key=CategoryMap.get)

print CategoryMap
print columns
