import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# open a connection to the db
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['USER_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# close the connection to the db
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# init the db (only used from command line to create the database)
def init_db():
    db = get_db()

    with current_app.open_resource('user_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# register the command to init the db from command line
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


# used in init file
def init_app(app):
    # let the app close the connection after getting a response
    app.teardown_appcontext(close_db)
    # register the command
    app.cli.add_command(init_db_command)