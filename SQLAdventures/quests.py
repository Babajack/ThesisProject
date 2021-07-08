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

        # preprocess file name
        # example: quest_info = SimpleSelects0
        quest_info = str(request.form['QuestSubmitButton'])
        quest_name = quest_info.rstrip('0123456789')
        quest_nr = int(quest_info[len(quest_name):])

        # find the quest file
        quest_data = os.path.join(current_app.static_folder, 'data', 'quests.json')
        with open(quest_data, encoding='utf-8') as quest_data:
            quest_data = json.load(quest_data)

        # find the relevant quest
        selected_quest_line = quest_data[quest_name]
        for i in range(len(selected_quest_line)):
            if i == quest_nr:
                session['quest_data'] = selected_quest_line[i]

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

    # load current quest
    return render_template('quests/active_quest.html', quest_data=session.get('quest_data'))


@bp.route('/query', methods=['POST'])
@auth.login_required
def validate_query():
    # request = query and highlighted-sql-keywords
    user_input = request.get_json()
    keywords = user_input['keywords']
    query = user_input['query']
    user_id = g.user['id']

    # check for valid SQL

    # validate keywords TODO uncomment!!
    # for keyword in keywords:
    #     if keyword.upper() not in db.get_user_keywords(user_id):
    #         return jsonify({'Error': '<b style="color:#708">' + keyword + '</b>' + ' ist noch nicht freigeschaltet!'})

    # validate sql
    import sqlite3
    try:
        result = [dict(row) for row in db.get_player_db(g.user['id']).execute(query).fetchall()]

        # check for empty result
        if not result:
            return jsonify({'Error': 'Die Ergebnistabelle ist leer!'})

    # check for errors
    except sqlite3.Error as err:
        # TODO wrap error
        return jsonify({'Error': str(err.args)})

    # check for correct result
    if session.get('quest_data') is not None:
        # check for possible result queries if user found an accepted result
        for query in session.get('quest_data')['ResultQueries']:
            expected_result = [dict(row) for row in
                               db.get_player_db(user_id).execute(query).fetchall()]
            # compare results
            is_correct = result == expected_result  # not any(x != y for x, y in zip(result, expected_result))
            if is_correct:
                # check if user unlocked a new keyword
                keywords = session.get('quest_data')['UnlockedKeywords']
                if keywords:
                    if db.add_user_keywords(user_id, keywords):
                        result.append({'result': True, 'unlocked': keywords})
                    else:
                        result.append({'result': True})

                # TODO check if user increased his level

                return jsonify(result)

        result.append({'result': False})

    return jsonify(result)
