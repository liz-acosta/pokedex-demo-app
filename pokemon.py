from enum import Enum
import requests

POKEMON_ATTRIBUTES = {'Ability': 'ability',
                      'Color': 'pokemon-color',
                      'Type': 'type'}

BASE_URL = 'https://pokeapi.co/api/v2/'

def get_attributes(attribute):

    response = requests.get(BASE_URL + attribute)

    response_json = response.json()

    attributes_list = [item['name'] for item in response_json['results']]

    return attributes_list
    
def get_list_by_attribute(attribute, selection):
    
    response = requests.get(BASE_URL + POKEMON_ATTRIBUTES[attribute] + '/' + selection)

    pokemon_list = [item['pokemon']['name'] for item in response.json()['pokemon']]

    return pokemon_list

def get_pokemon_by_name(name):

    response = requests.get(BASE_URL + 'pokemon/' + name)

    response_json = response.json()

    pokemon = {'id': response_json['id'],
                'name': response_json['name'],
                'types': [item['type']['name'] for item in response_json['types']],
                'abilities': [item['ability']['name'] for item in response_json['abilities']],
                'image_url': response_json['sprites']['front_default']}
    
    return pokemon

def get_pokemon_characteristics_by_id(pokemon):

    response = requests.get(BASE_URL + 'pokemon-species/' + pokemon['name'])

    response_json = response.json()

    description = next(filter(lambda x: x['version']['name'] == 'firered', response_json['flavor_text_entries']), None)

    pokemon.update({'description': description['flavor_text'].replace('\n', ' '),
                    'color': response_json['color']['name']}) 

    return pokemon

print(get_attributes('type'))

# test = get_list_by_attribute('type', 'ground')

test_pokemon = get_pokemon_by_name('eevee')

test_test_pokemon = get_pokemon_characteristics_by_id(test_pokemon)

print(test_pokemon)

print('****', test_test_pokemon)




    