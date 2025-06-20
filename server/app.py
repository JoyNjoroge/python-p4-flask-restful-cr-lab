#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# GET /plants
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [{
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        } for plant in plants]
        return plant_list, 200

    # POST /plants
    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )

        db.session.add(new_plant)
        db.session.commit()

        plant_data = {
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': new_plant.price
        }

        return plant_data, 201


# GET /plants/<id>
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        }
        return plant_data, 200


# Link resources to routes
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
