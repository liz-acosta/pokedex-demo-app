from flask import Flask, render_template,request
import pokemon

app = Flask(__name__)

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
    print(form_data)
    
    pokemon_attribute = list(request.form.keys())[0]
    pokemon_selection = form_data[pokemon_attribute]
    print(pokemon_attribute)

    pokemon_list = pokemon.get_list_by_attribute(pokemon_attribute, pokemon_selection)
    if request.method == 'POST':
        print(request.form.keys())
    return render_template("pokemon.html", pokemon_list=pokemon_list)
   
#    else:
#       user = request.args.get('name')

#     pokemon.get_list_by_attribute
#     return render_template("pokemon.html", pokemon=pokemon)

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['name']
#       return redirect(url_for('dashboard',name = user))
#    else:
#       user = request.args.get('name')

if __name__ == "__main__":
    app.run(debug=True)