# Pokedex demo app

This is a simple Flask app that enables users to view Pokemon according to the following attributes: Ability, Color, or Type.

## Prerequisites

* Python 3.11+
* Some familiarity with [Jupyter notebooks](https://jupyter.org/install)

## Running the Flask app

1. Create a virtual environment: `virtualenv venv`

2. Activate the virtual environment: `source venv/bin/activate`

3. Install the required depedencies: `pip install -r requirements.txt` 

4. Run the app: `flask run`

The Flask app will start, and you can view it by navigating to http://localhost:5000 in your browser.

## Running the Jupyter notebook

1. Install Jupyter: `pip3 install jupyter`

2. Run the notebook: `jupyter notebook`

The Jupyter server will start and automatically open a new browswer tab.

## Running and viewing the coverage report

1. Analyze the code for coverage: `coverage run -m unittest`

2. View the coverage report: `coverage report`

## Running the tests

1. Run the tests: `python -m unittest`


