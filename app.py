from flask import (Flask, g, render_template, flash,
                   redirect, url_for, abort)
import datetime
from slugify import slugify

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'da;lfkjadlfjfdaopsifdsaifdoisafakldf=jdaff'


@app.before_request
def before_request():
    """Connect to the database before each request"""
    # g is used globally so we attach thing to access them everywhere
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the db after each request"""
    g.db.close()
    return response


# INDEX
@app.route('/')
def index():
    return render_template("index.html")


# LIST JOURNALS
@app.route('/entries')
def entries():
    journals_list = models.Entry.select()
    return render_template("journal_list.html", entries=journals_list)


@app.route('/details/<slug>')
def entry_detail(slug):
    entry = models.Entry.get(models.Entry.slug == slug)
    return render_template('detail.html', entry=entry)


# ADD JOURNAL
@app.route('/entry/add', methods=['GET', 'POST'])
def add_journals():
    """Add a new entry"""
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Entry.create(title=form.title.data.strip(),
                            slug=slugify(form.title.data),
                            date=form.date.data,
                            time_spent=form.time_spent.data,
                            content_learned=form.content_learned.data,
                            resources=form.resources.data)
        flash("An entry was saved", "success")
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


# EDIT JOURNAL
@app.route('/entry/<slug>/edit', methods=['GET', 'POST'])
def edit_entry(slug):
    """Edit an entry"""
    entry = models.Entry.get(models.Entry.slug == slug)
    form = forms.UpdateEntryForm(title=entry.title,
                                 date=entry.date,
                                 time_spent=entry.time_spent,
                                 content_learned=entry.content_learned,
                                 resources=entry.resources
                                 )
    if form.validate_on_submit():
        models.Entry.update(
            {models.Entry.title: form.title.data.strip(),
             models.Entry.slug: slugify(form.title.data),
             models.Entry.date: form.date.data,
             models.Entry.time_spent: form.time_spent.data,
             models.Entry.content_learned: form.content_learned.data,
             models.Entry.resources: form.resources.data
             }).where(models.Entry.slug == entry.slug).execute()
        flash("Entry was updated", "success")
        return redirect(url_for('entries'))

    return render_template('edit.html', form=form)


# DELETE
@app.route('/entry/<slug>/delete')
def delete_entry(slug):
    try:
        entry = models.Entry.get(models.Entry.slug ** slug)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Entry.get(
                slug=slug
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("You have deleted {}!".format(entry.title), "success")
    return redirect(url_for('entries'))


if __name__ == "__main__":
    models.initialize()

    try:
        models.Entry.create_entry(
            title="Initial Journal",
            date=datetime.datetime.now(),
            time_spent=55,
            content_learned="Trying to pass the project",
            resources="Treehouse"
        )
    except ValueError:
        print('value error')
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
