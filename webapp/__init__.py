from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dark_ghost"
    app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .view import views
    from .auth import auths

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auths, url_prefix="/auth") #/auth

    from .models import User, Note
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auths.login"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists("webapp/"+DB_NAME):
        with app.app_context():
            db.create_all()
            print("db created")
