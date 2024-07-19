import os
from flask import Flask, render_template, send_file
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig, StageConfig
from application.jobs import workers
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.data.models import *
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_swagger_ui import get_swaggerui_blueprint
from flask_security import utils
from flask_marshmallow import Marshmallow
from flask_sse import sse
from application.utils.cache import cache, init_app
import jwt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS, cross_origin
from application.jobs.workers import celery, ContextTask


# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# create an UploadSet for images
# create an UploadSet for images
images = UploadSet('images', IMAGES)

app = None
api = None
celery = None
cache = cache

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder="templates")
    print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      app.logger.info("Starting stage.")
      print("Starting  stage")
      app.config.from_object(StageConfig)
      print("pushed config")
    else:
      app.logger.info("Starting Local Development.")
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    app.app_context().push()

    # initialize the login manager
    login_manager.init_app(app)
    # Define and register the load_user function
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    print("DB Init")
    db.init_app(app)
    print("DB Init complete")
    app.app_context().push() 
    
    # configure Flask-Uploads
    configure_uploads(app, (images,))
          
    ma = Marshmallow(app)
    app.app_context().push()

    jwt = JWTManager()
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    jwt.init_app(app)
    app.app_context().push()

    app.logger.info("App setup complete")
    
    api = Api(app)
    app.app_context().push()   
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]      
    )   

    celery.Task = workers.ContextTask
    app.app_context().push()
    #cache
    init_app(app)
    app.app_context().push()
    print("Create app complete")
    return app, api, celery, cache

app, api, celery, cache = create_app()

CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": "http://localhost:8081",
        "methods": ["OPTIONS", "GET", "POST", "PUT", "PATCH","DELETE"]
    }
})
app.config['CORS_HEADERS'] = ["Content-Type"]

from application.controller.api import UserAPI,CreateUserAPI,VenueAPI,CreateVenueAPI
from application.controller.api import ShowAPI,CreateShowAPI,AllVenuesAPI,AllShowsAPI
from application.controller.api import CreateBookingAPI, AdminBookingsAPI,UserBookingsAPI
from application.controller.api import SearchAPI,VenuesByShowNameAPI

# Add the UserAPI resource to the API with its corresponding URL endpoint    
api.add_resource(UserAPI, '/api/user', '/api/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])

api.add_resource(CreateUserAPI, '/api/user/', methods=['POST'])    
    # Add the VenueAPI resource to the API with its corresponding URL endpoint   
api.add_resource(VenueAPI,'/api/venue' ,'/api/venue/<int:venue_id>', methods=['GET', 'PUT','PATCH', 'DELETE'])
    # Add the CreateVenueAPI resource to the API with its corresponding URL endpoint for creating a new venue
api.add_resource(CreateVenueAPI, '/api/venue/create')
    # Add the ShowAPI resource to the API with its corresponding URL endpoint    
api.add_resource(ShowAPI, '/api/show', '/api/show/<int:show_id>', methods=['GET', 'PUT','PATCH', 'DELETE'])    
    # Add the CreateShowAPI resource to the API with its corresponding URL endpoint for creating a new venue
api.add_resource(CreateShowAPI, '/api/show/create')
api.add_resource(AllVenuesAPI, '/api/venues')
api.add_resource(AllShowsAPI, '/api/shows')
api.add_resource(CreateBookingAPI, '/api/create_booking')    
api.add_resource(AdminBookingsAPI, '/api/admin_bookings', '/api/admin_bookings/<int:user_id>', methods=['GET', 'DELETE']) 
api.add_resource(UserBookingsAPI, '/api/my_bookings','/api/my_bookings/<int:booking_id>')
api.add_resource(SearchAPI, '/api/search')
api.add_resource(VenuesByShowNameAPI, '/api/venues-by-show-name')

# Serve the OpenAPI specification at /swagger
SWAGGER_URL = '/swagger'
API_URL = '/api/swagger.yaml'  # URL to your OpenAPI specification (YAML file)
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My Flask RESTful API for my app 'TICKETSHOW"
    }
)
    
    # Get the absolute path of the current directory where this Python script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.route('/api/swagger.yaml')
@cross_origin(origin = '*', headers = ['Content-type'])
def serve_swagger_spec():
    yaml_file_path = os.path.join(current_directory, 'api.yaml')
    return send_file(yaml_file_path, mimetype='text/yaml')


from application.controller.controllers import *
from application.controller.api import api_routes,registration_api,login_api,admin_registration_approval_api,bookings_api
    # register the routes with the app
app.register_blueprint(routes)  
app.register_blueprint(login_bp)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(registration_api)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(login_api)
app.register_blueprint(admin_registration_approval_api)
app.register_blueprint(bookings_api,url_prefix='/api')
#app.register_blueprint(sse, url_prefix='/stream')



@app.route("/api/test")
@cross_origin(origin = '*', headers = ['Content-type'])
def test_backend():
    return jsonify({"message": "Connected to the backend!"})

from application.tasks import just_say_hello,your_immediate_task

@app.route('/cache-demo')
def cache_demo():
    # Set a value in the cache with a timeout of 60 seconds
    current_app.cache.set('test_key', 'test_value', timeout=60)

    # Check if the value exists in the cache
    cached_value = current_app.cache.get('test_key')
    print("Cached value:", cached_value)

    # You can also return the cached value as a response
    return f"Cached value: {cached_value}"

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403

# Rehash the passwords before running the Flask app
rehash_passwords()

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
