#!/usr/bin/python3
'''

The init file
creates a blueprint for the app views

'''
from flask import Flask, Blueprint


app_views = Blueprint("app_views", __name__)


from api.v1.views.index import *
