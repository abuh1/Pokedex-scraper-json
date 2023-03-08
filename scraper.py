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
        
path = './'
fileName = 'test'

# Start scraping
url = 'https://pokemondb.net/pokedex/all'
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

entries = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

for i, pokemon in enumerate(entries[69:70]):
    varnames = ('id', 'dexno', 'name', 'height', 'weight', 'image', 'types', 'hp', 'atk', 'defense','spatk',
                'spdef', 'spd', 'total')
    data = {}
    # Creates list of every piece of data of the pokemon
    info = pokemon.find_all("td")
    
    # Unique index for each data entry
    id = i
    # Pokedex number for each pokemon. Not unique (variations of the same pokemon have the same dex number)
    dexno = int(info[0]['data-sort-value'])
    # Gets name of pokemon, but if pokemon is a different variation it will replace the name with the variation name. e.g. Mega Venusaur
    name = info[1].find_all("a")[0].getText()
    if info[1].find_all("small"):
        name = info[1].find_all("small")[0].getText()
    # Puts types into list
    types = []
    for t in info[2].find_all("a"):
        types.append(t.getText())
    
    # Scrape stats
    hp = info[4].getText()
    atk = info[5].getText()
    defense = info[6].getText()
    spatk = info[7].getText()
    spdef = info[8].getText()
    spd = info[9].getText()
    total = info[3].getText()
    
    # Start to scrape the individual page of each pokemon for additional data
    details_ext = info[1].find_all("a")[0]["href"]
    
    # e.g https://pokemondb.net/pokedex/bulbasaur
    details_url = f"https://pokemondb.net{details_ext}"
    page = requests.get(details_url)
    details_soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get each tab name in a list
    tab_names = []
    tab_labels = details_soup.find_all(class_ = "sv-tabs-tab-list")[0].find_all(class_ = "sv-tabs-tab")
    for label in tab_labels:
        tab_names.append(label.getText())
    
    # Get each tab panel in a list
    info_tabs = details_soup.find_all(class_ = "tabset-basics")[0].find_all(class_ = "sv-tabs-panel-list")[0].find_all(class_ = "sv-tabs-panel")
    
    # Choose current tab info for the pokemon
    zipped_tabs = list(zip(tab_names, info_tabs))
    for tabs in zipped_tabs:
        if tabs[0] == name:
            active = tabs[1]
    # Scrape the rest of the info from active tab
    height = active.find_all(class_ = "vitals-table")[0].find_all("tr")[3].find("td").getText()
    weight = active.find_all(class_ = "vitals-table")[0].find_all("tr")[4].find("td").getText()
    image = active.find_all("picture")[0].find_all("img")[0]["src"]
    abilities = active.find_all(class_ = "vitals-table")[0].find_all("tr")[5].find(class_ = "text-muted")
    
    print(name)
    print(image)    
    
    
    # Put all data into a dictionary
    for i in varnames:
        data[i] = locals()[i]
    
    # Output to json file
    # write_json(data)