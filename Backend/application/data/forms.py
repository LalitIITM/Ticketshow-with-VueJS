from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, SubmitField, FloatField, FileField
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.validators import DataRequired , EqualTo
from werkzeug.utils import secure_filename
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage
from datetime import datetime
from application.data.models import *

images = UploadSet('images', IMAGES)

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class VenueForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50)])
    place = StringField('Place', validators=[InputRequired(), Length(max=50)])
    capacity = IntegerField('Capacity', validators=[InputRequired(), NumberRange(min=1)])

class ShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    ticket_price = IntegerField('Ticket Price', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])

    def __init__(self, *args, **kwargs):
        super(ShowForm, self).__init__(*args, **kwargs)
        self.venue.choices = [(v.id, v.name) for v in Venue.query.all()]

class BookingForm(FlaskForm):
    show_name = SelectField('Show', validators=[DataRequired()])
    venue_name = SelectField('Venue', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')