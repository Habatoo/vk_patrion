import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object): 
    DEBUG = False
    DEVELOPMENT = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dgFKT5&md32@rfvnFHTr123f569#jhgfj'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'hj67#28mnHJGT67#2degn'

    LOGGER_CONFIG = dict(level=logging.DEBUG,
                     file="app.log",
                     formatter=logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s:%(message)s")
                     )

class DevConfig(Configuration):
    DEBUG = True
    DEVELOPMENT = True

class ProdConfig(Configuration):
    DEBUG = False
    DEVELOPMENT = False

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': Configuration,
}            