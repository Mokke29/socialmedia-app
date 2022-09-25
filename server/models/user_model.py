from database import db
from models import profile_model, following_model
import os


class User(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=False)

    posts = db.relationship("Post", backref='created_by')
    profile = db.relationship("Profile", backref='profile_owner')

    followed_by = db.relationship(
        "Following", backref='user', foreign_keys='Following.user_id')
    followers = db.relationship(
        "Following", backref='follower', foreign_keys='Following.follower_id')
    comment = db.relationship(
        "Comment", backref='created_by', foreign_keys='Comment.user_id')

    def delete(self):
        try:
            user = User.get_by_id(self.user_id)
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def create(cls, username, password):
        try:
            if User.query.filter_by(username=username).first():
                print(f"User already exists #{username}")
                return False
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                created_user = User.get_by_username(new_user.username)
                new_profile = profile_model.Profile(
                    description="", avatar_path="user.png", profile_name=username, user_id=created_user.user_id)
                db.session.add(new_profile)
                db.session.commit()
                return new_user.username
        except Exception as e:
            print(f"Database error... {e}")
            return False

    @classmethod
    def get_by_id(cls, id):
        user = User.query.get(id)
        return user

    @classmethod
    def get_by_username(cls, username):
        user = User.query.filter_by(username=username).first()
        return user
