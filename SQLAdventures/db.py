import json
import sqlite3
from typing import Union

import click
from flask import current_app, g, session, Flask
from flask.cli import with_appcontext


# open a connection to the user db
def get_user_db() -> sqlite3.Connection:
    if 'user_db' not in g:
        g.user_db = sqlite3.connect(
            current_app.config['USER_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.user_db.row_factory = sqlite3.Row
    return g.user_db


# open a connection to the db of the current player
def get_player_db(user_id: int) -> sqlite3.Connection:
    if 'player_db' not in g:
        g.player_db = sqlite3.connect(
            current_app.config['PLAYER_DATABASE'] + str(user_id) + '.sqlite',
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

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# init the db of the current player
def init_player_db(user_id: int):
    db = get_player_db(user_id)

    with current_app.open_resource('player_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# register the command to init the db from command line
@click.command('init-user-db')
@with_appcontext
def init_db_command():
    init_user_db()
    click.echo('Initialized the user database.')


# used in init file to register some functionality
def init_app(app: Flask):
    # close connection to db after application context is popped
    app.teardown_appcontext(close_user_db)
    app.teardown_appcontext(close_player_db)
    # register the command to init the user db
    app.cli.add_command(init_db_command)


# validates the user-specific query
# checks for sql-errors, empty tables and unlocked-keywords
# return a fitting error message or result table
def validate_user_query(user_id: int, query: str, keywords: list[str]) -> Union[dict, list[dict]]:
    # TODO check

    # validate keywords
    for keyword in keywords:
        if keyword.upper() not in get_user_keywords(user_id):
            return {'Error': '<b style="color:#708">' + keyword + '</b>' + ' ist noch nicht freigeschaltet!'}

    # validate sql
    try:
        result = [dict(row) for row in get_player_db(g.user['id']).execute(query).fetchall()]
        if not result:
            return {'Error': 'Die Ergebnistabelle ist leer!'}

        # TODO validate result
        return result
    except sqlite3.Error as err:
        # TODO wrap error
        return {'Error': str(err.args)}


# return a list of unlocked keywords of the user with id = user_id
def get_user_keywords(user_id: int) -> list[str]:
    return json.loads(get_user(user_id)['Keywords'])


# add a unlocked keyword to the users keyword-list
def add_user_keyword(user_id: int, keyword: str):
    current = get_user_keywords(user_id)
    current.append(keyword)
    get_user_db().execute('UPDATE user SET Keywords = ? WHERE id = ?', (current, user_id))
    get_user_db().commit()


# return user with id = user_id
def get_user(user_id: int) -> sqlite3.Row:
    return get_user_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
