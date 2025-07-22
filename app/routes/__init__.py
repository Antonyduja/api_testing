from .home_page import home_page_bp
from .collections import collections_bp
from .environments import environments_bp

def register_routes(app):
    app.register_blueprint(home_page_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(environments_bp)
