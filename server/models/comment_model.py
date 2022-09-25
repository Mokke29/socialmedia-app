from database import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    reply_to = db.Column(db.Integer)
    reply_profilename = db.Column(db.String(50))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def create_comment(self, content, post_id, user_id):
        try:
            new_comment = Comment(content=content, post_id=post_id, user_id=user_id)
            db.session.add(new_comment)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Comment model exception $$ {e}")
            return False

    def create_reply(self, content, post_id, user_id, comment_id, ):
        try:
            new_reply = Comment(content=content, post_id=post_id, user_id=user_id, reply_to = comment_id)
            db.session.add(new_reply)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Comment model exception $$ {e}")
            return False

    
