from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from database import db
from util import util
from models import user_model, profile_model
import os

images_dir = os.path.join(os.getcwd(), 'static/avatar')

class Following(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def follow(self, user_id, profile_to_follow):
        is_followed = False
        user_to_follow = user_model.User.get_by_id(profile_to_follow.user_id)
        for follower in user_to_follow.followed_by:
            if user_id == follower.follower.user_id:
                is_followed = True
                break
        if is_followed == False:
            new_following_action = Following(
                user_id=profile_to_follow.user_id, follower_id=user_id)
            db.session.add(new_following_action)
            db.session.commit()
            print(
                f"User {user_to_follow.profile[0].profile_name} followed successfully!")
        else:
            print("You cannot follow same person twice...")

    @classmethod
    def unfollow(cls, user_id, profile_to_unfollow):
        user_to_follow = user_model.User.get_by_id(profile_to_unfollow.user_id)
        for following in user_to_follow.followed_by:
            if user_id == following.follower.user_id:
                print(following)
                db.session.delete(following)
                db.session.commit()
                break

    @classmethod
    def check_if_followed(cls, user_id, profile_to_check):
        user_to_check = user_model.User.get_by_id(profile_to_check.user_id)
        for follower in user_to_check.followed_by:
            if user_id == follower.follower.user_id:
                return True
        return False

    @classmethod
    def get_followers(cls, profile):
        user_to_check = user_model.User.get_by_id(profile.user_id)
        return len(user_to_check.followed_by)


