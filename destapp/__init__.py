from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
db = SQLAlchemy()
DB_NAME = 'database.db'
UPLOAD_FOLDER = 'saved_files/'

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'fgfgfgd sdaasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from destapp.views import views
    from destapp.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from destapp.models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


