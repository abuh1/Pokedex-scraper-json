# Web scraper for https://pokemondb.net/pokedex/all - outputs into JSON file
import json
from bs4 import BeautifulSoup
import requests

# Function to write to json file
def writeToJSON(path, fileName, data):
    filePathName = './' + path + '/' + fileName + '.json'
    with open(filePathName, 'w') as file:
        json.dump(data, file)
        
path = './'
fileName = 'test'

# Start scraping
url = 'https://pokemondb.net/pokedex/all'
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

entries = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

for pokemon in entries[0:5]:
    data = {}
    # Creates list of every piece of data of the pokemon
    info = pokemon.find_all("td")
    
    data['dexno'] = int(info[0]['data-sort-value'])
    # Gets name of pokemon, but if pokemon is a different variation it will replace the name with the variation name. e.g. Mega Venusaur
    data['name'] = info[1].find_all("a")[0].getText()
    if info[1].find_all("small"):
        data['name'] = info[1].find_all("small")[0].getText()
    # Puts types into list
    types = []
    for t in info[2].find_all("a"):
        types.append(t.getText())
    data['types'] = types
    
    data['hp'] = info[4].getText()
    data['atk'] = info[5].getText()
    data['defense'] = info[6].getText()
    data['spatk'] = info[7].getText()
    data['spdef'] = info[8].getText()
    data['spd'] = info[9].getText()
    data['total'] = info[3].getText()
    
    writeToJSON(path, fileName, data)
    