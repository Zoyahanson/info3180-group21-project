from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Favorite, User

favorites_bp = Blueprint('favorites', __name__)


@favorites_bp.route('/api/favorites', methods=['GET'])
def get_favorites():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    favorites = Favorite.query.filter_by(user_id=session["user_id"]).all()

    results = []
    for f in favorites:
        other = User.query.get(f.favorited_user_id)
        results.append({
            "id": f.id,
            "favorited_user_id": f.favorited_user_id,
            "profile": other.profile.to_dict() if other and other.profile else None
        })

    return jsonify(results)


@favorites_bp.route('/api/favorites', methods=['POST'])
def add_favorite():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    favorited_id = data.get('favorited_user_id')

    if not favorited_id:
        return jsonify({"error": "Missing favorited_user_id"}), 400

    existing = Favorite.query.filter_by(
        user_id=session["user_id"],
        favorited_user_id=favorited_id
    ).first()

    if existing:
        return jsonify({"message": "Already favorited"}), 200

    fav = Favorite(user_id=session["user_id"], favorited_user_id=favorited_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"message": "Added to favorites"}), 201


@favorites_bp.route('/api/favorites/<int:favorited_user_id>', methods=['DELETE'])
def remove_favorite(favorited_user_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    fav = Favorite.query.filter_by(
        user_id=session["user_id"],
        favorited_user_id=favorited_user_id
    ).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()

    return jsonify({"message": "Removed from favorites"})
