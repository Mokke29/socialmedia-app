from urllib import response
from database import db
from flask import Blueprint, request, jsonify, make_response
from util import user_util
from models import user_model, profile_model
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import os

user_route = Blueprint("user_route", __name__, static_folder="static")

@user_route.post('/follow')
@jwt_required()
def follow():
    user_id = get_jwt_identity()
    data = request.get_json()
    profile = profile_model.Profile.query.filter_by(profile_name=data['profile']).first()
    if profile: 
        user_util.follow(user_id=user_id, profile_to_follow=profile)
        return jsonify({"msg": f"You followed user #{profile.profile_name}"})
    else:
        return jsonify('Something went wrong, please try again later...')

@user_route.post('/unfollow')
@jwt_required()
def unfollow():
    user_id = get_jwt_identity()
    data = request.get_json()
    profile = profile_model.Profile.query.filter_by(profile_name=data['profile']).first()
    if profile: 
        user_util.unfollow(user_id=user_id, profile_to_unfollow=profile)
        return jsonify({"msg": f"You unfollowed user #{profile.profile_name}"})
    else:
        return jsonify('Something went wrong, please try again later...')
