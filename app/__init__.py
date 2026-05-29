from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Optional

db = SQLAlchemy()

def create_app(config: Optional[object] = None) -> Flask:
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.api)

    with app.app_context():
        db.create_all()

    return app
