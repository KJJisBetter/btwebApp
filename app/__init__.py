from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)

    from app.models import User
    login.login_view = 'main.login'

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)  # Import the routes module
    from app import models

    return app
