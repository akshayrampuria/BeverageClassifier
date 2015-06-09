from google import search

num_results = 100
cuisines = ['African','American','Argentinian','Bagels','BBQ','Belgian','Brazilian','Breakfast','Brunch','Bubble Tea','Burgers','Cajun and Creole','Californian Cuisine','Cambodian','Caribbean','Cheesesteaks','Chinese','Churrascaria','Costa Rican','Crepes','Cuban','Deli','Dessert','Dim Sum and dumplings','Diner','English','Farm','Filipino','French','Frozen Yogurt and dessert','German','Gluten-Free','Greek','Grocery Items','Haitian','Halal','Hawaiian','Healthy','Hot Dogs','Indian','Indonesian','Irish','Italian','Jamaican','Japanese','Juices','Korean','Kosher','Late-Night','Latin-American','Lebanese','Lunch-Specials','Malaysian','Mediterranean','Mexican','Middle-Eastern','Moroccan','Noodle-Shops','Organic','Pakistani','Peruvian','Pizza','Polish','Portuguese','Russian','Salads','Sandwiches-Wraps','Scandinavian','Seafood','Smoothies-Shakes','Soup','Southern and Soul','Spanish','Sri-Lankan','Steakhouse','Sushi','Sweets and Candy','Taiwanese','Thai','Turkish','Vegan','Vegetarian','Venezuelan','Vietnamese','Wings']
site_query = 'site:http://www.seamless.com/food-delivery/'
outfile_name = 'seamless-urls.txt'

for cuisine in cuisines:
    search_query = site_query+' '+'\"'+cuisine+'\"'
    res = search(search_query, stop=num_results)
    for url in res:
        with open(outfile_name, 'a') as outfile:
            outfile.write(url+'\n')
        print(url)
