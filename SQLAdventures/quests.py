import json
import os

from flask import Blueprint, render_template, request, session, url_for, current_app, redirect, g, jsonify

from SQLAdventures import auth, db

bp = Blueprint('quests', __name__, url_prefix='/quests')


@bp.route('/questbook', methods=['GET', 'POST'])
@auth.login_required
def questbook():
    if request.method == 'POST':
        # user wants to start a quest

        # find the quest file
        quest_data = os.path.join(current_app.static_folder, 'data', 'quests.json')
        quest_data = json.load(open(quest_data))

        # preprocess file name
        current_quest = str(request.form['QuestSubmitButton'])
        quest_name = current_quest.rstrip('0123456789')
        quest_number = int(current_quest[len(quest_name):])

        # find the relevant quest
        session['quest_data'] = quest_data[quest_name][quest_number]

        return redirect(url_for('quests.quest'))

    quest_file = os.path.join(current_app.static_folder, 'data', 'quests.json')

    # -- set user stats for testing --
    # user_db = db.get_user_db()
    #
    # user_db.execute('update user set Simple = 5 where id = ?', (g.user['id'],))
    # user_db.commit()
    #

    return render_template('quests/quests.html', questfile=json.load(open(quest_file)),
                           user_categories=current_app.config['USER_CATEGORIES'])


@bp.route('/quest')
@auth.login_required
def quest():
    if session.get('quest_data') is None:
        # TODO show error or smth
        pass

    # get the expected result
    # result = db.get_player_db(g.user['username']).execute(session.get('quest_data')['Query']).fetchall()

    return render_template('quests/active_quest.html', quest_data=session.get('quest_data'))


@bp.route('/query', methods=['POST'])
@auth.login_required
def validate_query():
    # request = query and highlighted-sql-keywords
    user_input = request.get_json()
    keywords = user_input['keywords']
    query = user_input['query']
    user_id = g.user['id']

    result = db.validate_user_query(user_id, query, keywords)

    # check for correct result
    if (session.get('quest_data')) is not None:
        expected_result = [dict(row) for row in
                           db.get_player_db(user_id).execute(session.get('quest_data')['Query']).fetchall()]
        # TODO implement better query comparison
        is_correct = result == expected_result #not any(x != y for x, y in zip(result, expected_result))

    return jsonify(result)
