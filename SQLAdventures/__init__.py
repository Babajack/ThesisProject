import os
from flask import Flask, render_template
from flask_login import login_required


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        USER_DATABASE=os.path.join(app.instance_path, 'user_db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init the db
    from . import user_db
    user_db.init_app(app)

    # init the login manager
    from . import auth
    auth.init_auth()

    @login_required
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
