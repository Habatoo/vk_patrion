import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_restful import Resource,  Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required
from flask_cors import CORS

from config import config

app = Flask(__name__)
app.config.from_object(config.get('dev'))

db  = SQLAlchemy(app)

# app.config['JWT_SECRET_KEY'] = 'hj67#28mnHJGT67#2degn'
jwt = JWTManager(app)
CORS(app)
api = Api(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login = LoginManager(app)
login.login_view = 'login'

######## logger ###################
log = logging.getLogger('btb_Api')
fh = logging.FileHandler(app.config['LOGGER_CONFIG']['file'])
fh.setLevel(app.config['LOGGER_CONFIG']['level'])
fh.setFormatter(app.config['LOGGER_CONFIG']['formatter'])
log.addHandler(fh)
log.setLevel(app.config['LOGGER_CONFIG']['level'])
###################################

from app import view
from app.models import *

# #### ADMIN ####
admin = Admin(app)
admin.add_view(ModelView(Content, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tag, db.session))

