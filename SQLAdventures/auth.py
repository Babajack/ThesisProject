import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from SQLAdventures.db import get_user_db, get_player_db, init_player_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username_register']
        password = request.form['password_register']
        password2 = request.form['password2_register']
        user_db = get_user_db()

        if not username:
            error = 'Benutzername darf nicht leer sein!'
        elif not password:
            error = 'Passwort darf nicht leer sein!'
        elif password != password2:
            error = 'Passwörter stimmen nicht überein!'
        elif user_db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Spieler {} ist bereits registriert!'.format(username)

        if error is None:
            user_db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            user_db.commit()

            # login the user
            user = user_db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            session.clear()

            session['user_id'] = user['id']

            # create new database file for new player
            init_player_db(user['username'])

            return redirect(url_for('index'))

        #flash(error)

    return render_template('auth/register.html', error=error)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_db = get_user_db()
        user = user_db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Benutzername oder Passwort falsch!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', error=error)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
