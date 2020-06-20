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

# @app.route('/api/create_content/<vk_id>/<title>/<body>/<tag>', methods=['GET', 'POST'])
# def get_create_content(vk_id, title, body, tag):
#     # create content
#     user = User.query.filter(User.vk_id == vk_id).first()
#     content = Content(
#         title=title, 
#         body=body, 
#         author=user, 
#         )
#     #Content.tags.append(Tag.query.filter_by(name=tag).first())
#     db.session.add(Content)
#     db.session.commit()
#     return jsonify({'content': [{'id': content.id, 'title': content.title, 'body': content.body}]})

@app.route('/api/users', methods=['GET', 'POST'])
def get_all_users():
    # select all users - author of content
    users = User.query.all()
    all_users_list = []
    for user in users:
        all_users_list.append({'id': user.id, 'email': user.vk_id})
    return jsonify({'users': [all_users_list]})

@app.route('/api/user/<vk_id>', methods=['GET', 'POST'])
def get_user(vk_id):
    # select user and his content by id
    user = User.query.filter_by(vk_id=vk_id).first_or_404()
    contents = user.content.order_by(Content.created.desc()).all()
    all_user_contents = []
    for content in contents:
        for tag in content.tags:
            print(tag)
            all_user_contents.append(
                {'id': content.id, 'title': content.title, 'tag': tag.name, 'tagslug': tag.slug})
    return jsonify(
        {'user': [{'vk_id': user.vk_id}]}, 
        {'content': [all_user_contents]}
        )

@app.route('/api/contents', methods=['GET', 'POST'])
def select_contents():
    # select all contents of all users
    contents = Content.query.all()
    all_contents_list = []
    for content in contents:
        all_contents_list.append({'id': content.id, 'title': content.title, 'slug': content.slug})
    return jsonify({'contents': [all_contents_list]})

@app.route('/api/content/<id>', methods=['GET', 'POST'])
def select_content(id):
    # select all contents of all users
    content = Content.query.filter_by(id=id).first_or_404()
    return jsonify(
        {'contents': [{'id': content.id, 'title': content.title, 'slug': content.slug, 'body': content.body}]})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
