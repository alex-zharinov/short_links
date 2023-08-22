from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        return jsonify({'message':
                        'Указанный id не найден'}), HTTPStatus.NOT_FOUND
    return jsonify(link.to_dict()), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), HTTPStatus.BAD_REQUEST
    if 'url' not in data:
        return jsonify({'message':
                        '"url" является обязательным полем!'}), HTTPStatus.BAD_REQUEST
    original = data.get('url')
    link_map = URLMap(original=original)
    try:
        link_map.get_short_id(data.get('custom_id'))
    except Exception as err:
        return jsonify({'message': f'{err}'}), HTTPStatus.BAD_REQUEST
    db.session.add(link_map)
    db.session.commit()
    return jsonify(
        {
            'url': link_map.original,
            'short_link': request.host_url + link_map.short
        }
    ), HTTPStatus.CREATED
