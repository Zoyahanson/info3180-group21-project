from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Match, Swipe

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/api/like', methods=['POST'])
def like_user():

    data = request.get_json()
    swiper_id = data.get('user1_id')
    swiped_id = data.get('user2_id')

    if not swiper_id or not swiped_id:
        return jsonify({"error": "Missing user IDs"}), 400

    # Record the swipe if not already done
    existing_swipe = Swipe.query.filter_by(swiper_id=swiper_id, swiped_id=swiped_id).first()
    if not existing_swipe:
        swipe = Swipe(swiper_id=swiper_id, swiped_id=swiped_id, action='like')
        db.session.add(swipe)
        db.session.commit()

    # Check if the other user already liked back
    reverse = Swipe.query.filter_by(swiper_id=swiped_id, swiped_id=swiper_id, action='like').first()

    if reverse:
        # Only create match once (use sorted IDs to avoid duplicate)
        u1, u2 = min(swiper_id, swiped_id), max(swiper_id, swiped_id)
        existing_match = Match.query.filter_by(user1_id=u1, user2_id=u2).first()
        if not existing_match:
            match = Match(user1_id=u1, user2_id=u2)
            db.session.add(match)
            db.session.commit()
        return jsonify({"message": "It's a match!"})

    return jsonify({"message": "User liked"})


@matches_bp.route('/api/matches/<int:user_id>')
def get_matches(user_id):

    matches = Match.query.filter(
        (Match.user1_id == user_id) | (Match.user2_id == user_id)
    ).all()

    results = []

    for m in matches:
        other = m.user2 if m.user1_id == user_id else m.user1
        results.append({
            "id": m.id,
            "user1_id": m.user1_id,
            "user2_id": m.user2_id,
            "other_user": other.profile.to_dict() if other.profile else None
        })

    return jsonify(results)


@matches_bp.route('/api/dislike', methods=['POST'])
def dislike_user():

    data = request.get_json()
    swiper_id = data.get('user1_id')
    swiped_id = data.get('user2_id')

    if not swiper_id or not swiped_id:
        return jsonify({"error": "Missing user IDs"}), 400

    existing = Swipe.query.filter_by(swiper_id=swiper_id, swiped_id=swiped_id).first()
    if not existing:
        swipe = Swipe(swiper_id=swiper_id, swiped_id=swiped_id, action='dislike')
        db.session.add(swipe)
        db.session.commit()

    return jsonify({"message": "User disliked"})