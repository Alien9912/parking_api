from flask import Flask
from .config import Config
from .extensions import db
from .routes import bp
import requests
import random
from .models import Coffee, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        if Coffee.query.count() == 0 and User.query.count() == 0:
            seed_database()

    return app

def seed_database():
    coffee_url = "https://dummyjson.com/products/search?q=coffee&limit=10"
    coffee_data = requests.get(coffee_url).json()
    coffees = []
    for item in coffee_data['products'][:10]:
        reviews = [rev['comment'] for rev in item.get('reviews', [])[:3]]
        coffee = Coffee(
            title=item['title'],
            category=item['category'],
            description=item['description'],
            reviews=reviews
        )
        coffees.append(coffee)
    db.session.add_all(coffees)
    db.session.commit()

    users_url = "https://dummyjson.com/users?limit=10"
    users_data = requests.get(users_url).json()
    users = []
    for item in users_data['users']:
        user = User(
            name=item['firstName'] + " " + item['lastName'],
            has_sale=random.choice([True, False]),
            address=item['address'],
            coffee_id=random.choice(coffees).id
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
