import os
from flask import Flask, render_template, g, url_for, request


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    player_db_path = app.instance_path + "\\players\\"
    app.config.from_mapping(
        SECRET_KEY='dev',
        USER_DATABASE=os.path.join(app.instance_path, 'user_db.sqlite'),
        PLAYER_DATABASE=player_db_path,
        JSON_SORT_KEYS=False,
        JSON_AS_ASCII=False,
        USER_CATEGORIES=['Tutorial', 'Selects', 'Joins',
                         'Sub-Queries', 'Mengen-Operationen', 'Komplexe Queries']
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
    from SQLAdventures import db
    db.init_app(app)

    from SQLAdventures import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    @auth.login_required
    def index():

        # -- set user stats for testing --
        user_db = db.get_user_db()
        #
        user_db.execute('update user set Selects = 20 where id = ?', (g.user['id'],))
        user_db.execute('update user set Joins = 20 where id = ?', (g.user['id'],))
        user_db.execute('update user set "Sub-Queries" = 20 where id = ?', (g.user['id'],))
        user_db.execute('update user set "Komplexe Queries" = 20 where id = ?', (g.user['id'],))
        user_db.commit()
        # user_db.commit()
        db.add_user_keywords(g.user['id'], ['DISTINCT', 'LENGTH', 'DESC', 'ASC', 'LIKE', 'BETWEEN',
                                            'AND', 'SUM', 'ASG', 'COUNT', 'GROUP BY', 'ROUND',
                                            'HAVING', 'JOIN', 'INNER JOIN', 'RIGHT JOIN', 'LEFT JOIN',
                                            'CROSS JOIN', 'SEMI JOIN', 'WEITERE TIPPS'])
        # --------------------------------

        return render_template('index.html')

    from SQLAdventures import lexicon
    app.register_blueprint(lexicon.bp)

    from SQLAdventures import quests
    app.register_blueprint(quests.bp)

    return app
