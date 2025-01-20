from flask import Flask, request, send_from_directory, render_template, jsonify
from flask import current_app as app
from application.data.models import *
from application.data.forms import *
from application.data import data_access
from flask_security import login_required, roles_accepted, roles_required
from application import tasks
from application.controller.login import *
from flask_sse import sse
from time import perf_counter
from time import perf_counter_ns
from application.utils.cache import cache
from flask_uploads import UploadSet, IMAGES
from functools import wraps
from datetime import timedelta

print("in controller app", app)

images = UploadSet('images', IMAGES)

# Create a blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route("/hello", methods=["GET"])
@cache.cached(timeout=300)
def hello():
    start = perf_counter_ns()
    app.logger.info("I am doing something here")
    stop = perf_counter_ns()
    print("Elapsed time:", stop - start, "Am working")
    return "Welcome to Lalit's App TICKETSHOW"

@routes.route('/')
@cache.cached(timeout=300)
def home():
    return render_template("home.html", now=datetime.now())

# Route for the index page
@routes.route('/index')
@cache.cached(timeout=300)
def index():
    return render_template('index.html',now=datetime.now())

# Route for displaying all venues
@routes.route('/venues')
@cache.cached(timeout=50, key_prefix='venues')
def venues():
    # Check if venues data is in the cache
    cached_venues = cache.get('venues')
    
    if cached_venues is not None:
        return render_template('venue.html', venues=cached_venues, now=datetime.now())
    else:
        # Data is not in the cache, fetch it from the database
        venues = Venue.query.all()
        
        # Store the fetched data in the cache
        cache.set('venues', venues, timeout=50)
        
        return render_template('venue.html', venues=venues, now=datetime.now())

@routes.route('/admin_dashboard', methods = ['GET', 'POST'])
@admin_required
def admin_dashboard():
    venues = Venue.query.all()
    shows = Show.query.all()

    return render_template('admin_dashboard.html', venues=venues, shows=shows, now =datetime.now())

@routes.route('/user_dashboard', methods = ['GET', 'POST'])
@user_required
def user_dashboard():
    venues = Venue.query.all()
    shows = Show.query.all()
    return render_template('user_dashboard.html', venues=venues, shows=shows, now =datetime.now())

# Route for creating a new venue
@routes.route('/create_venue', methods=['GET', 'POST'])
@admin_required
def create_venue():
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, place=form.place.data, capacity=form.capacity.data)
        db.session.add(venue)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Venue created successfully!', 'success')
        return redirect(url_for('routes.admin_dashboard'))
    return render_template('create_venue.html', form=form,now=datetime.now())

# Route for editing a venue
@routes.route('/venue/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_venue(id):
    venue = Venue.query.get(id)
    if request.method == 'POST':
        venue.name = request.form['name']
        venue.place = request.form['place']
        venue.capacity = request.form['capacity']
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Venue updated successfully!')
        return redirect(url_for('routes.venues'))
    return render_template('edit_venue.html', venue=venue,now=datetime.now())

# Route for deleting a venue
@routes.route('/venue/delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def delete_venue(id):
    venue = Venue.query.get(id)
    if request.method == 'POST':
        db.session.delete(venue)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Venue deleted successfully!')
        return redirect(url_for('routes.venues'))
    return render_template('delete_venue.html', venue=venue,now=datetime.now())

# Route for displaying all shows
@routes.route('/shows')
@cache.cached(timeout=300)
def shows():
    shows = Show.query.all()
    # create a list to store show details with venue names and thumbnail images
    show_details = []    
    for show in shows:
        venue = Venue.query.get(show.venue_id)
        show_detail = {
            'id': show.id,
            'Name': show.name,
            'Rating': show.rating,
            'Tag': show.tags,
            'ticket_Price': show.ticket_price,
            'venue_name': venue,
            'thumbnail_image': show.image_path,
        }
        show_details.append(show_detail)        
    return render_template('shows.html', show_details=show_details, now=datetime.now())

# Route for creating a new show
@routes.route('/create_show', methods=['GET', 'POST'])
@admin_required
def create_show():
    form = ShowForm()
    if form.validate_on_submit():
        # create show
        show = Show(name=form.name.data, rating=form.rating.data, tags=form.tags.data, 
                    ticket_price=form.ticket_price.data, venue_id=form.venue.data)
        
        # save image file
        if form.image.data:
            filename = images.save(form.image.data)
            show.image_path = filename
        
        db.session.add(show)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Show created successfully!', 'success')
        return redirect(url_for('routes.shows'))  
        
    return render_template('create_show.html', form=form, show={}, now=datetime.now())

# Route for editing a show
@routes.route('/show/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_show(id):
    show = Show.query.get(id)
    if request.method == 'POST':
        show.name = request.form['name']
        show.rating = request.form['rating']
        show.tags = request.form['tags']
        show.ticket_price = request.form['ticket_price']
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Show updated successfully!')
        return redirect(url_for('routes.shows'))
    return render_template('edit_show.html', show=show,now=datetime.now())

# Route for deleting a show
@routes.route('/show/delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def delete_show(id):
    show = Show.query.get(id)
    if request.method == 'POST':
        db.session.delete(show)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Show deleted successfully!')
        return redirect(url_for('routes.shows'))
    return render_template('delete_show.html', show=show,now=datetime.now())

# Route for creating a booking
@routes.route('/create_booking', methods=['GET', 'POST'])
@user_required
def create_booking():
    form = BookingForm()
    form.show_name.choices = [(s.name, s.name) for s in Show.query.all()]
    form.venue_name.choices = [(v.name, v.name) for v in Venue.query.all()]

    if form.validate_on_submit():
        show_name = form.show_name.data
        venue_name = form.venue_name.data
        quantity = form.quantity.data

        # Get the show object associated with the selected show name
        show = Show.query.filter_by(name=show_name).first()

        # Get the venue object associated with the selected venue name
        venue = Venue.query.filter_by(name=venue_name).first()

        # Check if the selected venue is associated with the selected show
        if venue.id != show.venue_id:
            flash('Please select the correct venue for this show.', 'danger')
            return redirect(url_for('routes.create_booking'))

        # Create a new booking
        booking = Booking(show_id=show.id, venue_id=venue.id, user_id=current_user.id, quantity=quantity)
        db.session.add(booking)
        db.session.commit()
        # Clear the entire cache
        cache.clear()

        flash('Booking created successfully!', 'success')
        return redirect(url_for('routes.my_bookings'))

    return render_template('create_booking.html', form=form, now=datetime.now())

# Route for viewing user's bookings
@routes.route('/my_bookings', methods=['GET'])
@user_required
@cache.cached(timeout=300)
def my_bookings():
    if current_user is None:
        # user is not logged in
        return redirect(url_for('login.login'))
    print(current_user)
    # get user's bookings from database
    bookings = Booking.query.filter_by(user_id=current_user.id).all()    
    # create a list to store booking details along with show and venue names
    booking_details = []
    
    for booking in bookings:
        show = Show.query.get(booking.show_id)
        venue = Venue.query.get(booking.venue_id)
        #show = session.get(Show, booking.show_id)
        #venue = session.get(Venue, booking.venue_id)
        
        booking_detail = {
            'id' : booking.id,
            'show_name': show.name if show else 'N/A',
            'venue_name': venue.name  if venue else 'N/A',
            'quantity': booking.quantity
        }
        booking_details.append(booking_detail)
      
    return render_template('my_bookings.html', booking_details=booking_details, now=datetime.now())

# Route for deleting a booking
@routes.route('/delete_booking/<int:booking_id>', methods=['POST'])
@user_required
def delete_booking(booking_id):
    # get booking from database
    booking = Booking.query.get(booking_id)
    flash('Confirm you want to delete this booking, this cannot be undone later')
    # check if booking exists and belongs to the current user
    if booking and booking.user_id == current_user.id:
        db.session.delete(booking)
        db.session.commit()
        # Clear the entire cache
        cache.clear()
        flash('Booking deleted successfully!', 'success')
    else:
        flash('Booking not found or you are not authorized to delete it!', 'danger')

    return redirect(url_for('routes.my_bookings'))

@routes.route('/admin_bookings', methods=['GET'])
@admin_required
@cache.cached(timeout=300)
def admin_bookings():
    if current_user is None:
        # user is not logged in
        return redirect(url_for('login.login'))
    # Join the Booking table with the User, Venue, and Show tables
    bookings = Booking.query\
        .join(User, User.id == Booking.user_id)\
        .join(Venue, Venue.id == Booking.venue_id)\
        .join(Show, Show.id == Booking.show_id)\
        .all()
    
    # create a list to store booking details along with show and venue names
    booking_details = []
    
    for booking in bookings:
        user =  User.query.get(booking.user_id)
        show = Show.query.get(booking.show_id)
        venue = Venue.query.get(booking.venue_id)
        
        booking_detail = {
            'id': booking.id,
            'user': user.username,
            'show_name': show.name,
            'venue_name': venue.name,
            'quantity': booking.quantity
        }
        booking_details.append(booking_detail)
      
    return render_template('admin_bookings.html', booking_details=booking_details, now=datetime.now())

@routes.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        place = request.form['location']
        rating = request.form.get('rating', None)
        tags = request.form.get('tag', None)

        if search_term and place:
            venues = Venue.query.filter(Venue.place == place).all()

            if rating and tags:
                shows = Show.query.filter(
                    Show.name.ilike('%{}%'.format(search_term)),
                    Show.rating == rating,
                    Show.tags == tags,
                    Show.venue.has(place=place) # filter shows by venue place
                ).all()
            elif rating:
                shows = Show.query.filter(
                    Show.name.ilike('%{}%'.format(search_term)),
                    Show.rating == rating,
                    Show.venue.has(place=place) # filter shows by venue place
                ).all()
            elif tags:
                shows = Show.query.filter(
                    Show.name.ilike('%{}%'.format(search_term)),
                    Show.tags == tags,
                    Show.venue.has(place=place) # filter shows by venue place
                ).all()
            else:
                shows = Show.query.filter(
                    Show.name.ilike('%{}%'.format(search_term)),
                    Show.venue.has(place=place) # filter shows by venue place
                ).all()

            show_venues = {}
            for show in shows:
                venue = Venue.query.filter(Venue.id == show.venue_id).first()
                show_venues[show.id] = venue

            return render_template('search1.html', venues=venues, shows=shows, show_venues=show_venues, now=datetime.now())

        elif search_term:
            shows = Show.query.filter(
                Show.name.ilike('%{}%'.format(search_term))
            ).all()

            show_venues = {}
            for show in shows:
                venue = Venue.query.filter(Venue.id == show.venue_id).first()
                show_venues[show.id] = venue

            return render_template('search1.html', shows=shows, show_venues=show_venues, now=datetime.now())

        elif place:
            venues = Venue.query.filter(Venue.place == place).all()
            shows = []
            show_venues = {}

            for venue in venues:
                for show in venue.shows:
                    if search_term:
                        if search_term in show.name:
                            shows.append(show)
                            show_venues[show.id] = venue
                    else:
                        shows.append(show)
                        show_venues[show.id] = venue

            return render_template('search1.html', venues=venues, shows=shows, show_venues=show_venues, now=datetime.now())

    return render_template('search1.html', now=datetime.now())
  
@routes.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)

### To test db connectivity
from application.data.models import User
@routes.route('/test')
def test_db():
   users = User.query.all()
   for user in users:
       print (user.username)
   return render_template('test.html',users=users, now=datetime.now())

def register_routes(app):
    app.register_blueprint(routes)
    
from application import tasks
#from application.tasks import just_say_hello,your_immediate_task, long_running_job 

## To check celery workers and redis
@routes.route('/enqueue_hello', methods=['GET'])
def some_controller_function():
    # Enqueue the task
    #job = tasks.just_say_hello.apply_async(countdown=10)
    now = datetime.now()
    print("In flask, time is " ,now)
    job = tasks.just_say_hello.apply_async(countdown=10)
    result = job.wait()
    return str(result) , 200
    #return "Task enqueued with ID: {}".format(result.id)

@routes.route('/trigger_task', methods=['GET','POST'])
def trigger_task(): 
    result = tasks.your_immediate_task.delay()
    return "Task triggered TRIGGER successfully :{}".format(result.id)

@routes.route("/start_long_running_job", methods=['GET','POST'])
def start_long_running_task():
    result = tasks.long_running_task.delay()    
    return "STARTED LONG RUNNING TASK!:{}".format(result.id)

@routes.route("/test_send_message", methods=["GET","POST"])
def test_send_message():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"

@routes.route('/cache-demo')
@cache.cached(timeout=300)  # Cache this route 
def cache_demo():
    cached_value = "This value is cached for so many seconds."
    return jsonify({"Cached Value": cached_value})
