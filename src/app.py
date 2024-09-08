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



@app.route('/user', methods=['POST'])
def create_user():
    body = request.json
    me = User(email=body["email"], password=body["password"], is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": me.id
    }

    return jsonify(response_body), 200 


@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))

    response_body = {
        "msg": "OK",
        "data": users_serialized
    }

    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_serialize = user.serialize()

    response_body = {
        "msg": "Ok",
        "data": user_serialize
    }

    return jsonify(response_body), 200



@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():
    users = User.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))

    response_body = {
        "msg": "OK",
        "data": users_serialized
    }

    return jsonify(response_body), 200


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200





@app.route('/favorite/personaje/<int:personaje_id>', methods=['POST'])
def create_personaje():
    body = request.json
    me = Personajes(name=body["name"], eye_color=body["eye_color"], hair_color=body["hair_color"], is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": me.id
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



@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_personaje_by_id(personaje_id):
    personaje = Personajes.query.filter_by(id=personaje_id).first()
    personaje_serialize = personaje.serialize()

    response_body = {
        "msg": "Ok",
        "data": personaje_serialize
    }

    return jsonify(response_body), 200



@app.route('/favorite/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_personaje_by_id(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje is None:
        return "Personaje not found", 404

    db.session.delete(personaje)
    db.session.commit()
    response_body = {

        "msg": "Personaje deleted",

    }

    return jsonify(response_body), 200



@app.route('/favorite/vehiculo/<int:vehiculo_id>', methods=['POST'])
def create_vehiculo():
    body = request.json
    me = Vehiculos(name=body["name"], model=body["model"],  is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": me.id
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



@app.route('/vehiculo/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo_by_id(vehiculo_id):
    vehiculo = Vehiculos.query.filter_by(id=vehiculo_id).first()
    vehiculo_serialize = vehiculo.serialize()

    response_body = {
        "msg": "Ok",
        "data": vehiculo_serialize
    }

    return jsonify(response_body), 200



@app.route('/favorite/vehiculo/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo_by_id(vehiculo_id):
    vehiculo = Vehiculos.query.get(vehiculo_id)
    if vehiculo is None:
        return "Vehiculo not found", 404

    db.session.delete(vehiculo)
    db.session.commit()
    response_body = {

        "msg": "Vehiculo deleted",

    }

    return jsonify(response_body), 200



@app.route('/favorite/planeta/<int:planeta_id>', methods=['POST'])
def create_planeta():
    body = request.json
    me = Planetas(name=body["name"], population=body["population"],  is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": me.id
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


@app.route('/planeta/<int:planeta_id>', methods=['GET'])
def get_planeta_by_id(planeta_id):
    planeta = Planetas.query.filter_by(id=planeta_id).first()
    planeta_serialize = planeta.serialize()

    response_body = {
        "msg": "Ok",
        "data": planeta_serialize
    }

    return jsonify(response_body), 200



@app.route('/favorite/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_planeta_by_id(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta is None:
        return "Planeta not found", 404

    db.session.delete(planeta)
    db.session.commit()
    response_body = {

        "msg": "Planeta deleted",

    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)