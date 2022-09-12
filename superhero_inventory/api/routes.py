from flask import Blueprint, request, jsonify
from superhero_inventory.helpers import token_required
from superhero_inventory.heroes import db,User,Superhero,hero_schema,heros_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}


# CREATE Superhero ENDPOINT
@api.route('/superhero', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics = request.json['comics']
    power = request.json['power']
    date_created = request.json['date_created']
    owner = request.json['owner']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    hero = Superhero(name,description,comics,power,date_created,owner,user_token = user_token )

    db.session.add(hero)
    db.session.commit()

    response = heros_schema.dump(hero)
    return jsonify(response)




# RETRIEVE ALL Superhero ENDPOINT
@api.route('/superheros', methods = ['GET'])
@token_required
def get_superheros(current_user_token):
    owner = current_user_token.token
    superhero = Superhero.query.filter_by(user_token = owner).all()
    response = heros_schema.dump(superhero)
    return jsonify(response)


# RETRIEVE ONE Superhero ENDPOINT
@api.route('/superhero/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Superhero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE HERO ENDPOINT
@api.route('/superhero/<id>', methods = ['POST','PUT'])
@token_required
def update_hero(current_user_token,id):
    hero = Superhero.query.get(id) # GET HERO INSTANCE

    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comics = request.json['comics']
    hero.power = request.json['power']
    hero.date_created = request.json['date_created']
    hero.owner = request.json['owner']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


# DELETE HERO ENDPOINT
@api.route('/superhero/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Superhero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)