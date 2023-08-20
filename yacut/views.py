from flask import abort, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id

LEN_ID = 6


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data == '' or form.custom_id.data is None:
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
        link = request.host_url + link.short
        return render_template('yacut.html', form=form, link=link)
    return render_template('yacut.html', form=form)


@app.route('/<short_link>')
def redirect_view(short_link):
    link = URLMap.query.filter_by(short=short_link).first()
    if URLMap.query.filter_by(short=short_link).first():
        return redirect(link.original)
    abort(404)
