from tkinter import EXCEPTION
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from database import db
from util import util
from models import user_model, profile_model
import os

images_dir = os.path.join(os.getcwd(), 'static/avatar')

def search_profile(profile):
    profiles_found = []
    profiles = profile_model.Profile.query.filter(
        profile_model.Profile.profile_name.startswith(f'{profile}')).all()
    for prof in profiles:
        profiles_found.append(prof.profile_name)
    return profiles_found
