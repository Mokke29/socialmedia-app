from database import db
from datetime import datetime
from util import util
import os

images_dir = os.path.join(os.getcwd(), 'static/avatar')

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    avatar_path = db.Column(db.String(100))
    profile_name = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def edit_profile(self, data, image=False ):
        try:
            if image != False:
                new_image = util.id_generator()
                image.filename = new_image + "." + image.filename.split('.')[1]
                if util.file_exists(os.path.join(images_dir, image.filename)):
                    new_image = util.id_generator()
                    image.filename = new_image + "." + image.filename.split('.')[1]
                else: 
                    pass
                image.save(os.path.join(images_dir, image.filename))

            if data['profile_name'] != '':
                self.profile_name = data['profile_name'] 
            if data['description'] != '': 
                self.description = data['description']
            if image != False:
                self.avatar_path = image.filename
            
            db.session.commit()
            return {"err": False}
        except Exception as e:
            print(f"Profile model exception $$ {e}")
            return {"err": True}