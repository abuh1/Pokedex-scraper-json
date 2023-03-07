# Web scraper for https://pokemondb.net/pokedex/all - outputs into JSON file
import json
from bs4 import BeautifulSoup
import requests

# Function to write to json file
def write_json(data, filename='draftdex.json'):
    with open(filename, 'r+') as f:
        # Load existing data into a dict (empty json file)
        file_data = json.load(f)
        file_data["pokemon"].append(data)
        f.seek(0)
        json.dump(file_data, f, indent = 4)
        
# Function to scrape detailed pages of each pokemon, including alternate forms
def scrape_details(pokemon):
    pass
        
        
path = './'
fileName = 'test'

# Start scraping
url = 'https://pokemondb.net/pokedex/all'
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

entries = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

for i, pokemon in enumerate(entries[0:20]):
    data = {}
    # Creates list of every piece of data of the pokemon
    info = pokemon.find_all("td")
    
    # Unique index for each data entry
    data['id'] = i
    # Pokedex number for each pokemon. Not unique (variations of the same pokemon have the same dex number)
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
    
    # Scrape stats
    data['hp'] = info[4].getText()
    data['atk'] = info[5].getText()
    data['defense'] = info[6].getText()
    data['spatk'] = info[7].getText()
    data['spdef'] = info[8].getText()
    data['spd'] = info[9].getText()
    data['total'] = info[3].getText()
    
    # Start to scrape the individual page of each pokemon for additional data
    details_ext = info[1].find_all("a")[0]["href"]
    
    # e.g https://pokemondb.net/pokedex/bulbasaur
    details_url = f"https://pokemondb.net{details_ext}"
    page = requests.get(details_url)
    det_soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get image - gets alternate form image if other forms
    images = det_soup.find_all("picture")[1].find_all("img")
    for img in images:
        pic = img['src']
    
    print(data['name'])
    print(pic)