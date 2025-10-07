# Unit Tests for Pokemon.py

This directory contains comprehensive unit tests for the `pokemon.py` module using Python's built-in `unittest` framework.

## Test Coverage

The test suite covers all functions in `pokemon.py`:

- `get_attributes()` - Tests successful API responses and empty results
- `get_list_by_attribute()` - Tests both `pokemon` and `pokemon_species` response formats
- `get_pokemon_by_name()` - Tests successful responses, JSON decode errors, and multiple types/abilities
- `get_pokemon_description()` - Tests successful responses, missing English entries, and empty entries
- Constants - Tests `POKEMON_ATTRIBUTES` and `BASE_URL` constants

## Running the Tests

### Method 1: Using unittest directly
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m unittest test_pokemon.py -v

# Run specific test
python -m unittest test_pokemon.TestPokemon.test_get_attributes_success -v
```

### Method 2: Using the test runner script
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests with custom runner
python run_tests.py
```

### Method 3: Using pytest (if installed)
```bash
# Activate virtual environment
source venv/bin/activate

# Install pytest if not already installed
pip install pytest

# Run tests with pytest
pytest test_pokemon.py -v
```

## Test Features

- **Mocking**: All tests use `unittest.mock` to avoid making actual API calls
- **Comprehensive Coverage**: Tests both success and error scenarios
- **Edge Cases**: Handles empty responses, missing data, and API errors
- **Isolation**: Each test is independent and doesn't affect others
- **Documentation**: Each test method has clear docstrings explaining its purpose

## Test Structure

```
TestPokemon
├── setUp() - Initialize test fixtures
├── tearDown() - Clean up after tests
├── test_get_attributes_* - Tests for get_attributes function
├── test_get_list_by_attribute_* - Tests for get_list_by_attribute function
├── test_get_pokemon_by_name_* - Tests for get_pokemon_by_name function
├── test_get_pokemon_description_* - Tests for get_pokemon_description function
└── test_*_constants - Tests for module constants
```

## Expected Output

When all tests pass, you should see:
```
Ran 12 tests in 0.004s
OK
```

## Adding New Tests

To add new tests:

1. Add a new test method to the `TestPokemon` class
2. Follow the naming convention: `test_function_name_scenario`
3. Use appropriate mocking with `@patch('pokemon.requests.get')`
4. Include a descriptive docstring
5. Test both success and failure scenarios

Example:
```python
@patch('pokemon.requests.get')
def test_new_function_success(self, mock_get):
    """Test new_function with successful response."""
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = {'expected': 'data'}
    mock_get.return_value = mock_response
    
    # Test the function
    result = new_function('test_input')
    
    # Assertions
    self.assertEqual(result, expected_result)
    mock_get.assert_called_once_with(expected_url)
```
