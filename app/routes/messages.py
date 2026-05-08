from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Message, Match

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/api/messages', methods=['POST'])
def send_message():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    match_id  = data.get('match_id')
    content   = data.get('content')

    if not match_id or not content:
        return jsonify({"error": "match_id and content are required"}), 400

    match = Match.query.get(match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404

    sender_id = session["user_id"]

    # Derive receiver from the match
    if match.user1_id == sender_id:
        receiver_id = match.user2_id
    else:
        receiver_id = match.user1_id

    message = Message(
        match_id=match_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent", "id": message.id})


@messages_bp.route('/api/messages/<int:match_id>')
def get_messages(match_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    messages = Message.query.filter_by(match_id=match_id).order_by(Message.timestamp).all()

    return jsonify([
        {
            "id":          m.id,
            "sender_id":   m.sender_id,
            "receiver_id": m.receiver_id,
            "content":     m.content,
            "timestamp":   m.timestamp.isoformat(),
            "is_read":     m.is_read
        }
        for m in messages
    ])
