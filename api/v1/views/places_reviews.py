#!/usr/bin/python3
"""
The implementation of the reviews api endpoint
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def reviews(place_id):
    """view for reviews endpoint"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify([x.to_dict() for x in place.reviews])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("text") is None:
        abort(400, "Missing text")
    if data.get("user_id") is None:
        abort(400, description="Missing user_id")
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    review = Review(**data, place_id=place_id)
    storage.new(review)
    place.reviews.append(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def reviews_with_id(id):
    """view for reviews with id endpoint"""
    review = storage.get(Review, id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})
    else:
        updates = request.get_json(silent=True)
        if updates is None:
            abort(400, description="Not a JSON")
        immutable_fields = ["id", "created_at",
                            "updated_at", "place_id", "user_id"]
        for field in immutable_fields:
            if field in updates:
                del updates[field]
        for k, v in updates.items():
            setattr(review, k, v)
        review.save()
        return jsonify(storage.get(Review, id).to_dict())
