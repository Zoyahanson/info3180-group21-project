from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Profile, Interest

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search_users():

    location    = request.args.get('location')
    min_age     = request.args.get('min_age', type=int)
    max_age     = request.args.get('max_age', type=int)
    interest_ids = request.args.getlist('interests', type=int)
    sort_by     = request.args.get('sort', 'newest')

    current_user_id = session.get('user_id')

    query = Profile.query

    if current_user_id:
        query = query.filter(Profile.user_id != current_user_id)

    query = query.filter(Profile.visibility == 'public')

    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))

    if min_age is not None:
        query = query.filter(Profile.age >= min_age)

    if max_age is not None:
        query = query.filter(Profile.age <= max_age)

    if interest_ids:
        query = query.filter(Profile.interests.any(Interest.id.in_(interest_ids)))

    if sort_by == 'newest':
        query = query.order_by(Profile.id.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Profile.id.asc())

    profiles = query.all()

    return jsonify([p.to_dict() for p in profiles])