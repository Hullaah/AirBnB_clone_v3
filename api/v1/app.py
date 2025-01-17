#!/usr/bin/python3
'''

A flask app to show the status
of the flask app

'''
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0", resources=r"/*")


@app.errorhandler(404)
def not_found_error(error):
    """custom 404 message"""
    return make_response(jsonify({
        "error": "Not found"
    }), 404)


@app.errorhandler(400)
def client_error(error):
    """handles client error"""
    return jsonify({"error": error.description}), 400


@app.teardown_appcontext
def teardown(x):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = int(getenv("HBNB_API_PORT", default=5000))
    app.run(host=host, port=port, threaded=True)
