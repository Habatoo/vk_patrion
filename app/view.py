from app import app
from app import db
from app import log
from app import api

from flask import make_response
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

from app.copydir import copydir
from app.models import *

# @app.route('/')
# def index():
#     return "Test vk"

# api.add_resource(UserLogin, '/api/login/')
# api.add_resource(ProtectArea, '/api/protect-area/')

@app.route('/api/create_user/<vk_id>', methods=['GET', 'POST'])
def get_create_user(vk_id):
    # create user
    user = User.query.filter(User.vk_id == vk_id).first()
    if user: 
        return make_response(jsonify({'error': 'User already exists'}), 412)

    user = User(
        vk_id=vk_id,
        )
    db.session.add(user)
    db.session.commit()

    new_user = User.query.filter(User.vk_id == vk_id).first()         
    user_dir = new_user.vk_id
    user_folders = os.path.join('app', 'static', 'user_data', user_dir)
    if not os.path.isdir(user_folders):
        os.mkdir(user_folders)
        os.mkdir(os.path.join(user_folders, 'files'))
    copydir(os.path.join('app', 'static', 'user_data'), user_folders)
    return jsonify({'user': [{'vk_id': user.vk_id}]})

@app.route('/api/users', methods=['GET', 'POST'])
def get_all_users():
    # select all users - author of content
    users = User.query.all()
    all_users_list = []
    for user in users:
        all_users_list.append({'id': user.id, 'email': user.vk_id})
    return jsonify({'users': [all_users_list]})

@app.route('/api/users/<tag>', methods=['GET', 'POST'])
def get_users_bytags(task_id):
    # select all users - author of contents by tags
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
