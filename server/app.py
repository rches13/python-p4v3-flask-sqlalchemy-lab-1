# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the Earthquake by its id
    earthquake = Earthquake.query.get(id)
    
    # Check if the earthquake exists
    if earthquake:
        # Serialize the earthquake data to JSON
        return jsonify({
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }), 200
    else:
        # Return a message with the earthquake id if not found
        return jsonify({'message': f'Earthquake {id} not found.'}), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query all earthquakes with magnitude >= the provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Create a list of dictionaries with earthquake data
    quakes_list = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]

    # Return the JSON response with the count and quakes data
    return jsonify({
        'count': len(quakes_list),
        'quakes': quakes_list
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
