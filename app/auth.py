from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user
from app import db
from app.models import User, Profile, Interest
from datetime import date

import os

auth_bp = Blueprint('auth', __name__)


# REGISTER

@auth_bp.route('/api/register', methods=['POST'])
def register():

    data = request.get_json()

    email      = data.get('email')
    password   = data.get('password')
    username   = data.get('username')
    first_name = data.get('firstName', '').strip()
    last_name  = data.get('lastName', '').strip()
    gender     = data.get('gender')
    looking_for = (data.get('lookingFor') or 'any').lower()
    dob        = data.get('dob')  # YYYY-MM-DD

    if not email or not password or not username:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Calculate age from date of birth
    age = None
    if dob:
        try:
            birth = date.fromisoformat(dob)
            today = date.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        except ValueError:
            pass

    name = f"{first_name} {last_name}".strip() or username

    profile = Profile(
        user_id=user.id,
        name=name,
        age=age,
        gender=gender,
        looking_for=looking_for,
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# LOGIN

@auth_bp.route('/api/login', methods=['POST'])
def login():

    data = request.get_json()

    email    = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):

        login_user(user)
        session["user_id"] = user.id

        return jsonify({
            "message": "Login successful",
            "user_id": user.id
        })

    return jsonify({"error": "Invalid credentials"}), 401


# LOGOUT

@auth_bp.route('/api/logout', methods=['POST'])
def logout():

    logout_user()
    session.clear()

    return jsonify({"message": "Logged out"})


# GET ALL INTERESTS

@auth_bp.route('/api/interests', methods=['GET'])
def get_interests():
    interests = Interest.query.order_by(Interest.name).all()
    return jsonify([i.to_dict() for i in interests])


# CREATE PROFILE

@auth_bp.route('/api/profile', methods=['POST'])
def create_profile():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    existing_profile = Profile.query.filter_by(user_id=session["user_id"]).first()
    if existing_profile:
        return jsonify({"error": "Profile already exists for this user"}), 400

    data = request.form
    file = request.files.get('photo')
    filename = None

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

    profile = Profile(
        user_id=session["user_id"],
        name=data.get("name"),
        age=int(data.get("age")) if data.get("age") else None,
        bio=data.get("bio"),
        location=data.get("location"),
        gender=data.get("gender"),
        looking_for=data.get("looking_for", "any"),
        profile_picture=filename
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile created successfully"}), 201


# GET PROFILE

@auth_bp.route('/api/profile', methods=['GET'])
def get_profile():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    profile = Profile.query.filter_by(user_id=session["user_id"]).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    data = profile.to_dict()
    data["interest_ids"] = [i.id for i in profile.interests]
    return jsonify(data)


# UPLOAD PROFILE PHOTO

@auth_bp.route('/api/profile/photo', methods=['POST'])
def upload_profile_photo():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    profile = Profile.query.filter_by(user_id=session["user_id"]).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    file = request.files.get('photo')
    if not file:
        return jsonify({"error": "No photo provided"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    profile.profile_picture = filename
    db.session.commit()

    return jsonify({"message": "Photo updated", "profile_picture": filename})


# UPDATE PROFILE

@auth_bp.route('/api/profile', methods=['PUT'])
def update_profile():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    profile = Profile.query.filter_by(user_id=session["user_id"]).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()

    if data.get("name") is not None:
        profile.name = data["name"]
    if data.get("age") is not None:
        profile.age = int(data["age"])
    if data.get("bio") is not None:
        profile.bio = data["bio"]
    if data.get("location") is not None:
        profile.location = data["location"]
    if data.get("gender") is not None:
        profile.gender = data["gender"]
    if data.get("looking_for") is not None:
        profile.looking_for = data["looking_for"]
    if data.get("visibility") is not None:
        profile.visibility = data["visibility"]

    # Update interests
    if "interests" in data:
        interest_ids = data["interests"]  # list of IDs
        interests = Interest.query.filter(Interest.id.in_(interest_ids)).all()
        profile.interests = interests

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})
