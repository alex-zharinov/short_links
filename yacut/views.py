from flask import abort, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap

LEN_ID = 6


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        link_map = URLMap()
        if form.custom_id.data == '' or form.custom_id.data is None:
            form.custom_id.data = URLMap.get_unique_short_id()
        link_map.get_link_map(
            form.original_link.data,
            form.custom_id.data
        )
        db.session.add(link_map)
        db.session.commit()
        form = URLMapForm(obj=link_map)
        link = request.host_url + link_map.short
        return render_template('yacut.html', form=form, link=link)
    return render_template('yacut.html', form=form)


@app.route('/<short_link>')
def redirect_view(short_link):
    link = URLMap.query.filter_by(short=short_link).first()
    if URLMap.query.filter_by(short=short_link).first():
        return redirect(link.original)
    abort(404)
