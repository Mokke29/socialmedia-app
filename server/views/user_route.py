from urllib import response
from database import db
from flask import Blueprint, request, jsonify, make_response
from models import user_model, profile_model
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import os

user_route = Blueprint("user_route", __name__, static_folder="static")


@user_route.post('/create')
def create_user():
    data = request.get_json()
    new_user = user_model.User.create(data['username'], data['password'])
    if new_user:
        usr = user_model.User.get_by_username(new_user)
        access_token = create_access_token(identity=usr.user_id, fresh=True)
        refresh_token = create_refresh_token(usr.user_id)
        response = make_response(
            {"err": False, 'msg': f'New user created #{new_user}'})
        response.set_cookie('access_token_cookie',
                            access_token, secure=True, samesite='None')
        response.set_cookie('refresh_token_cookie',
                            refresh_token, secure=True, samesite='None')
        response.headers.add('Access-Control-Allow-Headers',
                             'x-www-form-urlencoded, Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response
    else:
        return jsonify(err=True, msg='User already exists...')


@user_route.delete('/delete')
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = user_model.User.get_by_id(user_id)
    if user.delete():
        return jsonify('User deleted successfully!')
    else:
        return jsonify('Something went wrong, please try again later...')
