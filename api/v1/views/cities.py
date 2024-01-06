#!/usr/bin/python3
"""
The implementation of the cities api endpoint
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET", "POST"])
def cities(state_id):
    """view for cities endpoint"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify([x.to_dict() for x in state.cities])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    city = City(**data, state_id=state_id)
    storage.new(city)
    state.cities.append(city)
    storage.save()
    return jsonify({x: y for x, y in city.to_dict().items() if x != 'state'}), 201


@app_views.route("/cities/<id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def cities_with_id(id):
    """view for cities with id endpoint"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
    else:
        updates = request.get_json(silent=True)
        if updates is None:
            abort(400, description="Not a JSON")
        immutable_fields = ["id", "created_at", "updated_at"]
        for field in immutable_fields:
            if field in updates:
                del updates[field]
        for k, v in updates.items():
            setattr(city, k, v)
        city.save()
        return jsonify(storage.get(City, id).to_dict())
