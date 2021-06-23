import json
import os

from flask import Blueprint, render_template, request, session, url_for, current_app, redirect, g

from SQLAdventures import auth, db
from SQLAdventures.db import get_user_db, get_player_db, init_player_db

bp = Blueprint('quests', __name__, url_prefix='/quests')


@bp.route('/questbook', methods=('GET', 'POST'))
@auth.login_required
def questbook():
    if request.method == 'POST':
        # user wants to start a quest
        # store the selected quest nr
        session['current_quest'] = request.form['QuestSubmitButton']
        return redirect(url_for('quests.quest'))

    quest_file = os.path.join(current_app.static_folder, 'data', 'quests.json')

    # -- set user stats for testing --
    # user_db = db.get_user_db()
    #
    # user_db.execute('update user set Simple = 5 where id = ?', (g.user['id'],))
    # user_db.commit()
    #

    return render_template('quests/quests.html', questfile=json.load(open(quest_file)))


@bp.route('/quest')
@auth.login_required
def quest():
    if session['current_quest'] is None:
        # show error or smth
        pass

    quest_data = os.path.join(current_app.static_folder, 'data', 'quests.json')
    quest_data = json.load(open(quest_data))

    # current_quest = [ quest_category, quest_number ]
    data = str(session['current_quest'])
    quest_name = data.rstrip('0123456789')
    quest_number = int(data[len(quest_name):])

    # find the relevant quest
    quest_data = quest_data[quest_name][quest_number]

    # get the expected result
    result = db.get_player_db().execute(quest_data['Query']).fetchall()

    return render_template('quests/active_quest.html', quest_data=quest_data)
