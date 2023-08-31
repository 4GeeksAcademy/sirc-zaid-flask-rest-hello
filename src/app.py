"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Starships, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# USER

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    response = list(map(lambda user: user.serialize(), users))

    print(response)

    if (response == []):
        return {"msg": "No hay usuarios"}

    response_body = {
        "results": response
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user = User.query.filter_by(id = user_id).first()
    
    if user is None:
        return {
            "error": "Usuario no encontrado"
        }
    
    return {
        "msg": "Buenass",
        "results": user.serialize()
    }

# PEOPLE

@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()
    response = list(map(lambda user: user.serialize(), people))

    print(response)

    if (response == []):
        return {"msg": "No hay personas"}

    response_body = {
        "results": response
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):

    people = People.query.filter_by(id = people_id).first()
    
    if people is None:
        return {
            "error": "Usuario no encontrado"
        }
    
    return {
        "results": people.serialize()
    }

# PLANETS

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    response = list(map(lambda user: user.serialize(), planets))

    print(response)

    if (response == []):
        return {"msg": "No hay planetas"}

    response_body = {
        "results": response
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):

    planets = Planets.query.filter_by(id = planets_id).first()
    
    if planets is None:
        return {
            "error": "Planeta no encontrado"
        }
    
    return {
        "results": planets.serialize()
    }



# VEHICLES

@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    vehicles = Vehicles.query.all()
    response = list(map(lambda user: user.serialize(), vehicles))

    print(response)

    if (response == []):
        return {"msg": "No hay favoritos"}

    response_body = {
        "results": response
    }

    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_one_vehicle(vehicles_id):

    vehicle = Vehicles.query.filter_by(id = vehicles_id).first()
    
    if vehicle is None:
        return {
            "error": "Favorito no encontrado"
        }
    
    return {
        "results": vehicle.serialize()
    }

# STARSHIPS

@app.route('/starships', methods=['GET'])
def get_starship():

    starship = Starships.query.all()
    response = list(map(lambda user: user.serialize(), starship))

    print(response)

    if (response == []):
        return {"msg": "No hay favoritos"}

    response_body = {
        "results": response
    }

    return jsonify(response_body), 200

@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_one_starship(starships_id):

    favorite = Starships.query.filter_by(id = starships_id).first()
    
    if favorite is None:
        return {
            "error": "Favorito no encontrado"
        }
    
    return {
        "results": favorite.serialize()
    }


# FAVORITES 

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_one_favorite(id):

    favorites = Favorites.query.filter_by(user_id = id)
    response = list(map(lambda user: user.serialize(), favorites))

    
    if response == []:
        return {
            "error": "Favorito no encontrado"
        }
    
    return {
        "results": response
    }

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def set_favorite_person(people_id):
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    
    if user_query is None:
        return {"msg": "El usuario no existe"}

    people_query = People.query.filter_by(id = people_id).first()
    if people_query is None:
        return {"msg": "El personaje no existe"}

    newPeople = Favorites(user_id=request_body["user_id"], people_id = people_id)
    
    favorites = Favorites.query.filter_by(user_id = request_body["user_id"])
    for favorite in favorites:
        if favorite.people_id == people_id:
            return { "msg": "El personaje ya fue agregado" }
        

    db.session.add(newPeople)
    db.session.commit()

    return {
        "results": "Guardado"
    }

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def set_favorite_planet(planet_id):
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    
    if user_query is None:
        return {"msg": "El usuario no existe"}

    planet_query = Planets.query.filter_by(id = planet_id).first()
    if planet_query is None:
        return {"msg": "El planeta no existe"}

    newPlanet = Favorites(user_id=request_body["user_id"], planet_id = planet_id)
    
    favorites = Favorites.query.filter_by(user_id = request_body["user_id"])
    for favorite in favorites:
        if favorite.planet_id == planet_id:
            return { "msg": "El planeta ya fue agregado" }
        

    db.session.add(newPlanet)
    db.session.commit()

    return {
        "results": "Guardado"
    }

# DELETE

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    
    if user_query is None:
        return {"msg": "El usuario no existe, puedes crearlo"}

    planet_query = Planets.query.filter_by(id = planet_id).first()
    if planet_query is None:
        return {"msg": "El planeta no existe, puedes crearlo"}

    
    favorites = Favorites.query.filter_by(user_id = request_body["user_id"])

    existeFavorito = False

    for favorite in favorites:
        if favorite.planet_id == planet_id:
            existeFavorito = True
            db.session.delete(favorite)
            db.session.commit()
    
    if existeFavorito:
        return {"msg": "Este planeta ya fue borrado"}

    return {
        "results": "borrado!"
    }

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    
    if user_query is None:
        return {"msg": "El usuario no existe, puedes crearlo"}

    people_query = People.query.filter_by(id = people_id).first()
    if people_query is None:
        return {"msg": "El personaje no existe, puedes crearlo"}

    
    favorites = Favorites.query.filter_by(user_id = request_body["user_id"])

    existeFavorito = False

    for favorite in favorites:
        if favorite.people_id == people_id:
            existeFavorito = True
            db.session.delete(favorite)
            db.session.commit()
    
    if existeFavorito == False:
        return {"msg": "Este personaje ya fue borrado"}

    return {
        "results": "borrado!"
    }




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
