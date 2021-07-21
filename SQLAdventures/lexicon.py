import json
import os

from flask import Blueprint, render_template, request, g, current_app

from SQLAdventures import auth, db

bp = Blueprint('lexicon', __name__)


@bp.route('/lexicon')
@auth.login_required
def lexicon():
    keywords = db.get_user_keywords(g.user['id'])
    lexicon_data = os.path.join(current_app.static_folder, 'data', 'lexicon.json')
    with open(lexicon_data, encoding='utf-8') as lexicon_data:
        lexicon_data = json.load(lexicon_data)
    return render_template('lexicon.html', menu=request.args.get('menu'), keywords=keywords, lexicon=lexicon_data)
