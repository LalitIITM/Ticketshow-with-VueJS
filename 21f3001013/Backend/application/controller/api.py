from flask import Blueprint, request, jsonify, session, make_response
from flask_restful import Api, Resource, fields, abort, marshal_with, reqparse, marshal
from application.data.models import User, Venue, Show, Booking
from application.data.database import db
from flask import current_app as app
import werkzeug
from flask import abort
from application.utils.validation import BusinessValidationError, NotFoundError
from datetime import datetime, timedelta
from application.config import Config
from flask_login import current_user, logout_user
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from application.data.schemas import *
from application.utils.cache import cache
import sqlite3
import jwt
from sqlalchemy.orm import Session
from functools import wraps
#from main import cache

# Create a blueprint for the API routes
api_routes = Blueprint('api_routes', __name__)

# Request parsers for checking a user
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('password')

# Request parser for creating a new venue
create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name', required=True, help='Venue name is required')
create_venue_parser.add_argument('place', required=True, help='Venue place is required')
create_venue_parser.add_argument('capacity', type=int, required=True, help='Venue capacity is required')

# Request parser for editing a venue
edit_venue_parser = reqparse.RequestParser()
edit_venue_parser.add_argument('id')
edit_venue_parser.add_argument('name')
edit_venue_parser.add_argument('place')
edit_venue_parser.add_argument('capacity', type=int)

# Request parser for creating a new show
create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('name', required=True, help='Show name is required')
create_show_parser.add_argument('rating', type=float, required=True, help='Show rating is required')
create_show_parser.add_argument('tags', required=True, help='Show tags are required')
create_show_parser.add_argument('ticket_price', type=float, required=True, help='Ticket price is required')
create_show_parser.add_argument('venue_id', type=int, required=True, help='Venue ID is required')
create_show_parser.add_argument('thumbnail_image', type=int, required=False, help='Image Optional')

# Request parser for editing a show
edit_show_parser = reqparse.RequestParser()
edit_show_parser.add_argument('name')
edit_show_parser.add_argument('rating', type=float)
edit_show_parser.add_argument('tags')
edit_show_parser.add_argument('ticket_price', type=float)
edit_show_parser.add_argument('venue_id', type=int)

# Request parser for deleting a venue
delete_venue_parser = reqparse.RequestParser()
# Request parser for deleting a show
delete_show_parser = reqparse.RequestParser()
# Request parser for deleting a user
delete_user_parser = reqparse.RequestParser()

# Request parser for booking creation
create_booking_parser = reqparse.RequestParser()
create_booking_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
create_booking_parser.add_argument('show_name', required=True, help='Show name is required')
create_booking_parser.add_argument('venue_name', required=True, help='Venue name is required')
create_booking_parser.add_argument('quantity', type=int, required=True, help='Quantity is required')

# Define the Resource fields here
user_resource_fields = {

    'username': fields.String,
    'password': fields.String
}

venue_resource_fields = {
    'venue_id': fields.Integer,
    'name': fields.String,
    'place': fields.String,
    'capacity': fields.Integer
}

# Create a new dictionary with only the required fields from venue_resource_fields
venue_create_fields = {
    'name': venue_resource_fields['name'],
    'place': venue_resource_fields['place'],
    'capacity': venue_resource_fields['capacity'],
}

show_resource_fields = {
    'name': fields.String,
    'rating': fields.Float,
    'tags': fields.String,
    'ticket_price': fields.Float,
    'venue_id': fields.Integer
    
}

show_create_fields = {
    'name': fields.String,
    'rating': fields.Float,
    'tags': fields.String,
    'ticket_price': fields.Float,
    'venue_id': fields.Integer,
    'thumbnail_image': fields.String(attribute=lambda x: x.image_path)
}
# API Resource for Booking Creation

booking_resource_fields = {
    'user_id': fields.Integer,
    'show_name': fields.String,
    'venue_name': fields.String,
    'quantity': fields.Integer
}

def connect_db():
    try:
        conn = sqlite3.connect('db_directory/testdb.sqlite3', timeout=1000)
        print("Database connected successfully")
        # Get a list of all tables in the database
        
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None
    
registration_api = Blueprint('registration_api', __name__)

@registration_api.route('/api/user/register', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def register():
    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)
    
    if not username or not password:
        return jsonify({'message': 'Invalid username or password'})

    try:
    # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            print("Username already exists")
            return jsonify({'message':"Username already exists"})
            #return jsonify({"message": "Username already exists"}), 409

    # Insert the new user into the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()  # Make sure to commit the changes
        return jsonify({"message": "success"})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "An error occurred"})
   
### Login and Logout routes & APIs
login_api = Blueprint('login_api', __name__)

@login_api.route('/api/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-type'])
def user_login():
    data = request.get_json()
    try:
        username = data.get('username', None)
        password = data.get('password', None)

        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({'message': 'Invalid username or password'})

        if not user.check_password(password):
            print("Incorrect Password")
            return jsonify({'message': 'Invalid username or password'})

        if user.approved == 0:
            print("Unapproved User")
            return jsonify({'message': 'Your registration is not approved, please wait'})
        
        access_token = jwt.encode(
            {
                "username": username,
                "user_id": user.id,
                "user_role": user.role,
                "exp": datetime.utcnow() + timedelta(hours=24),
            },
            key=app.config['SECRET_KEY']
        )

        return jsonify({
            'message': 'User login successful',
            'user_name': user.username,
            'user_id': user.id,
            'user_role': user.role,
            'access_token': access_token
        })
    
    except KeyError:
        return jsonify({'message': 'Invalid input data'})
    
    except Exception as e:
        return jsonify({'message': 'An error occurred' + str(e)})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split('Bearer ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
            user_role = data.get('user_role')  # Get the user's role from token payload
            if user_role not in ['user', 'admin']:
                return jsonify({'message': 'Unauthorized'}), 403  # Return 403 Forbidden
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split('Bearer ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
            user_role = data.get('user_role')  # Get the user's role from token payload
            if user_role != 'admin':
                return jsonify({'message': 'Unauthorized'}), 403  # Return 403 Forbidden
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split('Bearer ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
            user_role = data.get('user_role')  # Get the user's role from token payload
            if user_role != 'user':
                return jsonify({'message': 'Unauthorized'}), 403  # Return 403 Forbidden
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@login_api.route('/api/logout', methods=['GET'])
@cross_origin(origin = '*', headers = ['Content-type'])
@token_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Create a blueprint for approval of a  user registration
admin_registration_approval_api = Blueprint('admin_registration_approval_api', __name__)
@admin_registration_approval_api.route('/api/approve_user/<int:user_id>', methods=['PUT'])
@cross_origin(origin = '*', headers = ['Content-type'])
@token_required
@admin_required  
def approve_user_registration(user_id):
    # Get the user from the database based on the provided user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.approved == 1:
        return jsonify({'message': 'User is already approved'}), 400

    # Set the 'approved' field of the user to 1 for approval
    user.approved = 1

    try:
        db.session.commit()
        cache.clear()
        return jsonify({'message': 'User registration approved successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to approve user registration'}), 500

#UserAPI
class UserAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @cache.cached(timeout=50)    
    def get(self, username=None):
        if username:
            user = User.query.filter_by(username=username).first()
            if user is None:
                return {"Message": "User Not Found"}, 404
            
            user_schema = UserSchema()  # Instantiate the UserSchema
            serialized_user = user_schema.dump(user)  # Serialize the user data
            
            return serialized_user, 200
        else:
            users = User.query.all()
            
            user_schema = UserSchema(many=True)  # Instantiate the UserSchema with many=True
            serialized_users = user_schema.dump(users)  # Serialize the list of users
            
            return serialized_users, 200            
        
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required    
    def put(self, username):
        args = request.get_json()
        password = args.get("password", None)
        if password:
            user = db.session.query(User).filter(User.username == username).first()
            if user:
                user.set_password(password)
                db.session.commit()
                
                # Clear the cache for the 'get' method of UserAPI
                cache.delete(UserAPI.get.make_cache_key(username=username))

                return {"Message": "Password updated successfully"}, 200  # Return the user object with a 200 status code
            else:
                return{"Message": "User not found"}, 404
        else:
            return {"Message": "Password is required for update"}, 400
        
    @cross_origin(origin = '*', headers = ['Content-type'])
    @token_required       
    def delete(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            # Clear the cache for the 'get' method of UserAPI
            cache.delete(UserAPI.get.make_cache_key(username=username))
            return {"Message": "User deleted successfully"}
        else:
            return {"Message": "User not found"}, 404

class CreateUserAPI(Resource):
    
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required    
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        password = args.get("password", None)

        if not username:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="username is required")
        if not password:
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="password is required")

        try:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            # Create a response dictionary with the appropriate message and username
            response_data = {"Message": "User added successfully", "username": username}

            return response_data, 200
        except IntegrityError:
            # Handle the case where the username already exists
            raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate user")

# VenueAPI 
class VenueAPI(Resource):
    
    @cross_origin(origin='*', headers=['Content-type'])
    @cache.cached(timeout=50, query_string=True)
    def get(self, venue_id=None):
        if venue_id:
            venue = Venue.query.filter_by(id=venue_id).first()
            if venue is None:
                return {"Message": "Venue Not Found"}, 404
            
            venue_schema = VenueSchema()  # Instantiate the UserSchema
            serialized_venue = venue_schema.dump(venue)  # Serialize the user data
            
            return serialized_venue, 200
        else:
            venues = Venue.query.all()            
            venue_schema = VenueSchema(many=True)  # Instantiate the UserSchema with many=True
            serialized_venues = venue_schema.dump(venues)  # Serialize the list of users
            
            return serialized_venues, 200
            
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required    
    def patch(self, venue_id):
        args = request.get_json()
        print (args['name'])
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        if venue is None:
            raise NotFoundError(status_code=404)

        if args['name']:
            venue.name = args['name']
        if args['place']:
            venue.place = args['place']
        if args['capacity']:
            venue.capacity = args['capacity']
        if args['id']:
            venue.id = args['id']
        
        db.session.commit()
        
        # Clear the cache associated with VenueAPI.get        
        # Clear the entire cache
        cache.clear()

        return {"Message": "Venue Updated successfully"} ,200    
    
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required  
    def delete(self, venue_id):
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        if venue is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(venue)
            db.session.commit()
            # Clear the entire cache
            cache.clear()
            # Instead of marshaling the response, return a simple dictionary response
            return {"message": "Venue deleted successfully"}, 200
  
class CreateVenueAPI(Resource):   
    #@marshal_with(venue_create_fields)
    @cross_origin(origin = '*', headers = ['Content-type'])
    @token_required
    @admin_required  
    def post(self):
        data = request.get_json()

        name = data.get('name', None)
        place = data.get('place', None)
        capacity = data.get('capacity', None)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code="BE2001", error_message="Venue name is required")
        if place is None:
            raise BusinessValidationError(status_code=400, error_code="BE2002", error_message="Venue place is required")
        if capacity is None:
            raise BusinessValidationError(status_code=400, error_code="BE2003", error_message="Venue capacity is required")

        new_venue = Venue(name=name, place=place, capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        print("Successfully new Venue created")
        return {"message": "Venue created successfully"}, 200

# ShowAPI 
class ShowAPI(Resource):
        
    @cross_origin(origin = '*', headers = ['Content-type'])
    @cache.cached(timeout=50, query_string=True)
    def get(self, show_id=None):
        if show_id:
            show = Show.query.filter_by(id=show_id).first()
            if show is None:
                return {"Message": "Show Not Found"}, 404
            
            show_schema = ShowSchema()  
            serialized_show = show_schema.dump(show)  
            
            return serialized_show, 200
        else:
            shows = Show.query.all()            
            show_schema = ShowSchema(many=True) 
            serialized_shows = show_schema.dump(shows)              
            return serialized_shows, 200 

    #@marshal_with(show_resource_fields)
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required
    def patch(self, show_id):
        args = request.get_json()
        show = db.session.query(Show).filter(Show.id == show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)

        show.name = args.get('name', show.name)
        show.rating = args.get('rating', show.rating)
        show.tags = args.get('tags', show.tags)
        show.ticket_price = args.get('ticket_price', show.ticket_price)
        if 'venue_name' in args:
            venue = Venue.query.filter_by(name=args['venue_name']).first()
            if venue:
                show.venue_id = venue.id
        show.image_path = args.get('image_path', show.image_path)

        db.session.commit()
        # Clear the entire cache
        cache.clear()
        return {"Message": "Show updated successfully"}, 200

    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required
    def delete(self, show_id):
        show = db.session.query(Show).filter(Show.id == show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)

        db.session.delete(show)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        return {"message": "Show deleted successfully"}, 200
    
    @cross_origin(origin = '*', headers = ['Content-type'])
    @token_required
    @admin_required  
    def delete(self, show_id):
        show = db.session.query(Show).filter(Show.id == show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)

        db.session.delete(show)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        return {"message": "Show deleted successfully"}, 200

class CreateShowAPI(Resource):
    #@marshal_with(show_create_fields)
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required
    def post(self):
        data = request.get_json()

        name = data.get('name')
        rating = data.get('rating')
        tags = data.get('tags')
        ticket_price = data.get('ticket_price')
        venue_name = data.get('venue_name')
        venue = Venue.query.filter_by(name=venue_name).first()
        if venue:
            venue_id = venue.id
        else:
            raise NotFoundError(status_code=404)
        image_path = data.get('image_path')

        if name is None:
            raise BusinessValidationError(status_code=400)
        # Add validation checks for other required fields

        new_show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, image_path=image_path,venue_id=venue_id)
        db.session.add(new_show)
        db.session.commit()
        # Clear the entire cache
        cache.clear()

        return {"message": "Show created successfully"}, 200
    
#Bookings APIs
bookings_api = Blueprint('bookings_api', __name__)

# API resource for fetching all bookings by admin
class AdminBookingsAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    @admin_required
    @cache.cached(timeout=50)
    def get(self, user_id=None):
        if user_id is None:
            bookings = Booking.query.all()  # Retrieve all bookings
        else:
            bookings = Booking.query.filter_by(user_id=user_id).all()  # Retrieve bookings for a specific user
        
        serialized_bookings = []

        for booking in bookings:
            user = User.query.get(booking.user_id)
            show = Show.query.get(booking.show_id)
            venue = Venue.query.get(booking.venue_id)
            
            booking_dict = {
                'id': booking.id,
                'user_name': user.username if user else None,
                'show_name': show.name if show else None,
                'venue_name': venue.name if venue else None,
                'quantity': booking.quantity,
                'place' : venue.place if venue else None
                }
            serialized_bookings.append(booking_dict)
        
        return serialized_bookings, 200


class CreateBookingAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    def post(self):
        try:
            token = None
            if 'Authorization' in request.headers:
                token = request.headers.get('Authorization')
                if token and token.startswith('Bearer '):
                    token = token.split('Bearer ')[1]

            if not token:
                return jsonify({'message': 'Authorization token is missing'})

            try:
                data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
                user_id = data.get('user_id')
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'})
            except jwt.DecodeError:
                return jsonify({'message': 'Invalid token'})

            data = request.get_json()
            show_name = data.get('show_name')
            venue_name = data.get('venue_name')
            quantity = data.get('quantity')

            if not (show_name and venue_name and quantity):
                return jsonify({'message': 'Invalid booking data'})

            show = db.session.query(Show).filter_by(name=show_name).first()
            if not show:
                return jsonify({'message': 'Invalid show name'})

            # Check if the selected venue hosts the specified show
            venue = db.session.query(Venue).filter_by(name=venue_name).first()
            if not venue:
                return jsonify({'message': 'Invalid venue name'})

            if venue.id != show.venue_id:
                return jsonify({'message': 'Selected venue does not host the specified show'}), 400

            new_booking = Booking(user_id=user_id, show_id=show.id, venue_id=venue.id, quantity=quantity)
            with db.session.begin_nested():
                db.session.add(new_booking)
            
            db.session.commit()
            # Clear the entire cache
            cache.clear()
            response = jsonify({'message': 'Booking created successfully!'})
            response.headers['Content-Type'] = 'application/json'  
            return response
            #return jsonify({'message': 'Booking created successfully!'})

        except Exception as e:
            response = jsonify({'message': 'An error occurred!'})
            response.headers['Content-Type'] = 'application/json'  
            return response
            #return jsonify({'message': 'An error occurred: ' + str(e)})
        
@cache.cached(timeout=50)
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    booking_details = []

    for booking in bookings:
        show = Show.query.get(booking.show_id)
        venue = Venue.query.get(booking.venue_id)
        user = User.query.get(booking.user_id)

        booking_detail = {
            'id': booking.id,
            'user_name': user.username,
            'show_name': show.name,
            'venue_name': venue.name,
            'quantity': booking.quantity,
            'place' : venue.place
        }
        booking_details.append(booking_detail)
        
    return booking_details

class UserBookingsAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    @token_required 
    @cache.cached(timeout=50)
    def get(self):
        token = request.headers.get('Authorization', '').split('Bearer ')[1]
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data.get('user_id')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return jsonify({'message': 'Invalid token'})

        if not user_id:
            return jsonify({'message': 'User ID is missing'})

        booking_details = get_user_bookings(user_id)
        if booking_details is None:
            return jsonify({'message': 'An error occurred'})

        return jsonify(booking_details)

    @cross_origin(origin='*', headers=['Content-type'])
    @token_required
    def delete(self,booking_id):

        booking = db.session.query(Booking).filter(Booking.id == booking_id).first()
        if booking is None:
            raise NotFoundError(status_code=404)

        db.session.delete(booking)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        return {"message": "Booking deleted successfully"}, 200
        
#All Venues       
class AllVenuesAPI(Resource):
    
    @cross_origin(origin='*', headers=['Content-type'])
    @cache.cached(timeout=300)
    def get(self):
        venues = db.session.query(Venue).all()
        venue_data =[]
        for venue in venues:
    
            venue_dict = {
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'capacity': venue.capacity
            }
            venue_data.append(venue_dict)

        return jsonify(venue_data)
        
#  All Shows
class AllShowsAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    @cache.cached(timeout=300)
    def get(self):
        shows = db.session.query(Show).all()
        show_data = []

        for show in shows:
            show_dict = {
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
                'ticket_price': show.ticket_price,
                'id': show.id,
                'venue_name': show.venue.name if show.venue else None,
               
            }
            show_data.append(show_dict)

        return jsonify(show_data)

class SearchAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    
    def post(self):
        data = request.json
        show = data.get('show')
        place = data.get('location')
        
        shows = Show.query

        if show:
            shows = shows.filter(Show.name.ilike('%{}%'.format(show)))

        if place:
            shows = shows.join(Venue).filter(Venue.place == place)

        response_data = []
        for show in shows:
            venue = Venue.query.get(show.venue_id)
            response_data.append({
                "id": show.id,
                "name": show.name,
                "rating": show.rating,
                "tags": show.tags,
                "venue": venue.name if venue else "",
                "place": venue.place if venue else ""
            })

        return jsonify(response_data)

class VenuesByShowNameAPI(Resource):
    @cross_origin(origin='*', headers=['Content-type'])
    def get(self):
        show_name = request.args.get('show_name')
        if not show_name:
            return {"message": "Show name is required"}, 400

        show = Show.query.filter_by(name=show_name).first()
        if not show:
            return {"message": "Show not found"}, 404

        venues = Venue.query.filter_by(id=show.venue_id).all()
        venue_data = []

        for venue in venues:
            venue_dict = {
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'capacity': venue.capacity
            }
            venue_data.append(venue_dict)

        return jsonify(venue_data)
    
import csv, io

@cross_origin(origin='*', headers=['Content-type'])
def generate_booking_report(user_id):
    bookings = get_user_bookings(user_id)
    for booking in bookings:
        print(booking['user_name'], booking['id'], booking['show_name'])
        
    # Create a CSV formatted string
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Booking ID','User Name','Show Name',
                          'Venue Name', 'Quantity', 'Place'])
    for booking in bookings:
        print(booking)
        csv_writer.writerow([booking['id'], booking['user_name'], booking['show_name'],
                             booking['venue_name'], booking['quantity'], booking['place']])
    
    
    return output.getvalue()

@app.route('/api/export_bookings/<int:user_id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-type'])
@token_required
def export_bookings(user_id):
    # Call the report generation function and generate the report
    report_data = generate_booking_report(user_id)
    
    # Return the report as a downloadable file (e.g., CSV)
    response = make_response(report_data)
    response.headers['Content-Disposition'] = 'attachment; filename=bookings_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/api/export_all_bookings', methods=['GET'])
@cross_origin(origin='*', headers=['Content-type'])
@admin_required
def export_all_bookings():
    # Fetch all bookings from the database
    bookings = Booking.query.all()

    # Create a CSV formatted string
    report_data = []
    for booking in bookings:
        user = User.query.get(booking.user_id)
        show = Show.query.get(booking.show_id)
        venue = Venue.query.get(booking.venue_id)

        report_data.append([booking.id, user.username if user else None,
                            show.name if show else None, venue.name if venue else None,
                            booking.quantity, venue.place if venue else None])

    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Booking ID', 'User Name', 'Show Name', 'Venue Name', 'Quantity', 'Place'])
    csv_writer.writerows(report_data)

    # Return the report as a downloadable file (e.g., CSV)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=all_bookings_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response