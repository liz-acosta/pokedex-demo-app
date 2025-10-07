import unittest
from unittest.mock import patch, Mock
import requests
from pokemon import (
    get_attributes, 
    get_list_by_attribute, 
    get_pokemon_by_name, 
    get_pokemon_description,
    POKEMON_ATTRIBUTES,
    BASE_URL
)


class TestPokemon(unittest.TestCase):
    """Unit tests for pokemon.py module"""

    def setUp(self):
        # This seems a little tedious since the test methods also create mock responses
        """Set up test fixtures before each test method."""
        self.mock_response = Mock()
        self.mock_response.json.return_value = {}

    def tearDown(self):
        """Clean up after each test method."""
        pass

    @patch('pokemon.requests.get')
    def test_get_attributes_success(self, mock_get):
        """Test get_attributes function with successful API response."""
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {
            'results': [
                {'name': 'fire'},
                {'name': 'water'},
                {'name': 'grass'}
            ]
        }
        mock_get.return_value = mock_response

        # Test the function
        result = get_attributes('type')

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertIn('fire', result)
        self.assertIn('water', result)
        self.assertIn('grass', result)
        self.assertEqual(result, ['fire', 'water', 'grass'])  # Order matters for this function
        mock_get.assert_called_once_with(BASE_URL + 'type')

    @patch('pokemon.requests.get')
    def test_get_attributes_empty_response(self, mock_get):
        """Test get_attributes function with empty results."""
        mock_response = Mock()
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        result = get_attributes('ability')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
        mock_get.assert_called_once_with(BASE_URL + 'ability')

    @patch('pokemon.requests.get')
    def test_get_list_by_attribute_with_pokemon_species(self, mock_get):
        """Test get_list_by_attribute when response contains pokemon_species."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'pokemon_species': [
                {'name': 'bulbasaur'},
                {'name': 'ivysaur'},
                {'name': 'venusaur'}
            ]
        }
        mock_get.return_value = mock_response

        result = get_list_by_attribute('Type', 'grass')

        expected_url = BASE_URL + POKEMON_ATTRIBUTES['Type'] + '/grass'
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertIn('bulbasaur', result)
        self.assertIn('ivysaur', result)
        self.assertIn('venusaur', result)
        self.assertEqual(result, ['bulbasaur', 'ivysaur', 'venusaur'])
        mock_get.assert_called_once_with(expected_url)

    @patch('pokemon.requests.get')
    def test_get_list_by_attribute_with_pokemon(self, mock_get):
        """Test get_list_by_attribute when response contains pokemon."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'pokemon': [
                {'pokemon': {'name': 'pikachu'}},
                {'pokemon': {'name': 'raichu'}}
            ]
        }
        mock_get.return_value = mock_response

        result = get_list_by_attribute('Ability', 'static')

        expected_url = BASE_URL + POKEMON_ATTRIBUTES['Ability'] + '/static'
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn('pikachu', result)
        self.assertIn('raichu', result)
        self.assertEqual(result, ['pikachu', 'raichu'])
        mock_get.assert_called_once_with(expected_url)

    @patch('pokemon.requests.get')
    def test_get_pokemon_by_name_success(self, mock_get):
        """Test get_pokemon_by_name with successful API response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 25,
            'name': 'pikachu',
            'types': [
                {'type': {'name': 'electric'}}
            ],
            'abilities': [
                {'ability': {'name': 'static'}}
            ],
            'sprites': {
                'front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'
            }
        }
        mock_get.return_value = mock_response

        # Mock the description function
        with patch('pokemon.get_pokemon_description') as mock_desc:
            mock_desc.return_value = 'A mouse Pokémon.'

            result = get_pokemon_by_name('pikachu')

            # Test individual fields for better error messages
            self.assertIsInstance(result, dict)
            self.assertEqual(result['id'], 25)
            self.assertEqual(result['name'], 'pikachu')
            self.assertIsInstance(result['types'], list)
            self.assertEqual(len(result['types']), 1)
            self.assertIn('electric', result['types'])
            self.assertIsInstance(result['abilities'], list)
            self.assertEqual(len(result['abilities']), 1)
            self.assertIn('static', result['abilities'])
            self.assertIsInstance(result['image_url'], str)
            self.assertTrue(result['image_url'].startswith('https://'))
            self.assertEqual(result['description'], 'A mouse Pokémon.')
            
            # Also test the complete object for regression
            expected_result = {
                'id': 25,
                'name': 'pikachu',
                'types': ['electric'],
                'abilities': ['static'],
                'image_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
                'description': 'A mouse Pokémon.'
            }
            self.assertEqual(result, expected_result)
            mock_get.assert_called_once_with(BASE_URL + 'pokemon/pikachu')
            mock_desc.assert_called_once_with('pikachu')

    @patch('pokemon.requests.get')
    def test_get_pokemon_by_name_json_decode_error(self, mock_get):
        """Test get_pokemon_by_name with JSON decode error."""
        # Mock a response that raises JSONDecodeError when .json() is called
        mock_response = Mock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        result = get_pokemon_by_name('invalid-pokemon')

        self.assertIsNone(result, "Function should return None when JSON decode fails")
        mock_get.assert_called_once_with(BASE_URL + 'pokemon/invalid-pokemon')

    @patch('pokemon.requests.get')
    def test_get_pokemon_description_success(self, mock_get):
        """Test get_pokemon_description with successful API response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'flavor_text_entries': [
                {
                    'language': {'name': 'en'},
                    'flavor_text': 'A mouse Pokémon.\nIt can generate electricity.'
                },
                {
                    'language': {'name': 'es'},
                    'flavor_text': 'Un Pokémon ratón.'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = get_pokemon_description('pikachu')

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn('mouse', result.lower())
        self.assertNotIn('\n', result, "Newlines should be replaced with spaces")
        self.assertEqual(result, 'A mouse Pokémon. It can generate electricity.')
        mock_get.assert_called_once_with(BASE_URL + 'pokemon-species/pikachu')

    @patch('pokemon.requests.get')
    # Does it make sense to have this test?
    # Even though `None` is a potential outcome of the function,
    # it doesn't have any way of handling the Error
    # Is the test maybe redundant?
    # This test is simply verifying the default behavior of Python
    # which is to raise a `TypeError` in this particular scenario
    def test_get_pokemon_description_no_english_entry(self, mock_get):
        """Test get_pokemon_description when no English entry is found."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'flavor_text_entries': [
                {
                    'language': {'name': 'es'},
                    'flavor_text': 'Un Pokémon ratón.'
                }
            ]
        }
        mock_get.return_value = mock_response

        # This should raise a TypeError when trying to access 'flavor_text' on None
        with self.assertRaises(TypeError):
            get_pokemon_description('pikachu')

    # Does it make sense to have this test?
    # Even though `None` is a potential outcome of the function,
    # it doesn't have any way of handling the Error
    # Is the test maybe redundant?
    # This test is simply verifying the default behavior of Python
    # which is to raise a `TypeError` in this particular scenario
    @patch('pokemon.requests.get')
    def test_get_pokemon_description_empty_entries(self, mock_get):
        """Test get_pokemon_description with empty flavor_text_entries."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'flavor_text_entries': []
        }
        mock_get.return_value = mock_response

        with self.assertRaises(TypeError):
            get_pokemon_description('pikachu')

    def test_pokemon_attributes_constants(self):
        """Test that POKEMON_ATTRIBUTES constant is correctly defined."""
        self.assertIsInstance(POKEMON_ATTRIBUTES, dict)
        self.assertEqual(len(POKEMON_ATTRIBUTES), 3)
        self.assertIn('Ability', POKEMON_ATTRIBUTES)
        self.assertIn('Color', POKEMON_ATTRIBUTES)
        self.assertIn('Type', POKEMON_ATTRIBUTES)
        self.assertEqual(POKEMON_ATTRIBUTES['Ability'], 'ability')
        self.assertEqual(POKEMON_ATTRIBUTES['Color'], 'pokemon-color')
        self.assertEqual(POKEMON_ATTRIBUTES['Type'], 'type')
        
        # Also test the complete object for regression
        expected_attributes = {
            'Ability': 'ability',
            'Color': 'pokemon-color',
            'Type': 'type'
        }
        self.assertEqual(POKEMON_ATTRIBUTES, expected_attributes)

    def test_base_url_constant(self):
        """Test that BASE_URL constant is correctly defined."""
        self.assertIsInstance(BASE_URL, str)
        self.assertTrue(BASE_URL.startswith('https://'))
        self.assertTrue(BASE_URL.endswith('/'))
        self.assertIn('pokeapi.co', BASE_URL)
        self.assertEqual(BASE_URL, 'https://pokeapi.co/api/v2/')

    
    # Is this test necessary?
    # This function handles singular or multiple types and abilities the same
    # this isn't testing anything meaningful  
    @patch('pokemon.requests.get')
    def test_get_pokemon_by_name_with_multiple_types_and_abilities(self, mock_get):
        """Test get_pokemon_by_name with multiple types and abilities."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 1,
            'name': 'bulbasaur',
            'types': [
                {'type': {'name': 'grass'}},
                {'type': {'name': 'poison'}}
            ],
            'abilities': [
                {'ability': {'name': 'overgrow'}},
                {'ability': {'name': 'chlorophyll'}}
            ],
            'sprites': {
                'front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
            }
        }
        mock_get.return_value = mock_response

        with patch('pokemon.get_pokemon_description') as mock_desc:
            mock_desc.return_value = 'A seed Pokémon.'

            result = get_pokemon_by_name('bulbasaur')

            expected_result = {
                'id': 1,
                'name': 'bulbasaur',
                'types': ['grass', 'poison'],
                'abilities': ['overgrow', 'chlorophyll'],
                'image_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
                'description': 'A seed Pokémon.'
            }

            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
