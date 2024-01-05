#!/usr/bin/python3
'''
Creates a status view for my flask application
'''
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def view_status():
    """views status of the api"""
    return jsonify({"status": "OK"})
