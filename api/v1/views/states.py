from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

@app_views.route("/states", strict_slashes=False)
def states(methods=["GET", "POST"]):
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(State).values()])
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<id>", strict_slashes=False)
def states_with_id(id, methods=["GET", "DELETE", "PUT"]):
    state = storage.get(State, id)
    if not state:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        storage.delete(state)
        return jsonify({})
    else:
        updates = request.get_json(silent=True)
        if updates is None:
            abort(400, description="Not a JSON")
        immutable_fields = ["id", "created_at", "updated_at"]
        for field in immutable_fields:
            if field in updates:
                del updates[field]
        state.__dict__.update(updates)
        storage.save()
        return state
