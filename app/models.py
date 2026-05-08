from datetime import datetime, date
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# ─────────────────────────────────────────────
#  Junction table — profile interests (many-to-many)
# ─────────────────────────────────────────────

profile_interests = db.Table(
    "profile_interests",
    db.Column(
        "profile_id",
        db.Integer,
        db.ForeignKey("profiles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "interest_id",
        db.Integer,
        db.ForeignKey("interests.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# ─────────────────────────────────────────────
#  User
# ─────────────────────────────────────────────

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    profile       = db.relationship("Profile",  back_populates="user", uselist=False, cascade="all, delete-orphan")
    swipes        = db.relationship("Swipe",    foreign_keys="Swipe.swiper_id",   back_populates="swiper", cascade="all, delete-orphan")
    favorites     = db.relationship("Favorite", foreign_keys="Favorite.user_id",  back_populates="user",   cascade="all, delete-orphan")
    sent_messages = db.relationship("Message",  foreign_keys="Message.sender_id", back_populates="sender")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id":         self.id,
            "email":      self.email,
            "username":   self.username,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.username}>"


# ─────────────────────────────────────────────
#  Profile
# ─────────────────────────────────────────────

class Profile(db.Model):
    __tablename__ = "profiles"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Basic info
    name              = db.Column(db.String(100), nullable=False)
    age               = db.Column(db.Integer)
    bio               = db.Column(db.Text)
    profile_picture   = db.Column(db.String(500))

    # Location
    location          = db.Column(db.String(200), index=True)
    latitude          = db.Column(db.Float)
    longitude         = db.Column(db.Float)

    # Additional fields
    occupation        = db.Column(db.String(100))
    education         = db.Column(db.String(200))
    gender            = db.Column(db.String(20))
    looking_for       = db.Column(db.String(20),  default="any")
    relationship_type = db.Column(db.String(30),  default="any")

    # Matching preferences
    min_age_pref      = db.Column(db.Integer, default=18)
    max_age_pref      = db.Column(db.Integer, default=99)
    max_distance_km   = db.Column(db.Integer, default=50)

    # Visibility
    visibility        = db.Column(db.String(20), default="public")

    updated_at        = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user      = db.relationship("User",     back_populates="profile")
    interests = db.relationship("Interest", secondary=profile_interests, back_populates="profiles", lazy="select")

    def to_dict(self):
        return {
            "id":                self.id,
            "user_id":           self.user_id,
            "name":              self.name,
            "age":               self.age,
            "bio":               self.bio,
            "profile_picture":   self.profile_picture,
            "location":          self.location,
            "latitude":          self.latitude,
            "longitude":         self.longitude,
            "occupation":        self.occupation,
            "education":         self.education,
            "gender":            self.gender,
            "looking_for":       self.looking_for,
            "relationship_type": self.relationship_type,
            "min_age_pref":      self.min_age_pref,
            "max_age_pref":      self.max_age_pref,
            "max_distance_km":   self.max_distance_km,
            "visibility":        self.visibility,
            "interests":         [i.name for i in self.interests],
        }

    def __repr__(self):
        return f"<Profile {self.name}>"


# ─────────────────────────────────────────────
#  Interest  (normalised lookup table)
# ─────────────────────────────────────────────

class Interest(db.Model):
    __tablename__ = "interests"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

    profiles = db.relationship("Profile", secondary=profile_interests, back_populates="interests")

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f"<Interest {self.name}>"


# ─────────────────────────────────────────────
#  Swipe  (like | dislike | pass)
# ─────────────────────────────────────────────

class Swipe(db.Model):
    __tablename__ = "swipes"
    __table_args__ = (
        db.UniqueConstraint("swiper_id", "swiped_id", name="uq_swipe_pair"),
        db.Index("ix_swipes_pair", "swiper_id", "swiped_id"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    swiper_id  = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    swiped_id  = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action     = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False, index=True)

    swiper = db.relationship("User", foreign_keys=[swiper_id], back_populates="swipes")
    swiped = db.relationship("User", foreign_keys=[swiped_id])

    def to_dict(self):
        return {
            "id":         self.id,
            "swiper_id":  self.swiper_id,
            "swiped_id":  self.swiped_id,
            "action":     self.action,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Swipe {self.swiper_id} -> {self.swiped_id} ({self.action})>"


# ─────────────────────────────────────────────
#  Match  (confirmed mutual likes)
# ─────────────────────────────────────────────

class Match(db.Model):
    __tablename__ = "matches"
    __table_args__ = (
        db.UniqueConstraint("user1_id", "user2_id", name="uq_match_pair"),
        db.Index("ix_matches_user1", "user1_id"),
        db.Index("ix_matches_user2", "user2_id"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    user1_id   = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id   = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status     = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user1    = db.relationship("User", foreign_keys=[user1_id])
    user2    = db.relationship("User", foreign_keys=[user2_id])
    messages = db.relationship("Message", back_populates="match", cascade="all, delete-orphan", order_by="Message.timestamp")

    def other_user(self, current_user_id):
        return self.user2 if self.user1_id == current_user_id else self.user1

    def to_dict(self, current_user_id=None):
        data = {
            "id":         self.id,
            "user1_id":   self.user1_id,
            "user2_id":   self.user2_id,
            "status":     self.status,
            "created_at": self.created_at.isoformat(),
        }
        if current_user_id:
            other = self.other_user(current_user_id)
            data["other_user"] = other.profile.to_dict() if other.profile else None
        return data

    def __repr__(self):
        return f"<Match {self.user1_id} <-> {self.user2_id}>"


# ─────────────────────────────────────────────
#  Message
# ─────────────────────────────────────────────

class Message(db.Model):
    __tablename__ = "messages"
    __table_args__ = (
        db.Index("ix_messages_match_timestamp", "match_id", "timestamp"),
    )

    id          = db.Column(db.Integer, primary_key=True)
    match_id    = db.Column(db.Integer, db.ForeignKey("matches.id", ondelete="CASCADE"), nullable=False)
    sender_id   = db.Column(db.Integer, db.ForeignKey("users.id",   ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id",   ondelete="CASCADE"), nullable=False)
    content     = db.Column(db.Text,    nullable=False)
    is_read     = db.Column(db.Boolean, default=False, nullable=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    match    = db.relationship("Match", back_populates="messages")
    sender   = db.relationship("User",  foreign_keys=[sender_id],   back_populates="sent_messages")
    receiver = db.relationship("User",  foreign_keys=[receiver_id])

    def to_dict(self):
        return {
            "id":          self.id,
            "match_id":    self.match_id,
            "sender_id":   self.sender_id,
            "receiver_id": self.receiver_id,
            "content":     self.content,
            "is_read":     self.is_read,
            "timestamp":   self.timestamp.isoformat(),
        }

    def __repr__(self):
        return f"<Message match={self.match_id} from={self.sender_id}>"


# ─────────────────────────────────────────────
#  Favorite  (bookmarked profiles)
# ─────────────────────────────────────────────

class Favorite(db.Model):
    __tablename__ = "favorites"
    __table_args__ = (
        db.UniqueConstraint("user_id", "favorited_user_id", name="uq_favorite_pair"),
        db.Index("ix_favorites_user", "user_id"),
    )

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    favorited_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user           = db.relationship("User", foreign_keys=[user_id],           back_populates="favorites")
    favorited_user = db.relationship("User", foreign_keys=[favorited_user_id])

    def to_dict(self):
        return {
            "id":                self.id,
            "user_id":           self.user_id,
            "favorited_user_id": self.favorited_user_id,
            "created_at":        self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Favorite {self.user_id} -> {self.favorited_user_id}>"


# ─────────────────────────────────────────────
#  Additional Feature - Block Users
# ─────────────────────────────────────────────

class BlockedUser(db.Model):
    __tablename__ = "blocked_users"

    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    blocked_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    