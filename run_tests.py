#!/usr/bin/env python3
"""
Test runner script for pokemon.py unit tests.
This script provides an easy way to run all tests with detailed output.
"""

import unittest
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the test module
from test_pokemon import TestPokemon

def run_tests():
    """Run all unit tests for pokemon.py"""
    print("Running unit tests for pokemon.py...")
    print("=" * 50)
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPokemon)
    
    # Run the tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
