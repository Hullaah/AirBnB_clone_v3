from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from sqlalchemy import update


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states():
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(State).values()])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def states_with_id(id):
    state = storage.get(State, id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        state.delete()
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
        update(State).where(State.id==id).values(updates)
        storage.save()
        return jsonify(storage.get(State, id).to_dict())
