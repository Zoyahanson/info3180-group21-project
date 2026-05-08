-- DriftDater Database Schema
-- Compatible with PostgreSQL and SQLite

-- ─────────────────────────────────────────────
--  Users
-- ─────────────────────────────────────────────
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_email    ON users (email);
CREATE INDEX ix_users_username ON users (username);


-- ─────────────────────────────────────────────
--  Profiles
-- ─────────────────────────────────────────────
CREATE TABLE profiles (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER      NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    first_name        VARCHAR(80)  NOT NULL,
    last_name         VARCHAR(80)  NOT NULL,
    date_of_birth     DATE         NOT NULL,
    gender            VARCHAR(20)  NOT NULL,
    bio               TEXT,
    profile_photo     VARCHAR(500),
    location          VARCHAR(120),
    latitude          FLOAT,
    longitude         FLOAT,
    looking_for       VARCHAR(20)  NOT NULL DEFAULT 'any',
    min_age_pref      INTEGER      NOT NULL DEFAULT 18,
    max_age_pref      INTEGER      NOT NULL DEFAULT 99,
    max_distance_km   INTEGER      NOT NULL DEFAULT 50,
    relationship_type VARCHAR(30)  NOT NULL DEFAULT 'any',
    height_cm         INTEGER,
    is_visible        BOOLEAN      NOT NULL DEFAULT TRUE,
    updated_at        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_profiles_user_id  ON profiles (user_id);
CREATE INDEX ix_profiles_location ON profiles (location);


-- ─────────────────────────────────────────────
--  Interests
-- ─────────────────────────────────────────────
CREATE TABLE interests (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE INDEX ix_interests_name ON interests (name);


-- ─────────────────────────────────────────────
--  Profile Interests  (many-to-many junction)
-- ─────────────────────────────────────────────
CREATE TABLE profile_interests (
    profile_id  INTEGER NOT NULL REFERENCES profiles(id)  ON DELETE CASCADE,
    interest_id INTEGER NOT NULL REFERENCES interests(id) ON DELETE CASCADE,
    PRIMARY KEY (profile_id, interest_id)
);


-- ─────────────────────────────────────────────
--  Swipes
-- ─────────────────────────────────────────────
CREATE TABLE swipes (
    id         SERIAL PRIMARY KEY,
    swiper_id  INTEGER     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    swiped_id  INTEGER     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action     VARCHAR(10) NOT NULL CHECK (action IN ('like', 'dislike', 'pass')),
    created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_swipe_pair UNIQUE (swiper_id, swiped_id)
);

CREATE INDEX ix_swipes_pair    ON swipes (swiper_id, swiped_id);
CREATE INDEX ix_swipes_created ON swipes (created_at);


-- ─────────────────────────────────────────────
--  Matches
-- ─────────────────────────────────────────────
CREATE TABLE matches (
    id         SERIAL PRIMARY KEY,
    user1_id   INTEGER   NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id   INTEGER   NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_match_pair UNIQUE (user1_id, user2_id),
    CONSTRAINT ck_match_order CHECK (user1_id < user2_id)
);

CREATE INDEX ix_matches_user1 ON matches (user1_id);
CREATE INDEX ix_matches_user2 ON matches (user2_id);


-- ─────────────────────────────────────────────
--  Messages
-- ─────────────────────────────────────────────
CREATE TABLE messages (
    id         SERIAL PRIMARY KEY,
    match_id   INTEGER   NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    sender_id  INTEGER   NOT NULL REFERENCES users(id)   ON DELETE CASCADE,
    content    TEXT      NOT NULL,
    is_read    BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_messages_match_created ON messages (match_id, created_at);


-- ─────────────────────────────────────────────
--  Favorites
-- ─────────────────────────────────────────────
CREATE TABLE favorites (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER   NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    favorited_user_id INTEGER   NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_favorite_pair UNIQUE (user_id, favorited_user_id)
);

CREATE INDEX ix_favorites_user ON favorites (user_id);


-- ─────────────────────────────────────────────
--  Seed: default interests
-- ─────────────────────────────────────────────
INSERT INTO interests (name) VALUES
    ('hiking'), ('gaming'), ('cooking'), ('travel'),
    ('music'), ('fitness'), ('art'), ('movies'),
    ('reading'), ('photography'), ('dancing'), ('sports'),
    ('technology'), ('fashion'), ('food'), ('yoga');
