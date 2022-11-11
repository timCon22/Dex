"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import *
from models import User
with app.app_context():

    db.drop_all()
    db.create_all()
    db.session.commit()