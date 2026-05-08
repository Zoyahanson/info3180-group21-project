from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
import os



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        os.makedirs(upload_folder, exist_ok=True)

    with app.app_context():
        db.create_all()

    from app.views import views
    from app.auth import auth_bp
    from app.routes.matches import matches_bp
    from app.routes.messages import messages_bp
    from app.routes.search import search_bp
    from app.routes.favorites import favorites_bp

    app.register_blueprint(views)
    app.register_blueprint(auth_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(favorites_bp)

    return app
