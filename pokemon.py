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

    print(BASE_URL + POKEMON_ATTRIBUTES[attribute] + '/' + selection)
    
    response = requests.get(BASE_URL + POKEMON_ATTRIBUTES[attribute] + '/' + selection)

    response_json = response.json()

    if 'pokemon' not in response_json.keys():
        pokemon_list = [item['name'] for item in response_json['pokemon_species']]
    else:
        pokemon_list = [item['pokemon']['name'] for item in response_json['pokemon']]

    return pokemon_list

def get_pokemon_by_name(name):

    print(BASE_URL + 'pokemon/' + name)

    response = requests.get(BASE_URL + 'pokemon/' + name)

    try:
        response_json = response.json()
        pokemon = {'id': response_json['id'],
            'name': response_json['name'],
            'types': [item['type']['name'] for item in response_json['types']],
            'abilities': [item['ability']['name'] for item in response_json['abilities']],
            'image_url': response_json['sprites']['front_default'],
            'description': get_pokemon_description(response_json['name'])}
        return pokemon
    
    except requests.exceptions.JSONDecodeError:
        print(f"{name} is a pokemon species and not a pokemon lol")

def get_pokemon_description(pokemon):

    response = requests.get(BASE_URL + 'pokemon-species/' + pokemon)

    response_json = response.json()

    description = next(filter(lambda x: x['language']['name'] == 'en', response_json['flavor_text_entries']), None)['flavor_text'].replace('\n', ' ')

    return description




    