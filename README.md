# Pokedex scraper using Python (BeautifulSoup and regex)

Using BeautifulSoup to scrape data from https://pokemondb.net/pokedex

The program first scrapes https://pokemondb.net/pokedex/all for each pokemon's dex number, name, types and stats. It then goes to https://pokemondb.net/pokedex/{pokemon-name} to scrape the image, height, weight, and abilities. For pokemon variants it scrapes the variant's tab information instead.
