#!/usr/bin/python3
"""
The implementation of the places api endpoint
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET", "POST"])
def places(city_id):
    """view for places endpoint"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify([x.to_dict() for x in city.places])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    if data.get("user_id") is None:
        abort(400, description="Missing user_id")
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    place = Place(**data, user_id=data["user_id"])
    storage.new(place)
    city.places.append(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def places_with_id(id):
    """view for places with id endpoint"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
    else:
        updates = request.get_json(silent=True)
        if updates is None:
            abort(400, description="Not a JSON")
        immutable_fields = ["id", "created_at",
                            "updated_at", "user_id", "city_id"]
        for field in immutable_fields:
            if field in updates:
                del updates[field]
        for k, v in updates.items():
            setattr(place, k, v)
        place.save()
        return jsonify(storage.get(Place, id).to_dict())
