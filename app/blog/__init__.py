from flask import Blueprint

blog = Blueprint('blog', __name__, static_folder='static', template_folder='templates')

from . import views
# from .inject.BlogInject import

# iNoteBlogContext.ctx_func_init()
