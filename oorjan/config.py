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


config = {
    "development": "app.config.DevelopmentConfig",
    "testing": "app.config.TestingConfig",
    "default": "app.config.DevelopmentConfig"
}


def configure_app(app):
    # config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    # app.config.from_object(config[config_name])
    # app.config.from_envvar('FLASK_CONFIG')
    DEBUG = True
    TESTING = False
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'oorjan1.log'
    LOGGING_LEVEL = logging.DEBUG
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111@localhost/SOLAR_DATA'

    # Configure logging
    handler = logging.FileHandler(LOGGING_LOCATION)
    handler.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter(LOGGING_FORMAT)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
