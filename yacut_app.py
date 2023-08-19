import random
import string

from datetime import datetime

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

LEN_ID = 6

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 128), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if URLMap.query.filter_by(short=field.data).first() is not None:
            raise ValidationError('Предложенная ссылка уже существует!')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data == '':
            unique_short_id = get_unique_short_id(LEN_ID)
            while URLMap.query.filter_by(short=unique_short_id).first() is not None:
                unique_short_id = get_unique_short_id(LEN_ID)
            form.custom_id.data = unique_short_id
        link = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(link)
        db.session.commit()
        form = URLMapForm(obj=link)
        link = request.base_url + link.short
        return render_template('yacut.html', form=form, link=link)
    return render_template('yacut.html', form=form)


@app.route('/<short_link>')
def redirect_view(short_link):
    link = URLMap.query.filter_by(short=short_link).first()
    return redirect(link.original)


def get_unique_short_id(LEN):
    keylist = [random.choice(string.ascii_letters + string.digits) for i in range(LEN)]
    return ("".join(keylist))


if __name__ == '__main__':
    app.run()
