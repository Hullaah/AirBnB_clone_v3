#!/usr/bin/python3
'''

This is the implementation of the user routes for
the AirBnB project API

'''
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users():
    """view for users endpoint"""
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(User).values()])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    if data.get("password") is None:
        abort(400, "Missing password")
    if data.get("email") is None:
        abort(400, "Missing email")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def users_with_id(id):
    """view for users with id endpoint"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({})
    else:
        updates = request.get_json(silent=True)
        if updates is None:
            abort(400, description="Not a JSON")
        immutable_fields = ["id", "created_at", "updated_at", "email"]
        for field in immutable_fields:
            if field in updates:
                del updates[field]
        for k, v in updates.items():
            setattr(user, k, v)
        user.save()
        return jsonify(storage.get(User, id).to_dict())
