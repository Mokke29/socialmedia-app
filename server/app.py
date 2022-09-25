from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from flask_jwt_extended import JWTManager
from datetime import timedelta
from database import db
from views import user_route, auth_route, post_route, refresh_route, profile_route, comment_route

app = Flask(__name__)
# Config file
app.config.from_file("config.json", load=json.load)

app.config["CORS_SUPPORTS_CREDENTIALS"] = True
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["CORS_ORIGINS"] = "http://localhost:3000"

CORS(app)

# Routes
app.register_blueprint(user_route.user_route, url_prefix="/user")
app.register_blueprint(auth_route.auth_route, url_prefix="/auth")
app.register_blueprint(post_route.post_route, url_prefix="/post")
app.register_blueprint(comment_route.comment_route, url_prefix="/comment")
app.register_blueprint(refresh_route.refresh_route, url_prefix="/refresh")
app.register_blueprint(profile_route.profile_route, url_prefix="/profile")

db.init_app(app)

jwt = JWTManager(app)

# JWT time config
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)  # 1 h
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)  # 15 days


@app.get('/db')
def get_db():
    db.create_all()
    return jsonify("DB -> create_all")


if __name__ == '__main__':
    app.run()
    db.create_all()
