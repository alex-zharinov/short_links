import re
from datetime import datetime

from sqlalchemy.orm import validates
from validators import url

from . import db
from .constants import LEN_ID
from .utils import get_random_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @validates('original')
    def validate_original(self, key, value):
        if not url(value):
            raise ValueError('Неверная ссылка!')
        return value

    @validates('short')
    def validate_original(self, key, value):
        print('value =', type(value))
        if value == '':
            value = self.get_unique_short_id()
        elif not (re.fullmatch(r'^[a-zA-Z0-9]*$', value)) or len(value) > 16:
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        elif URLMap.query.filter_by(short=value).first() is not None:
            raise ValueError(f'Имя "{value}" уже занято.')
        return value

    def to_dict(self):
        return dict(
            url=self.original,
        )

    @classmethod
    def create_link_map(cls, url, custom_id):
        obj = URLMap(original=url, short=custom_id)
        db.session.add(obj)
        db.session.commit()
        return obj

    def get_unique_short_id(self=None):
        short = get_random_id(LEN_ID)
        while URLMap.query.filter_by(short=short).first() is not None:
            short = get_random_id(LEN_ID)
        return short
