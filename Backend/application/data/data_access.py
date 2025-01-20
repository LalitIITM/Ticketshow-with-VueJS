from application.data.models import *
from application.utils.cache import cache

@cache.cached(timeout=50, key_prefix='get_all_venues')
def get_all_venues():
    print("inside Venue")
    venues = Venue.query.all()   
    print("--------------------------") 
    print(str(Venue.query))
    print("--------------------------")
    return venues

@cache.cached(timeout=50, key_prefix='get_all_shows')
def get_all_shows():
    print("inside Show")
    shows = Show.query.all()   
    print("--------------------------") 
    print(str(Show.query))
    print("--------------------------")
    return shows

    return new_like
