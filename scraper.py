# Web scraper for https://pokemondb.net/pokedex/all - outputs into JSON file
import re
import json
from bs4 import BeautifulSoup
import requests

# Function to write to json file
def write_json(data, filename='dex.json'):
    with open(filename, 'r+') as f:
        # Load existing data into a dict (empty json file)
        file_data = json.load(f)
        file_data["pokemon"].append(data)
        f.seek(0)
        json.dump(file_data, f, indent = 4)

# Start scraping
url = 'https://pokemondb.net/pokedex/all'
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

entries = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")
# Take out partner pikachu and eevee
entries.pop(33)
entries.pop(178)

for pokemon in entries:
    varnames = ('dexno', 'name', 'height', 'weight', 'image', 'types', 'abilities', 'hp', 'atk', 'defense','spatk',
                'spdef', 'spd', 'total', 'is_mega', 'is_alolan', 'is_galarian', 'is_hisuian', 'is_paldean')
    data = {}
    # Creates list of every piece of data of the pokemon
    info = pokemon.find_all("td")
    
    # Gets name of pokemon, but if pokemon is a different variation it will replace the name with the variation name. e.g. Mega Venusaur
    name = info[1].find_all("a")[0].getText()
    if info[1].find_all("small"):
        name = info[1].find_all("small")[0].getText()
    
    if 'partner' in name.lower():
        print(name)
        continue
    # Pokedex number for each pokemon. Not unique (variations of the same pokemon have the same dex number)
    dexno = int(info[0]['data-sort-value'])
        
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
    info_tabs = details_soup.find_all(class_ = "tabset-basics")[0].find_all(class_ = "sv-tabs-panel-list")[0].find_all(class_ = "sv-tabs-panel", id=re.compile(r'tab-basic-[\d]+'))
    
    # Choose current tab info for the pokemon
    zipped_tabs = list(zip(tab_names, info_tabs))
    for tab in zipped_tabs:
        if tab[0] == name:
            active = tab[1]
    # Scrape the rest of the info from active tab
    height = active.find_all(class_ = "vitals-table")[0].find_all("tr")[3].find("td").getText()
    weight = active.find_all(class_ = "vitals-table")[0].find_all("tr")[4].find("td").getText()
    image = active.find_all(class_ = "grid-col span-md-6 span-lg-4 text-center")[0].find_all("img")[0]["src"]
    
    abilities = []
    ability_tags = active.find_all(class_ = "vitals-table")[0].find_all("tr")[5].find_all(class_ = "text-muted")
    for a in ability_tags:
        abilities.append(a.find_all("a")[0].getText())
    
    is_mega, is_galarian, is_alolan, is_hisuian, is_paldean = False, False, False, False, False
    if 'mega' in name.lower():
        is_mega = True
    elif 'alolan' in name.lower():
        is_alolan = True
    elif 'galarian' in name.lower():
        is_galarian = True
    elif 'hisuian' in name.lower():
        is_hisuian = True
    elif 'paldean' in name.lower():
        is_paldean = True
    
    heading = details_soup.find_all("h1")[0].getText()
    if heading not in name:
        name = name + ' ' + heading
    
    # Put all data into a dictionary
    for i in varnames:
        data[i] = locals()[i]
        
    # Output to json file
    write_json(data)
