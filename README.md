# DriftDater

DriftDater is a dating web application that allows registered users to create detailed profiles, discover compatible matches, and connect with other users through a messaging system.

The system implements a Flask REST API backend that handles authentication, profile management, matching logic, search functionality, and messaging between matched users. The frontend is built with Vue 3, providing a responsive and interactive user interface for browsing profiles, liking users, and managing conversations. Additionally, a relational database, that uses PostgreSQL in production and SQLite for development, is used to store user accounts, profiles, matches, and messages, ensuring structured and scalable data management.



---

## Team Members and their roles

Zoya Hanson: Project Manager & Backend Lead 

Thorn Brooks: QA/Testing Lead & Backend Assistant 

Davi-Ann Mills: Frontend Lead


---

## Tech Stack

- Frontend: Vue 3, Vue Router, Vuex, Vite
- Backend: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-Login
- Database: PostgreSQL, SQLite
- Auth: Session-based authentication with Flask-bcrypt password hashing
- File Uploads: Flask file handling for profile pictures

---

## Setup Instructions

### Prerequisites

Make sure you have the following installed:
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/driftdater.git
cd driftdater
```

---

### 2. Backend Setup (Flask)

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
.\venv\Scripts\activate         # Windows

# Install Python dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/driftdater
DEBUG=True
```

Run database migrations:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Start the Flask server:

```bash
flask --app app --debug run
```

The backend will run at: `http://localhost:5000`

---

### 3. Frontend Setup (Vue 3)

Open a new terminal:

```bash
npm install
npm run dev
```

The frontend will run at: `http://localhost:5173`

### Compile

```sh
npm run build
```

---

## API Documentation

Base URL: `http://localhost:5000`

Protected routes require the user to be logged in via session cookie. Requests that require auth will return `401 Unauthorized` if no valid session exists.

---

### Authentication & Profile

| Method | Endpoint | Description | Auth Required | Content-Type |
|--------|----------|-------------|---------------|--------------|
| POST | `/api/register` | Register a new user | No | `application/json` |
| POST | `/api/login` | Log in a user | No | `application/json` |
| POST | `/api/logout` | Log out the current user | Yes | — |
| POST | `/api/profile` | Create a profile for the logged-in user | Yes | `multipart/form-data` |

---

**POST `/api/register` — Request Body:**
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "securepassword"
}
```

**Success Response `201`:**
```json
{
  "message": "User registered successfully"
}
```

**Error Response `400`:**
```json
{
  "error": "Email already exists"
}
```

---

**POST `/api/login` — Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Success Response `200`:**
```json
{
  "message": "Login successful",
  "user_id": 1
}
```

**Error Response `401`:**
```json
{
  "error": "Invalid credentials"
}
```

---

**POST `/api/logout` — No body required.**

**Success Response `200`:**
```json
{
  "message": "Logged out"
}
```

---

**POST `/api/profile` — Form Data (multipart/form-data):**

| Field | Type | Required |
|-------|------|----------|
| `name` | string | Yes |
| `age` | integer | Yes |
| `bio` | string | No |
| `location` | string | No |
| `photo` | file | No |

**Success Response `201`:**
```json
{
  "message": "Profile created successfully"
}
```

---

### Matching

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/like` | Like another user | No* |
| GET | `/api/matches/<user_id>` | Get all mutual matches for a user | No* |



---

**POST `/api/like` — Request Body:**
```json
{
  "user1_id": 1,
  "user2_id": 3
}
```

**Response — Mutual match detected `200`:**
```json
{
  "message": "It's a match!"
}
```

**Response — One-sided like `200`:**
```json
{
  "message": "User liked"
}
```

---

**GET `/api/matches/<user_id>` — No body required.**

**Success Response `200`:**
```json
[
  {
    "id": 5,
    "user1_id": 1,
    "user2_id": 3
  }
]
```

---

### Messaging

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/messages` | Send a message to a matched user | No* |
| GET | `/api/messages/<match_id>` | Get all messages in a match conversation | No* |

---

**POST `/api/messages` — Request Body:**
```json
{
  "match_id": 5,
  "sender_id": 1,
  "receiver_id": 3,
  "content": "Hey, how are you?"
}
```

**Success Response `200`:**
```json
{
  "message": "Message sent"
}
```

---

**GET `/api/messages/<match_id>` — No body required.**

**Success Response `200`:**
```json
[
  {
    "sender": 1,
    "receiver": 3,
    "content": "Hey, how are you?",
    "timestamp": "2026-05-07T10:30:00"
  }
]
```

---

### Search & Discovery

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/search` | Search profiles by location and age range | No* |

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `location` | string | Filter by exact location string | `Kingston` |
| `min_age` | integer | Minimum age | `20` |
| `max_age` | integer | Maximum age | `30` |

**Example Request:**
```
GET /api/search?location=Kingston&min_age=20&max_age=30
```

**Success Response `200`:**
```json
[
  {
    "id": 2,
    "name": "Alice Wonder",
    "age": 25,
    "location": "Kingston"
  }
]
```

---

## Database Tables

| Table | Description |
|-------|-------------|
| `users` | Stores login credentials and account info |
| `profiles` | Stores detailed profile info linked to a user |
| `interests` | Lookup table of interest tags |
| `profile_interests` | Many-to-many join between profiles and interests |
| `swipes` | Records every like/dislike/pass action |
| `matches` | Confirmed mutual likes between two users |
| `messages` | Messages exchanged between matched users |
| `favorites` | Bookmarked profiles saved by users |
| `blocked_users` | Users blocked by other users |

---


## ER Diagram

<img width="1536" height="1024" alt="DRIFTDATER_ERD (2)" src="https://github.com/user-attachments/assets/f1652f56-13de-4951-b481-8de3889d649b" />



## User Manual

### Getting Started

#### 1. Register an Account
- Visit `http://localhost:5173` and click **Create Account**
- Fill in your email, username, name, date of birth, gender, and who you're looking for
- Your profile is automatically created after registration

#### 2. Complete Your Profile
- After logging in, click **Profile** in the navigation bar
- Add your bio, location, and select at least 3 interests
- Set your profile visibility (Public / Private)
- Click **Save Profile**

#### 3. Browse Potential Matches (Dashboard)
- The Dashboard shows profiles of other users
- Use the filters at the top to narrow by name, age range, or location
- For each profile you can:
  - **Like** — records your interest; if they like you back it's a match!
  - **Dislike** — records a dislike and removes the profile from your view
  - **Pass** — hides the profile without recording anything
  - **★ Save** — adds the profile to your favorites

#### 4. View Your Matches
- Click **Matches** in the nav to see all users who have mutually liked you
- Click **Message** on any match to open the chat

#### 5. Messaging
- Click **Messages** in the nav to see all your active conversations
- Click any conversation to open the chat window
- Type and send messages; the conversation auto-refreshes every 5 seconds
- Timestamps are shown on every message

#### 6. Dark Mode
- Click the **Dark Mode** button in the top-right navbar to toggle dark/light theme

#### 7. Logout
- Click **Logout** in the navbar to securely end your session

---

## Known Issues / Limitations

- Profile photo uploads are stored locally and may not persist on Render's free tier without cloud storage.
- Real-time messaging uses 5-second polling; WebSocket support is not yet integrated.
- Password reset functionality is not yet implemented.
- Search filters on the dashboard are client-side only; the backend search endpoint handles location and age range.

---

## Additional Notes

- Never commit your `.env` file — it is included in `.gitignore`
- Passwords are hashed using werkzeug.security (bcrypt-compatible)
- CORS is enabled for `http://localhost:5173`
- Optional features implemented: Dark Mode, Save Favorites
