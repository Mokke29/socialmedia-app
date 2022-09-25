from random import random
from database import db
from flask import Blueprint, make_response, request, jsonify
from datetime import datetime
from util import util
from models import profile_model, post_model, user_model, comment_model
import os
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

post_route = Blueprint("post_route", __name__, static_folder="static")

images_dir = os.path.join(os.getcwd(), 'static/posts')


@post_route.post('/create')
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.form
    image = request.files['image']
    new_image = util.id_generator()
    image.filename = new_image + "." + image.filename.split('.')[1]
    if util.file_exists(os.path.join(images_dir, image.filename)):
        new_image = util.id_generator()
        image.filename = new_image + "." + image.filename.split('.')[1]

    image.save(os.path.join(images_dir, image.filename))

    post = post_model.Post(
        content=data['content'], image_path=image.filename, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify('Post added sucessfully!')


@post_route.post('/delete')
@jwt_required()
def delete_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    post = post_model.Post.query.filter_by(id=data["post_id"]).first()
    user = user_model.User.get_by_id(post.user_id)
    if user.user_id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        post_obj = {"message": "Post deleted!"}
    else:
        post_obj = {"message": "Something went wrong!"}
    return jsonify(post_obj)


@post_route.post('/getall')
@jwt_required()
def get_posts():
    user_id = get_jwt_identity()
    data = request.get_json()
    post_arr = []
    profile = profile_model.Profile.query.filter_by(
        profile_name=data['profile']).first()
    posts = post_model.Post.query.filter_by(user_id=profile.user_id).all()
    for p in posts:
        post_obj = {"id": p.id, "image_path": p.image_path,
                    "likes": random.randrange(9000), "comments": 38, "creator": profile.profile_name}
        post_arr.append(post_obj)
    print(post_arr)
    return jsonify({"posts": post_arr})

# Gets all posts from followed profiles


@post_route.get('/get/followed/<page>')
@jwt_required()
def get_followed_posts(page):
    user_id = get_jwt_identity()
    sort = request.args.get('sort')
    print(f"SORT TYPE -> {sort}")
    print(f"PAGE NUMBER -> {page}")
    post_arr = []
    posts = post_model.Post.query.filter_by().all()
    for p in posts:
        profile = profile_model.Profile.query.filter_by(
            user_id=p.user_id).first()
        post_obj = {"id": p.id, "image_path": p.image_path, "likes": 875,
                    "comments": 38, "creator": profile.profile_name, "content": p.content, "avatar": profile.avatar_path}
        post_arr.append(post_obj)
        print(post_arr)
        print(post_arr)
    post_arr.reverse()
    return jsonify({"posts": post_arr})


@post_route.post('/details')
@jwt_required()
def get_post_details():
    user_id = get_jwt_identity()
    data = request.get_json()
    post = post_model.Post.query.filter_by(id=data["id"]).first()
    user = user_model.User.get_by_id(post.user_id)
    profile = profile_model.Profile.query.filter_by(
        user_id=user.user_id).first()
    post_obj = {"content": post.content, "image_path": post.image_path, "likes": 875,
                "comments": 38, "creator": profile.profile_name, "creator_avatar": profile.avatar_path}
    return jsonify(post_obj)
