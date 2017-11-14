from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_babel import Babel
from flask_nav import Nav
from flask_login import LoginManager
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from flask_moment import Moment
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()

babel = Babel()
mail = Mail()
moment = Moment()

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'auth.login'



def create_app(config_name):
    global app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    Markdown(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    from .inote import inote as inote_blueprint
    app.register_blueprint(inote_blueprint, url_prefix='/inote')
    #
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
