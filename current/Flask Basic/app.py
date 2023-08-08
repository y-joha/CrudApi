from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from enum import Enum
import datetime
import psycopg2
#first wrote this
# sudo docker.compose up flask_db

#than wrote 
# sudo docker.compose build

#than
## sudo docker.compose up --build flask_app


# to run this thing write this
# sudo docker.compose up --build flask_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motor_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class System(str, Enum):
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

#Change Model And Brand To Be Extarcted From DMV DataBase (Israel)
#initially


class Brand(str, Enum):
    Kawasaki = 'Kawasaki'
    Suzuki = 'Suzuki'
    Yamaha = 'Yamaha'
    Honda = 'Honda'

class Model_Name(str, Enum):
    #Kawasaki
    Ninja = 'Ninja'
    Z = 'Z'
    Versys = 'Versys'
    Vulcan = 'Vulcan'
    H2 = 'H2'
    ZH2 = 'ZH2'
    #Honda
    CB1000R = 'CB1000R'
    CB650R = 'CB650R'
    CB500F = 'CB650F'
    CBR1000RRR = 'CBR1000RRR'
    CBR500R = 'CBR500R'
    CRF300L = 'CRF300L'
    CRF1100 = 'CRF1100'
    #Suzuki
    GSX1300Busa = 'GSX1300Busa'
    GSXS800 = 'GSXS800'
    GSXR1000 = 'GSXR1000'
    SV650ABS = 'SV650ABS'
    DR650SE = 'DR650SE'
    DRZ400S = 'DRZ400S'
    #Yamaha
    YZFR1M = 'YZFR1M'
    YZFR1 = 'YZFR1'
    R7 = 'R7'
    YZFR3 = 'YZFR3'
    MT10 = 'MT10'
    MT9SP = 'MT9SP'
    MT09 = 'MT09'
    MT07 = 'MT07'
    Tracer7 = 'Tracer7'
    Tracer9 = 'Tracer9'
    
    
    

class Rider(db.Model):
    __tablename__ = 'riders'
    
    id = db.Column(db.Integer, primary_key=True)
    rider_name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    license_plate = db.Column(db.Integer, unique=True, nullable=False)
    brand = db.Column(db.Enum(Brand),nullable=False)
    model = db.Column(db.Enum(Model_Name),nullable=False)
    km = db.Column(db.Integer, nullable=False)
    year = db.Column(db.DateTime, nullable=False)
    def json(self):
        return{
            'id' : self.id, 
            'rider_name' : self.rider_name, 
            'email' : self.email, 
            'license_plate' : self.license_plate,
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
    name=db.Column(db.String(250),unique=True,nullable=False)
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
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
#{
#    "rider_name":"Yohai Davitsiotzo",
#    "email":"yohai@thewrong.com",
#    "license_plate" : 414xxx02,
#    "brand":"Kawasaki",
#    "model":"Z",
#    "km": 34000,
#    "year": "2021/10"
#}

  
#    RIDER METHODS *****************#
#create a rider for the table
@app.route('/riders', methods=['POST'])
def create_rider():
    try:
        data = request.get_json()
        new_rider = Rider(
            rider_name=data['rider_name'],
            email=data['email'],
            license_plate=data['license_plate'],
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
            return make_response(jsonify(rider.json()),200)
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
            rider.rider_name = data['rider_name']
            rider.email = data['email']
            rider.license_plate=data['license_plate']
            rider.brand=data['brand']
            rider.model=data['model']
            rider.km=data['km']
            rider.year=datetime.datetime.strptime(data['year'], '%Y/%m').date()
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

#{
#    "name":"Sproket",
#    "system":"Fuel",
#    "torque":14.30,
#    "remarks":"A,L,O",
#    "part_makat": 34000
#}

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

#{
#    "name":"Sproket"
#}


#    TOOLS METHODS *****************#
#create a tool for the table
@app.route('/tools', methods=['POST'])
def create_tool():
    try:
        data = request.get_json()
        new_tool = Tool(
            name=data['name'],
        )
        db.session.add(new_tool)
        db.session.commit()
        return make_response(jsonify({'message' : 'New Tool added to List'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Ein Tool Beseder?? EINNNNN'}) , 500)

    
#get all registered Tools
@app.route('/tools', methods=['GET'])
def get_tools():
    try:
        tools = Tool.query.all()
        return make_response(jsonify([tool.json() for tool in tools]),200)
    except Exception as e:
        return make_response(jsonify({'message' :'error getting tools'}),500)
