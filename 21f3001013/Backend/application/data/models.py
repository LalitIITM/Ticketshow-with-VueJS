from .database import db
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage
from sqlalchemy import CheckConstraint
import bcrypt
#from flask_security import UserMixin, RoleMixin

images = UploadSet('images', IMAGES)

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128),nullable=False)
    #email = db.Column(db.String, nullable = False)
    role = db.Column(db.String(10),default='user')
    is_admin = db.Column(db.Integer, default=0)
    approved = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    #fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 

    def set_password(self, password):
        # Hash the password and decode the bytes to a UTF-8 string
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Encode the password to bytes and compare as bytes
        encoded_password = password.encode('utf-8')
        return bcrypt.checkpw(encoded_password, self.password.encode('utf-8'))
    
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    place = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, 
                          info={'check_constraint': 'capacity >= 0 and capacity <= 100000'})


    shows = db.relationship('Show', backref='venue', lazy='dynamic')

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, info={'check_constraint':'rating >= 0 and rating <= 10'})
    tags = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255))
    ticket_price = db.Column(db.Integer, nullable=False, info={'check_constraint':'ticket_price >= 0 and ticket_price <= 100000'})
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)

    bookings = db.relationship('Booking', backref='show', lazy='dynamic')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    
def create_models(db):
    db.create_all()
    return User, Venue, Show, Booking

def rehash_passwords():
    users = User.query.all()
    for user in users:
        if isinstance(user.password, bytes):
            # Convert the bytes password to string and hash it
            user.set_password(user.password.decode('utf-8'))
            db.session.add(user)
        elif not user.password.startswith("$2b$"):
            # Hash the password and save as string (in case it was previously stored as plain text)
            user.set_password(user.password)
            db.session.add(user)
    db.session.commit()
