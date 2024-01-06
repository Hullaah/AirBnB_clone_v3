#!/usr/bin/python3
"""
The implementation of the amenities api endpoint
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET", "POST"])
def amenities():
    """view for amenities endpoint"""
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(Amenity).values()])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenities_with_id(id):
    """view for amenities with id endpoint"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        amenity.delete()
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
            setattr(amenity, k, v)
        amenity.save()
        return jsonify(storage.get(Amenity, id).to_dict())
