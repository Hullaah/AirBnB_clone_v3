#!/usr/bin/python3
'''

Creates a status view for the flask application
uses the blueprint defined in __init__

'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def view_status():
    """views status of the api"""
    return jsonify({"status": "OK"})
