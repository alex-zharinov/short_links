from flask import abort, redirect, render_template, request

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data is None:
            form.custom_id.data = URLMap.get_unique_short_id()
        obj = URLMap.create_link_map(
            url=form.original_link.data,
            custom_id=form.custom_id.data
        )
        form = URLMapForm(obj=obj)
        link = request.host_url + obj.short
        return render_template('yacut.html', form=form, link=link)
    return render_template('yacut.html', form=form)


@app.route('/<short_link>')
def redirect_view(short_link):
    link = URLMap.query.filter_by(short=short_link).first()
    if URLMap.query.filter_by(short=short_link).first():
        return redirect(link.original)
    abort(404)
