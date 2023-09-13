from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

# Add car to inventory 
@api.route('/inventory', methods = ['POST'])
@token_required
def add_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make,model,year,color,user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Call entire inventory
@api.route('/inventory', methods = ['GET'])
@token_required
def get_inventory(current_user_token):
    a_user = current_user_token.token
    inventory = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(inventory)
    return jsonify(response)

# Call single car from inventory
@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# Update car in inventory
@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete car from inventory
@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)