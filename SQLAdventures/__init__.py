import os
from flask import Flask, render_template, url_for, redirect


def create_app():
    # create and configure the app
    my_app = Flask(__name__, instance_relative_config=True)
    player_db_path = my_app.instance_path + "\\players\\"
    my_app.config.from_mapping(
        SECRET_KEY='b\x17p\x0f\x9e\xae\xe4\x81n\xc5&\xd9\xbb \xf0\x81b',
        USER_DATABASE=os.path.join(my_app.instance_path, 'user_db.sqlite'),
        PLAYER_DATABASE=player_db_path,
        JSON_SORT_KEYS=False,
        JSON_AS_ASCII=False,
        USER_CATEGORIES=['Selects', 'Sub-Queries',
                         'Joins', 'Komplexe Queries']
    )

    # ensure the instance folder exists
    try:
        os.makedirs(my_app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(player_db_path)
    except OSError:
        pass

    # init the db
    from SQLAdventures import db
    db.init_app(my_app)

    from SQLAdventures import auth
    my_app.register_blueprint(auth.bp)

    @my_app.route('/')
    @auth.login_required
    def index():
        return redirect(url_for('quests.questbook'))

    @my_app.route('/intro')
    @auth.login_required
    def intro():

        # -- set user stats for testing --
        # user_db = db.get_user_db()
        #
        # user_db.execute('update user set Selects = 20 where id = ?', (g.user['id'],))
        # user_db.execute('update user set Joins = 20 where id = ?', (g.user['id'],))
        # user_db.execute('update user set "Sub-Queries" = 20 where id = ?', (g.user['id'],))
        # #user_db.execute('update user set "Komplexe Queries" = 20 where id = ?', (g.user['id'],))
        # user_db.commit()
        # # user_db.commit()
        # db.add_user_keywords(g.user['id'], ['DISTINCT', 'LENGTH', 'DESC', 'ASC', 'LIKE', 'BETWEEN',
        #                                     'AND', 'SUM', 'ASG', 'COUNT', 'GROUP BY', 'ROUND',
        #                                     'HAVING', 'JOIN', 'INNER JOIN', 'RIGHT JOIN', 'LEFT JOIN',
        #                                     'CROSS JOIN', 'SEMI JOIN', 'WEITERE TIPPS'])
        # --------------------------------

        return render_template('intro.html')

    from SQLAdventures import lexicon
    my_app.register_blueprint(lexicon.bp)

    from SQLAdventures import quests
    my_app.register_blueprint(quests.bp)

    return my_app


app = create_app()
