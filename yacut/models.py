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
        assert url(value)
        return value

    def to_dict(self):
        return dict(
            url=self.original,
        )

    def get_link_map(self, original, short):
        setattr(self, 'original', original)
        setattr(self, 'short', short)

    def get_unique_short_id():
        short = get_random_id(LEN_ID)
        while URLMap.query.filter_by(short=short).first() is not None:
            short = get_random_id(LEN_ID)
        return short

    def get_short_id(self, short):
        if short and short != '':
            if not (re.fullmatch(r'^[a-zA-Z0-9]*$', short)) or len(short) > 16:
                raise ValueError('Указано недопустимое имя для короткой ссылки')
            if URLMap.query.filter_by(short=short).first() is not None:
                raise ValueError(f'Имя "{short}" уже занято.')
        else:
            short = URLMap.get_unique_short_id()
        setattr(self, 'short', short)

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
