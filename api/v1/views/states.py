#!/usr/bin/python3
'''
Defines the state view for the api
'''
from flask import jsonify, abort, make_response, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def get_state(state_id=None):
    """returns a state if id is given or returns all states"""
    states_dict = storage.all(State)
    if state_id is None:
        states = [state.to_dict() for state in states_dict.values()]
        return jsonify(states)
    else:
        state_obj = states_dict.get("State.{}".format(state_id), None)
        if state_obj is None:
            abort(404)
        else:
            return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_state(state_id=None):
    """deletes a state given the id"""
    states_dict = storage.all(State)
    state_obj = states_dict.get("State.{}".format(state_id), None)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """creates a new state"""
    json_req = request.get_json()
    if json_req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in json_req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_state = State(**json_req)
        new_state.save()
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["PUT"])
def update_state(state_id=None):
    """updates a state given the id"""
    states_dict = storage.all(State)
    state_obj = states_dict.get("State.{}".format(state_id), None)
    if state_obj is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key in json_req:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, json_req[key])
            state_obj.save()
    return make_response(jsonify(state_obj.to_dict()), 200)
