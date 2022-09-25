from database import db
from flask import Blueprint, make_response, request, jsonify
from datetime import datetime
from util import util
from models import profile_model, post_model, user_model, comment_model
import os
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

comment_route = Blueprint("comment_route", __name__, static_folder="static")

images_dir = os.path.join(os.getcwd(), 'static/posts')


@comment_route.post('/create')
@jwt_required()
def create_comment():
    user_id = get_jwt_identity()
    data = request.get_json()
    comment_model.Comment.create_comment(content=data.get(
        "content"), post_id=data.get("post_id"), user_id=user_id)
    return 200


@comment_route.post('/delete')
@jwt_required()
def delete_comment():
    user_id = get_jwt_identity()
    data = request.get_json()
    comment = comment_model.Comment.Comment.query.filter_by(
        id=data.get("comment_id")).first()
    if user_id == comment.user_id:
        db.session.delete(comment)
        db.session.commit()
        return 200
    else:
        return 500


@comment_route.post('/reply')
@jwt_required()
def create_new_reply():
    user_id = get_jwt_identity()
    data = request.get_json()
    comment_model.Comment.create_reply(content=data.get("content"), post_id=data.get(
        "post_id"), user_id=user_id, comment_id=data.get("comment_id"))
    return 200


@comment_route.post('/get/<page>')
@jwt_required()
def get_all_comments(page):
    user_id = get_jwt_identity()
    data = request.get_json()
    comment_arr = []
    if data.get('post_id'):
        print("GET COMMENTS")
        comments = comment_model.Comment.query.filter_by(
            post_id=data.get('post_id')).all()
        print(len(comments))
        if (page == 0):
            page_start = 0
        else:
            page_start = page*3-1
        page_comments = comments[page_start:page_start+2]
        for c in page_comments:
            print(c)
    return jsonify({"comments": comment_arr})
