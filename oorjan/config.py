import os
import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'oorjan.log'
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1111@localhost/SOLAR_DATA'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


config = {
    "development": "app.config.DevelopmentConfig",
    "testing": "app.config.TestingConfig",
    "default": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig"
}


def configure_app(app):
    # config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    # app.config.from_object(config[config_name])
    # app.config.from_envvar('FLASK_CONFIG')
    DEBUG = True
    TESTING = False
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'oorjan.log'
    LOGGING_LEVEL = logging.DEBUG
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111@localhost/SOLAR_DATA'

    # Configure logging
    handler = logging.FileHandler(LOGGING_LOCATION)
    handler.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter(LOGGING_FORMAT)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # JOBS FOR Alerting Service
    JOBS = [
        {
            'id': 'job2',
            'func': 'oorjan.emails:job2',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 3600
        }
    ]
    app.config['JOBS'] = JOBS
    # Setting Up Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['DEFAULT_MAIL_SENDER'] = 'ishaansutaria@gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ishaansutaria@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xxxxxxx'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
