from flask import Blueprint, request, jsonify
from sqlalchemy import func, distinct
from .extensions import db
from .models import User, Coffee

bp = Blueprint('main', __name__)

@bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    coffee_id = data.get('coffee_id')
    address = data.get('address', {})
    has_sale = data.get('has_sale', False)

    if not name or not coffee_id:
        return jsonify({'error': 'name and coffee_id are required'}), 400

    coffee = Coffee.query.get(coffee_id)
    if not coffee:
        return jsonify({'error': 'Coffee not found'}), 404

    user = User(name=name, coffee_id=coffee_id, address=address, has_sale=has_sale)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'name': user.name,
        'coffee': coffee.title,
        'address': user.address,
        'has_sale': user.has_sale
    }), 201

@bp.route('/coffee/search')
def search_coffee():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Parameter q is required'}), 400

    search_vector = func.to_tsvector('russian', Coffee.title)
    search_query = func.to_tsquery('russian', ' & '.join(query.split()))
    results = Coffee.query.filter(search_vector.op('@@')(search_query)).all()

    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category,
        'description': c.description
    } for c in results])

@bp.route('/coffee/unique_reviews')
def unique_reviews():
    subq = db.session.query(func.unnest(Coffee.reviews).label('review')).subquery()
    unique = db.session.query(distinct(subq.c.review)).all()
    reviews = [row[0] for row in unique if row[0]]
    return jsonify({'unique_reviews': reviews})

@bp.route('/users/by_country')
def users_by_country():
    country = request.args.get('country')
    if not country:
        return jsonify({'error': 'Parameter country is required'}), 400

    users = User.query.filter(User.address['country'].astext == country).all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'address': u.address,
        'coffee_title': u.coffee.title if u.coffee else None
    } for u in users])
