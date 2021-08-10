import json
import os
import sqlite3
from typing import Union

import click
from flask import current_app, g, session, Flask
from flask.cli import with_appcontext


# open a connection to the user db
def get_user_db() -> sqlite3.Connection:
    if not os.path.exists(os.path.join(current_app.instance_path, 'user_db.sqlite')):
        init_user_db()
    if 'user_db' not in g:
        g.user_db = sqlite3.connect(
            current_app.config['USER_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.user_db.row_factory = sqlite3.Row
    return g.user_db


# open a connection to the db of the current player
def get_player_db(username: str) -> sqlite3.Connection:
    if 'player_db' not in g:
        g.player_db = sqlite3.connect(
            current_app.config['PLAYER_DATABASE'] + username + '.sqlite',
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
    db = sqlite3.connect(
            current_app.config['USER_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    db.row_factory = sqlite3.Row

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# init the db of the current player
def init_player_db(username: str):
    db = get_player_db(username)

    with current_app.open_resource('player_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# init the db of the current player
def update_player_db_1(username: str):
    db = get_player_db(username)

    with current_app.open_resource('player_schema_update_1.sql') as f:
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


# return a list of the users unlocked keywords
def get_user_keywords(user_id: int) -> list[str]:
    return json.loads(get_user(user_id)['Keywords'])


# add unlocked keywords to the users keyword-list
# return true if the new keyword was now unlocked, false if the keyword was unlocked already
def add_user_keywords(user_id: int, unlocked_keywords_list: list[str]) -> list[str]:
    current = get_user_keywords(user_id)
    new_keywords = []
    # example: unlocked_keywords_list = ["INNER JOIN", "LEFT OUTER JOIN"]
    for keywords_elem in unlocked_keywords_list:
        if keywords_elem not in current:
            current.append(keywords_elem.upper())
            new_keywords.append(keywords_elem.upper())
    if new_keywords:
        #current.sort()
        get_user_db().execute('UPDATE user SET Keywords = ? WHERE id = ?', (json.dumps(current), user_id))
        get_user_db().commit()

    return new_keywords


# return a list of the users completed quests
def get_completed_quests(user_id: int) -> list[str]:
    return json.loads(get_user(user_id)['CompletedQuests'])


# add a completed quest to the users completed quest list
# return true if a new quest was completed, false if the quest was completed already
def add_completed_quest(user_id: int, completed_quest_id: str) -> bool:
    current = get_completed_quests(user_id)
    if completed_quest_id not in current:
        current.append(completed_quest_id)
        get_user_db().execute('UPDATE user SET CompletedQuests = ? WHERE id = ?', (json.dumps(current), user_id))
        get_user_db().commit()
        return True
    return False


# return user with id = user_id
def get_user(user_id: int) -> sqlite3.Row:
    return get_user_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def increase_category_level(user_id: int, category: str):
    query = 'UPDATE user SET ' + '\"' + category + '\" = ' + '\"' + category + '\" + 1 WHERE id = ' + str(user_id)
    # query = "UPDATE user SET %s = %s + 1 WHERE id = %d" % (category, category, user_id)
    get_user_db().execute(query)
    get_user_db().commit()
