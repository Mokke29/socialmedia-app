from database import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    comment= db.relationship("Comment", backref='comment', foreign_keys='Comment.post_id')

