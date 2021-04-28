from flask_login import LoginManager
from flask import current_app
import sqlite3


def init_auth(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return

