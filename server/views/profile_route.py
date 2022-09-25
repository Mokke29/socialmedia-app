from urllib import response
from database import db
from util import searching
from flask import Blueprint, request, jsonify, make_response
from models import user_model, profile_model, following_model
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import os

profile_route = Blueprint("profile_route", __name__, static_folder="static")


@profile_route.post('/search')
@jwt_required()
def search_profile():
    data = request.get_json()
    print(data['profile'])
    profiles = searching.search_profile(data['profile'])
    return jsonify({"profiles": profiles})


@profile_route.post('/edit')
@jwt_required()
def edit_user_profile():
    user_id = get_jwt_identity()
    profile = profile_model.Profile.query.filter_by(user_id=user_id).first()
    data = request.form
    try:
        if request.files['file'].filename:
            image = request.files['file']
            edit_result = profile.edit_profile(data=data, image=image)
        else:
            edit_result = profile.edit_profile(data=data)
    except Exception as e:
        print(f"/profile/edit $$ {e}")
        edit_result = profile.edit_profile(data=data)
    if edit_result["err"] == False:
        return jsonify("Success!")
    else:
        return jsonify("Something went wrong")

# Fetch user profile after successfull log in


@profile_route.get('/my')
@jwt_required()
def get_info():
    user_id = get_jwt_identity()
    if user_id:
        profile = profile_model.Profile.query.filter_by(
            user_id=user_id).first()
        return jsonify({"description": profile.description, "avatar_path": profile.avatar_path, "profile_name": profile.profile_name})
    else:
        return jsonify('Something went wrong, please try again later...')

# Fetch profile info of currently viewed profile


@profile_route.post('/info')
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    profile = profile_model.Profile.query.filter_by(
        profile_name=data['profile']).first()
    followed = following_model.Following.check_if_followed(
        user_id=user_id, profile_to_check=profile)
    followers = following_model.Following.get_followers(profile=profile)
    if profile:
        return jsonify({"description": profile.description, "avatar_path": profile.avatar_path, "profile_name": profile.profile_name, "followed": followed, "followers": followers})
    else:
        return jsonify('Something went wrong, please try again later...')


@profile_route.get('/suggested')
@jwt_required()
def get_suggested_profiles():
    user_id = get_jwt_identity()
    data = request.get_json()
    profile_arr = []
    # profile = profile_model.Profile.query.filter_by(profile_name=data['profile']).first()
    profiles = profile_model.Profile.query.all()
    for p in profiles:
        if (user_id == p.id):
            print("You")
        else:
            profile_obj = {"id": p.id, "avatar_path": p.avatar_path,
                           "profile_name": p.profile_name}
            profile_arr.append(profile_obj)
    print(profile_arr)
    return jsonify({"profiles":  profile_arr})
