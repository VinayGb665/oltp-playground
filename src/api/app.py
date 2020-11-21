import os
import random
import time
from flask.views import MethodView
from flask_rest_api import Api, Blueprint
import marshmallow as ma

from flask import (
    Flask,
    request,
    render_template,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from celery import Celery


class Config:
    OPENAPI_URL_PREFIX = "/doc"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_URL = "/swagger"
    API_SPEC_OPTIONS = {"x-internal-id": "2"}
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


app = Flask(__name__)

# Celery configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

app.config["UPLOAD_FOLDER"] = "downloads"
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/doc"
app.config["OPENAPI_REDOC_PATH"] = "/redoc"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_URL"] = "/swagger"

# Initialize extensions

# Initialize Celery
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
# celery.autodiscover_tasks()
celery.conf.update(app.config)


api = Api(app)
