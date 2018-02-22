from flask import Blueprint
from .inject import BlogInject

blog = Blueprint('blog', __name__, static_folder='static',
                 template_folder='templates')

from . import views