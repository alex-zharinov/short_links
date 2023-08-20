import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id

LEN_ID = 6


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        return jsonify({'message':
                        'Указанный id не найден'}), 404
    return jsonify(link.to_dict()), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400
    if 'url' not in data:
        return jsonify({'message':
                        '"url" является обязательным полем!'}), 400
    original = data.get('url')
    short = data.get('custom_id')
    if short and short != '':
        print(len(short))
        if not (re.fullmatch(r'^[a-zA-Z0-9]*$', short)) or len(short) > 16:
            return jsonify({'message': 'Указано недопустимое имя для короткой ссылки'}), 400
        if URLMap.query.filter_by(short=short).first() is not None:
            return jsonify(
                {'message': f'Имя "{short}" уже занято.'}
            ), 400
    else:
        short = get_unique_short_id(LEN_ID)
        while URLMap.query.filter_by(short=short).first() is not None:
            short = get_unique_short_id(LEN_ID)
    link = URLMap(original=original, short=short)
    db.session.add(link)
    db.session.commit()
    return jsonify(
        {
            'url': link.original,
            'short_link': request.host_url + link.short
        }
    ), 201
