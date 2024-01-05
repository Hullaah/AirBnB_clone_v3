#!/usr/bin/python3
'''
Creates a blueprint for the app views
'''
from flask import Flask, Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
