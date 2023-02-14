from flask import Flask

from .extensions import db

def create_app(database_uri="mysql://root@localhost/escala_rosenberg"):
    app= Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    
    db.init_app(app)
    
    return app