from app import app
from app import db
from app import log
from app import api

from flask import make_response
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

from app.models import *

@app.route('/')
def index():
    return "Test vk"

# api.add_resource(UserLogin, '/api/login/')
# api.add_resource(ProtectArea, '/api/protect-area/')

@app.route('/api/users', methods=['GET', 'POST'])
def get_all_users():
    users = User.query.all()
    all_users_list = []
    for user in users:
        all_users_list.append({'id': user.id, 'email': user.email})
    return jsonify({'users': all_users_list})

@app.route('/api/users/<tag>', methods=['GET', 'POST'])
def get_users_bytags(task_id):
    pass

@app.route('/api/user/<int:user_id>', methods=['GET', 'POST'])
def get_user(task_id):
    pass

@app.route('/api/contents', methods=['GET'])
def select_all_contents():
    pass

@app.route('/api/content/<tag>', methods=['GET'])
def select_content():
    pass

@app.route('/api/content', methods=['POST'])
def create_content():
    pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
