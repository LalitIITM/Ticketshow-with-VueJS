from flask_caching import Cache

# Create a Cache object
cache = Cache()

# Define cache configurations (you can modify these as needed)
cache_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB" : 9,
    "CACHE_DEFAULT_TIMEOUT" : 30000
}

# Initialize the cache with the app and configurations
def init_app(app):
    # Push the application context before initializing Flask-Caching
    app.app_context().push()
    
    cache.init_app(app, config=cache_config)
