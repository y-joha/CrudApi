from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from enum import Enum
import datetime
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
# to run this thing write this
# sudo docker.compose up --build flask_app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class System(Enum):
    Fuel = 'Fuel'
    Cooling = 'Cooling'
    Engine_Top_End = 'Engine_Top_End'
    Clutch = 'Clutch'
    Engine_Lub = 'Engine_Lub'
    Wheels_Tires = 'Wheels_Tires'
    Final_Drive = 'Final_Drive'
    Brakes = 'Brakes'
    Suspension = 'Suspension'
    Steering = 'Steering'
    Electrical = 'Electrical'
    Other = 'Other'

class Brand(Enum):
    Kawasaki = 'Kawasaki'
    Suzuki = 'Suzuki'
    Yamaha = 'Yamaha'
    Honda = 'Honda'

class Model_Name(Enum):
    Ninja = 'Ninja'
    Z = 'Z'
    
#Brand = Enum('Brand', ['Kawasaki', 'Suzuki', 'Yamaha','Honda'])
#Model_Name = Enum('Model', ['Ninja','Z'])

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    def json(self):
        return{
            'id' : self.id, 
            'username' : self.username, 
            'email' : self.email, 
        }

class Rider(db.Model):
    __tablename__ = 'riders'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    brand = db.Column(db.Enum(Brand),nullable=False)
    model = db.Column(db.Enum(Model_Name),nullable=False)
    km = db.Column(db.Integer, nullable=False)
    year = db.Column(db.DateTime, nullable=False)
    def json(self):
        return{
            'id' : self.id, 
            'username' : self.username, 
            'email' : self.email, 
            'brand' : self.brand,
            'model' : self.model,
            'km' : self.km,
            'year' : self.year.isoformat()
        }
    
class Tool(db.Model):
    __tablename__ = 'tools'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    
    def json(self):
        return{'id' : self.id, 'name' : self.name}
    
class Part(db.Model):
    __tablename__ = 'parts'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120),unique=True,nullable=False)
    system=db.Column(db.Enum(System),unique=True,nullable=False)
    torque=db.Column(db.Float,unique=True,nullable=False)
    remarks=db.Column(db.String(20),unique=True,nullable=False)
    part_makat=db.Column(db.Integer,unique=True,nullable=True)
    
    def json(self):
        return{
            'id' : self.id, 
            'name' : self.name, 
            'system' : self.system, 
            'torque' : self.torque,
            'remarks' : self.remarks,
            'part_makat' : self.part_makat,
            }
    
db.create_all()

#    RIDER METHODS *****************#
#create a rider for the table
@app.route('/riders', methods=['POST'])
def create_rider():
    try:
        data = request.get_json()
        new_rider = Rider(
            username=data['username'],
            email=data['email'],
            brand=data['brand'],
            model=data['model'],
            km=data['km'],
            year=datetime.datetime.strptime(data['year'], '%Y/%m').date()
        )
        db.session.add(new_rider)
        db.session.commit()
        return make_response(jsonify({'message' : 'New Rider added to List'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating new rider'}) , 500)

#get all registered rides
@app.route('/riders', methods=['GET'])
def list_riders():
    try:
        riders = Rider.query.all()
        return make_response(jsonify([rider.json() for rider in riders]),200)
    except Exception as e:
        return make_response(jsonify({'message' :'error getting riders'}),500)

#get a rider by id
@app.route('/riders/<int:id>', methods=['GET'])
def get_rider(id):
    try:
        rider = Rider.query.filter_by(id=id).first()
        if rider:
            return make_response(jsonify({'rider' : rider.json()}),200)
        return make_response(jsonify({'rider' : 'rider not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error getting rider'}),500)

# update a rider
@app.route('/riders/<int:id>', methods=['PUT'])
def update_rider(id):
    try:
        rider = Rider.query.filter_by(id=id).first()
        if rider:
            data = request.get_json()
            rider.username = data['username']
            rider.email = data['email']
            rider.brand=data['brand']
            rider.model=data['model']
            rider.km=data['km']
            rider.year=data['year']
            db.session.commit()
            return make_response(jsonify({'message' : 'rider updated'}),200)
        return make_response(jsonify({'message' : 'rider not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error updating rider'}),500)

#delete rider from the db
@app.route('/riders/<int:id>',methods=['DELETE'])
def delete_rider(id):
    try:
        rider = Rider.query.filter_by(id=id).first()
        if rider:
            db.session.delete(rider)
            db.session.commit()
            return make_response(jsonify({'message' : 'rider deleted'}),200)
        return make_response(jsonify({'message' : 'rider not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error deleting rider'}),500)

#    Parts METHODS *****************#
#create part specific to model
@app.route('/parts', methods=['POST'])
def create_parts():
    try:
        data = request.get_json()
        new_parts = Part(
            name=data['name'],
            system=data['system'],
            torque=data['torque'],
            remarks=data['remarks'],
            part_makat=data['part_makat'],
        )
        db.session.add(new_parts)
        db.session.commit()
        return make_response(jsonify({'message' : 'New Part added to List'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating new part'}) , 500)

#get all registered parts
@app.route('/parts', methods=['GET'])
def get_parts():
    try:
        parts = Part.query.all()
        return make_response(jsonify([part.json() for part in parts]),200)
    except Exception as e:
        return make_response(jsonify({'message' :'error getting parts'}),500)

#    User METHODS *****************#

#create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'],email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'new_user created successfully'}),201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating new user'}) , 500)
    
#get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]),200)
    except Exception as e:
        return make_response(jsonify({'message' :'error getting users'}),500)
    
#get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user' : user.json()}),200)
        return make_response(jsonify({'user' : 'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error getting user'}),500)
        
# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message' : 'user updated'}),200)
        return make_response(jsonify({'message' : 'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error updating user'}),500)

#delete user from the db
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message' : 'user deleted'}),200)
        return make_response(jsonify({'message' : 'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message' : 'error deleting user'}),500)