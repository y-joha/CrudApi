from flask import Flask,request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from enum import Enum
import datetime
import requests


# Define the API endpoint URL
base_url = 'https://data.gov.il/api/3/action/datastore_search?'

# Define the parameters for the search
resource_id = 'bf9df4e2-d90d-4c0a-a400-19e15af8e95f'  # Your resource ID
limit = 1  # Number of records to retrieve
  # Replace with the actual mispar_rehev value you're looking for

# Construct the complete URL with parameters


# Make a GET request to the API endpoint




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motor_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '46acc08d62e83091a75833cb80b6796d127a1103ad58d49be54e62d5f0381942'
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
    

    

class Rider(db.Model, UserMixin):
    __tablename__ = 'riders'
    
    id = db.Column(db.Integer, primary_key=True)
    rider_name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    license_plate = db.Column(db.Integer, unique=True, nullable=False)
    brand = db.Column(db.Enum(Brand),nullable=False)
    model = db.Column(db.String(40),nullable=False)
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

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(),
        Length(min=4, max=100)],render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(),
        Length(min=4, max=20)],render_kw={"placeholder":"Password"})
    
    submit = SubmitField("Register")
    
    def validate_email(self, email):
        existing_email = Rider.query.filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError(
                "HEY Buddy, This Email is Allready Taken!.")


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(),
            Length(min=4, max=100)],render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(),
        Length(min=4, max=20)],render_kw={"placeholder":"Password"})
    
    submit = SubmitField("Login")

  
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
        # Make a GET request to the API endpoint
        data = request.get_json()
        query = data['license_plate']
        url = f'{base_url}resource_id={resource_id}&limit={limit}&q={query}'
        response = requests.get(url)
        url_data = response.json()
        records = url_data['result']['records']
        new_rider = Rider(
            rider_name=data['rider_name'],
            email=data['email'],
            license_plate=records[0]['mispar_rechev'],
            brand=data['brand'],
            model=records[0]['degem_nm'],
            km=data['km'],
            year=datetime.datetime.strptime(records[0]['moed_aliya_lakvish'], '%Y-%m').date()
        )
        

        db.session.add(new_rider)
        db.session.commit()
        return make_response(jsonify({'message' : 'New Rider added to List'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating new rider: ' + e.args[0]}) , 500)

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
