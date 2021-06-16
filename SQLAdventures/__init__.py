import os
from flask import Flask, render_template, g
import json


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    player_db_path = app.instance_path + "\\players\\"
    app.config.from_mapping(
        SECRET_KEY='dev',
        USER_DATABASE=os.path.join(app.instance_path, 'user_db.sqlite'),
        PLAYER_DATABASE=player_db_path
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

    try:
        os.makedirs(player_db_path)
    except OSError:
        pass

    # init the db
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    @auth.login_required
    def index():
        return render_template('index.html')

    @app.route('/quests')
    @auth.login_required
    def quests():
        quest_file = os.path.join(app.static_folder, 'data', 'quests.json')

        #
        user_db = db.get_user_db()
        user_db.execute('update user set SIMPLE = 5')
        user_db.commit()
        #

        return render_template('quests/quests.html', questfile=json.load(open(quest_file)), user=g.user)

    return app
