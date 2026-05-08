from app import create_app, db
from app.models import User, Profile, Interest

app = create_app()

INTERESTS = [
    "Music", "Gaming", "Hiking", "Cooking", "Travel",
    "Photography", "Fitness", "Movies", "Reading", "Art",
    "Dancing", "Sports", "Yoga", "Coffee", "Anime",
    "Fashion"
]

USERS = [
    {
        "email": "alice@example.com",
        "username": "alice_w",
        "password": "password123",
        "name": "Alice Wonder",
        "age": 24,
        "bio": "Lover of sunsets and good coffee.",
        "location": "Kingston",
        "gender": "Female",
        "looking_for": "male",
        "interests": ["Travel", "Coffee", "Photography"],
    },
    {
        "email": "bob@example.com",
        "username": "bob_m",
        "password": "password123",
        "name": "Bob Martin",
        "age": 27,
        "bio": "Gym rat by day, chef by night.",
        "location": "Portmore",
        "gender": "Male",
        "looking_for": "female",
        "interests": ["Fitness", "Cooking", "Music"],
    },
    {
        "email": "cara@example.com",
        "username": "cara_j",
        "password": "password123",
        "name": "Cara James",
        "age": 22,
        "bio": "Anime and chill? Let's go.",
        "location": "Kingston",
        "gender": "Female",
        "looking_for": "any",
        "interests": ["Anime", "Gaming", "Art"],
    },
    {
        "email": "dave@example.com",
        "username": "dave_k",
        "password": "password123",
        "name": "Dave King",
        "age": 30,
        "bio": "Hiking trails and mountain views.",
        "location": "Mandeville",
        "gender": "Male",
        "looking_for": "female",
        "interests": ["Hiking", "Sports", "Fitness"],
    },
    {
        "email": "emma@example.com",
        "username": "emma_r",
        "password": "password123",
        "name": "Emma Rose",
        "age": 25,
        "bio": "Reading books, writing stories.",
        "location": "Spanish Town",
        "gender": "Female",
        "looking_for": "male",
        "interests": ["Reading", "Art", "Coffee"],
    },
    {
        "email": "frank@example.com",
        "username": "frank_d",
        "password": "password123",
        "name": "Frank Dunn",
        "age": 28,
        "bio": "Movies marathons every weekend.",
        "location": "Kingston",
        "gender": "Male",
        "looking_for": "female",
        "interests": ["Movies", "Gaming", "Music"],
    },
    {
        "email": "grace@example.com",
        "username": "grace_l",
        "password": "password123",
        "name": "Grace Lee",
        "age": 23,
        "bio": "Yoga in the morning, dancing at night.",
        "location": "Portmore",
        "gender": "Female",
        "looking_for": "any",
        "interests": ["Yoga", "Dancing", "Fitness"],
    },
    {
        "email": "henry@example.com",
        "username": "henry_b",
        "password": "password123",
        "name": "Henry Brooks",
        "age": 26,
        "bio": "Fashion is my love language.",
        "location": "Kingston",
        "gender": "Male",
        "looking_for": "female",
        "interests": ["Fashion", "Photography", "Travel"],
    },
]

with app.app_context():
    # Seed interests
    for name in INTERESTS:
        if not Interest.query.filter_by(name=name).first():
            db.session.add(Interest(name=name))
    db.session.commit()

    # Seed users
    added = 0
    for u in USERS:
        if User.query.filter_by(email=u["email"]).first():
            print(f"  skip {u['email']} (already exists)")
            continue

        user = User(email=u["email"], username=u["username"])
        user.set_password(u["password"])
        db.session.add(user)
        db.session.flush()

        interests = Interest.query.filter(Interest.name.in_(u["interests"])).all()

        profile = Profile(
            user_id=user.id,
            name=u["name"],
            age=u["age"],
            bio=u["bio"],
            location=u["location"],
            gender=u["gender"],
            looking_for=u["looking_for"],
            interests=interests,
        )
        db.session.add(profile)
        db.session.commit()
        added += 1
        print(f"  added {u['name']}")

    print(f"\nDone — {added} users added.")
