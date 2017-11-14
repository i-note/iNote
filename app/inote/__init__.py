from flask import Blueprint

inote = Blueprint('inote',__name__,static_folder='static',template_folder='templates')


from . import views