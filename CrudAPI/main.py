from flask import Flask, request
from flask_restful import Api , Resource


app = Flask(__name__)
api = Api(app)

names = {"yohai": {"brand": "Kawasaki", "model": "Z650", "Km": 34000},
        "shuki": {"brand": "Kawasaki", "model": "Ninja400", "Km": 18000}}
        


class Tipol(Resource):
    def get(self, name):
        return names[name]
    
    def put(self, name):
        print(request.form['treatment'])
        return {}
    
api.add_resource(Tipol, "/<string:name>/<string:treatment>")

#only for testing purposes
if __name__ == '__main__':
    app.run(debug=True)