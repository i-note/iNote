from flask import Blueprint

inote = Blueprint('inote', __name__)

from . import views
