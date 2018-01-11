import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    host = "0.0.0.0"
    port = 5000
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'os.urandom(24)'
    DEBUG = True
    INOTE_POSTS_PER_PAGE = 10

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3.db')

class LisukeDevConfig(BaseConfig):
    host = "0.0.0.0"
    port = 80
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3.db')
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '1573630389@qq.com'
    MAIL_PASSWORD = 'dreqneeqrytzgggi'
    INOTE_MAIL_SUBJECT_PREFIX = '[iNote]'
    INOTE_MAIL_SENDER = 'iNote Admin <1573630389@qq.com>'
    INOTE_ADMIN = '1573630389@qq.com'
    SERVER_NAME = 'lisuke.cf'



config = {
    'development': DevelopmentConfig,
    'lisuke-dev':LisukeDevConfig,
    'default': DevelopmentConfig
}
