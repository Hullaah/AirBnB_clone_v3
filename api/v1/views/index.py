#!/usr/bin/python3
'''

Creates a status view for the flask application
uses the blueprint defined in __init__

'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def view_status():
    """views status of the api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def view_statistics():
    """returns the couhnt of the objects available"""
    obj_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(obj_dict)
