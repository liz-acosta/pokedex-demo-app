import requests

POKEMON_ATTRIBUTES = {'Ability': 'ability',
                      'Color': 'pokemon-color',
                      'Type': 'type'}

def populate_dropdown(attribute):
    base_url = 'https://pokeapi.co/api/v2/'
    response = requests.get(base_url + POKEMON_ATTRIBUTES[attribute])
    dropdown_items = [item['name'] for item in response.json()['results']]
    return dropdown_items

test = populate_dropdown('Ability')

print(test)
