#!/usr/bin/python3
'''

A flask app to show the status
of the flask app

'''
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(x):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = int(getenv("HBNB_API_PORT", default=5000))
    app.run(host=host, port=port, threaded=True)
