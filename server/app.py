#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    db.init_app(app)
    Migrate(app, db)

    @app.route('/')
    def index():
        return jsonify({"message": "Flask SQLAlchemy Lab 1"}), 200

    @app.route('/earthquakes/<int:id>')
    def get_earthquake(id):
        quake = Earthquake.query.get(id)
        if not quake:
            return jsonify({"message": f"Earthquake {id} not found."}), 404
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200

    @app.route('/earthquakes/magnitude/<float:magnitude>')
    def get_quakes_by_magnitude(magnitude):
        quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        return jsonify({
            "count": len(quakes),
            "quakes": [
                {"id": q.id, "location": q.location, "magnitude": q.magnitude, "year": q.year}
                for q in quakes
            ]
        }), 200

    return app

# ✅ Create a global app object for seed.py and tests
app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
