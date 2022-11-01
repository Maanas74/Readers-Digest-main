from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
GOOGLE_API_KEY = "AIzaSyBfn7rxebKpLn0Az2W60KX4kMBZ0hpB5z0"
INIT_RENT = 15
DAILY_RENT = 5

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)

def start_app():
    app = Flask(__name__)
    app.secret_key = 'This is a Secret Key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes.view import view
    from .routes.books import books
    from .routes.users import users
    from .auth.auth import auth
    from .api.books import books_api
    # from . members import member

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    create_database(app)
    db.create_all(app=app)

    # app.register_error_handler(404, page_not_found)
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(books, url_prefix='/books')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(books_api, url_prefix='/api/books')

    return app