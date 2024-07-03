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
from models import db, User, Personajes, Vehiculos, Planetas
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

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))

    response_body = {
        "msg": "OK",
        "data": users_serialized
    }

    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def handle_personajes():

    personajes = Personajes.query.all() 
    personajes_serialized = list(map(lambda item:item.serialize(), personajes))

    response_body = {
        "msg": "OK",
        "data": personajes_serialized
    }

    return jsonify(response_body), 200

@app.route('/vehiculos', methods=['GET'])
def handle_vehiculos():

    vehiculos = Vehiculos.query.all() 
    vehiculos_serialized = list(map(lambda item:item.serialize(), vehiculos))

    response_body = {
        "msg": "OK",
        "data": vehiculos_serialized
    }

    return jsonify(response_body), 200

@app.route('/planetas', methods=['GET'])
def handle_planetas():

    planetas = Planetas.query.all()  
    planetas_serialized = list(map(lambda item:item.serialize(), planetas))

    response_body = {
        "msg": "OK",
        "data": planetas_serialized
    }


    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def create_user():
    
    body = request.json
    me = Personajes(email=body["email"], password=body["password"], is_activer=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }

@app.route('/personajes', methods=['POST'])
def create_personajes():
    
    body = request.json
    me = Personajes(name=body["name"], eye_color=body["eye_color"], hair_color=body["hair_color"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }

@app.route('/vehiculos', methods=['POST'])
def create_vehiculos():
    
    body = request.json
    me = Vehiculos(name=body["name"], model=body["model"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }


    return jsonify(response_body), 200

@app.route('/planetas', methods=['POST'])
def create_planetas():
    
    body = request.json
    me = Planetas(name=body["name"], population=body["population"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }


    return jsonify(response_body), 200

@app.route('/planetas/<int:planeta_id>', methods=['DELETE'])
def delete_planeta(planeta_id):
    
    user = Planetas.query.filter_by(id=planeta_id).first()
    if not user:
        response_body = {
            "error": "Planet not found",
        }
        return jsonify(response_body), 400
    
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }
    
    return jsonify(response_body), 200

@app.route('/personajes/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):
    
    user = Personajes.query.filter_by(id=personaje_id).first()
    if not user:
        response_body = {
            "error": "Personaje not found",
        }
        return jsonify(response_body), 400
    
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }


    return jsonify(response_body), 200

@app.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo(vehiculo_id):
    
    user = Vehiculos.query.filter_by(id=vehiculo_id).first()
    if not user:
        response_body = {
            "error": "Vehiculot not found",
        }
        return jsonify(response_body), 400
    
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_body = {
            "error": "User not found",
        }
        return jsonify(response_body), 400
    
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "OK",
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
