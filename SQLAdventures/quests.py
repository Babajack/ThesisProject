import json
import os

from flask import Blueprint, render_template, request, session, url_for, current_app, redirect, g, jsonify

from SQLAdventures import auth, db

bp = Blueprint('quests', __name__, url_prefix='/quests')


@bp.route('/questbook', methods=['GET', 'POST'])
@auth.login_required
def questbook():
    # find the quest file
    quest_data = os.path.join(current_app.static_folder, 'data', 'quests.json')
    with open(quest_data, encoding='utf-8') as quest_data:
        quest_data = json.load(quest_data)

    if request.method == 'POST':
        # user wants to start a quest

        # preprocess file name
        # example: quest_info = SimpleSelects0
        quest_id = str(request.form['QuestSubmitButton'])
        quest_name = quest_id.rstrip('0123456789')
        quest_nr = int(quest_id[len(quest_name):])

        # find the relevant quest
        selected_quest_line = quest_data[quest_name]
        for i in range(len(selected_quest_line)):
            if i == quest_nr:
                session['quest_data'] = selected_quest_line[i]
                session['quest_id'] = quest_id

        return redirect(url_for('quests.quest'))

    return render_template('quests/quests.html', questfile=quest_data,
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
    quest_data = session.get('quest_data')
    # quest_data = user_input['quest_data']

    # check for valid SQL

    # validate keywords TODO uncomment!!
    # for keyword in keywords:
    #     if keyword.upper() not in db.get_user_keywords(user_id):
    #         return jsonify({'Error': '<b style="color:#708">' + keyword + '</b>' + ' ist noch nicht freigeschaltet!'})

    # check for needed keywords
    if 'NeededKeywords' in quest_data:
        for neededKeyword in quest_data['NeededKeywords']:
            if neededKeyword in keywords:
                keywords.remove(neededKeyword)
            else:
                return jsonify({'Error': 'Für diese Aufgabe musst du ' + ' und '.join(
                    quest_data['NeededKeywords']) + ' verwenden!'})

    # validate sql
    import sqlite3
    try:
        result = [dict(row) for row in db.get_player_db(g.user['username']).execute(query).fetchall()]

        # check for empty result
        if not result:
            return jsonify({'Error': 'Die Ergebnistabelle ist leer!'})

    # check for errors
    except Exception as err:
        # TODO maybe wrap error
        return jsonify({'Error': str(err)})

    # check for correct result
    if quest_data is not None:
        # check for possible result queries if user found an accepted result
        for query in quest_data['ResultQueries']:
            expected_result = [dict(row) for row in
                               db.get_player_db(g.user['username']).execute(query).fetchall()]

            # compare rows based on values
            is_correct = True
            # check for different size of rows
            if len(expected_result) != len(result):
                is_correct = False
            # check if order is important
            elif quest_data['OrderedResult']:
                for i in range(len(expected_result)):
                    for expected_value in expected_result[i].values():
                        if expected_value not in result[i].values():
                            is_correct = False
            else:
                # check if expected rows are somewhere in the result
                for expected_row in expected_result:
                    for row in result:
                        for expected_value in expected_row.values():
                            if expected_value not in row.values():
                                # go to next row
                                break
                        else:
                            # row found -> go to next expected row
                            break
                        # row not found -> go to next row
                        continue
                    # expected row not found
                    else:
                        is_correct = False
                        break

            if is_correct:
                # check if user unlocked a new keyword
                keywords = quest_data['UnlockedKeywords'] if 'UnlockedKeywords' in quest_data else []
                if keywords:
                    new_keywords = db.add_user_keywords(user_id, keywords)
                    if new_keywords:
                        # quest with new unlocked keywords
                        result.append({'result': True, 'unlocked': new_keywords})
                    else:
                        # quest with already unlocked keywords
                        result.append({'result': True})
                else:
                    # quest without unlockable keywords
                    result.append({'result': True})

                # check if user completed a new quest and increased his level
                if db.add_completed_quest(user_id, session.get('quest_id')):
                    db.increase_category_level(user_id, session.get('quest_id').rstrip('0123456789'))
                    if 'UnlockedCategories' in quest_data:
                        for category in quest_data['UnlockedCategories']:
                            db.increase_category_level(user_id, category)
                        if quest_data['UnlockedCategories'] == ["Sub-Queries", "Joins"]:
                            db.update_player_db_1(g.user['username'])

                return jsonify(result)

        result.append({'result': False})

    return jsonify(result)
