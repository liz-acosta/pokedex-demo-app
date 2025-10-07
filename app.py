from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import pokemon

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route("/")
def home():

    attributes_dict = {}
    
    for key, value in pokemon.POKEMON_ATTRIBUTES.items():

        pokemon_attributes_list = pokemon.get_attributes(value)
        attributes_dict[key] = pokemon_attributes_list

    return render_template("index.html", pokemon_attributes=pokemon.POKEMON_ATTRIBUTES, attributes_dict=attributes_dict)

@app.route("/pokemon", methods = ['POST', 'GET'])
def display_pokemon():

    form_data = request.form.to_dict()
    
    pokemon_attribute = list(request.form.keys())[0]
    pokemon_selection = form_data[pokemon_attribute]

    pokemon_list = pokemon.get_list_by_attribute(pokemon_attribute, pokemon_selection)
    
    pokemon_dict_list = [pokemon.get_pokemon_by_name(pokemon_name) for pokemon_name in pokemon_list]

    print(pokemon_dict_list[0])

    return render_template("pokemon.html", pokemon_dict_list=pokemon_dict_list)

if __name__ == "__main__":
    app.run(debug=True)