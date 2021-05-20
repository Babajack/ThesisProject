import sqlite3

import click
from flask import current_app, g, session
from flask.cli import with_appcontext


# open a connection to the user db
def get_user_db():
    if 'user_db' not in g:
        g.user_db = sqlite3.connect(
            current_app.config['USER_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.user_db.row_factory = sqlite3.Row
    return g.user_db


# open a connection to the db of the current player
def get_player_db():
    if 'player_db' not in g:
        test = current_app.config['PLAYER_DATABASE'] + session['username'] + '.sqlite'
        g.player_db = sqlite3.connect(
            current_app.config['PLAYER_DATABASE'] + session['username'] + '.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.player_db.row_factory = sqlite3.Row
    return g.player_db


# close the connection to the db
def close_user_db(e=None):
    db = g.pop('user_db', None)

    if db is not None:
        db.close()


# close the connection to db of the current player
def close_player_db(e=None):
    db = g.pop('player_db', None)

    if db is not None:
        db.close()


# init the user db (only used from command line to create the database)
def init_user_db():
    db = get_user_db()

    with current_app.open_resource('user_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        

# init the db of the current player
def init_player_db():
    db = get_player_db()

    with current_app.open_resource('player_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# register the command to init the db from command line
@click.command('init-user-db')
@with_appcontext
def init_db_command():
    init_user_db()
    click.echo('Initialized the user database.')


# used in init file to register some functionality
def init_app(app):
    # close connection to db after application context is popped
    app.teardown_appcontext(close_user_db)
    app.teardown_appcontext(close_player_db)
    # register the command to init the user db
    app.cli.add_command(init_db_command)
