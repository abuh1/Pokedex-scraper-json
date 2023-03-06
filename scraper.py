# Web scraper for https://pokemondb.net/pokedex/all - outputs into JSON file
from bs4 import BeautifulSoup
import requests

url = 'https://pokemondb.net/pokedex/all'
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

entries = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")
print(entries[100])