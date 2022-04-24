from flask import Flask
from .leads_routes import bp

def init_app(app:Flask):
    app.register_blueprint(bp)
