import networkx as nx
import requests

country_list = ["Belgium", "Bulgaria", "Czech Republic", "Denmark", "Germany", "Estonia", "Ireland", "Greece", "Spain", "France", "Croatia", "Italy", "Cyprus", "Latvia", "Lithuania", "Luxembourg", "Hungary", "Malta", "Netherlands", "Austria", "Poland", "Portugal", "Romania", "Slovenia", "Slovakia", "Finland", "Sweden", "Norway"]
item_dict = {}
for country in country_list:
    params = dict (
            action='wbsearchentities',
            format='json',
            language='en',
            uselang='en',
            type='item',
            search=country
            )

    response = requests.get('https://www.wikidata.org/w/api.php?', params).json() 
    item_dict[country]=response["search"][0]["id"]

adj_dict = {i:[] for i in country_list}
url = 'https://query.wikidata.org/sparql'
for key, value in item_dict.items():
    # print(key+":")
    query = '''
    SELECT ?country2Label {
      VALUES (?country1) {(wd:'''+value+''')}
      ?border wdt:P31 wd:Q12413618 ;
              wdt:P17 ?country1 , ?country2 .
      FILTER (?country1 != ?country2)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      } ORDER BY ?country1Label
    '''
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    for i in data["results"]["bindings"]:
        country = i["country2Label"]["value"]
        if country in country_list:
            adj_dict[key]=[*adj_dict[key], country]

G = nx.Graph(adj_dict)
nx.write_adjlist(G, "borders.adjlist")