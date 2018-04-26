from flask import (Flask, g, render_template, flash,
                   redirect, url_for)
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
def journals():
    journals_list = models.Journal.select()
    return render_template("journal_list.html", journals=journals_list)


@app.route('/details/<slug>')
def journals_detail(slug):
    journal = models.Journal.get(models.Journal.slug == slug)
    return render_template('detail.html', journal=journal)


# ADD JOURNAL
@app.route('/entry/add', methods=['GET', 'POST'])
def add_journals():
    """Add a new album"""
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Journal.create(title=form.title.data.strip(),
                              slug=slugify(form.title.data),
                              date=form.date.data,
                              time_spent=form.time_spent.data,
                              content_learned=form.content_learned.data,
                              resources=form.resources.data)
        flash("Journal was saved", "success")
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


# EDIT JOURNAL
@app.route('/entry/<slug>/edit', methods=['GET', 'POST'])
def edit_journals(slug):
    """Edit an entry"""
    journal = models.Journal.get(models.Journal.slug == slug)
    form = forms.UpdateEntryForm(title=journal.title,
                                 date=journal.date,
                                 time_spent=journal.time_spent,
                                 content_learned=journal.content_learned,
                                 resources=journal.resources
                                 )
    if form.validate_on_submit():
        models.Journal.update(
            {models.Journal.title: form.title.data.strip(),
             models.Journal.slug: slugify(form.title.data),
             models.Journal.date: form.date.data,
             models.Journal.time_spent: form.time_spent.data,
             models.Journal.content_learned: form.content_learned.data,
             models.Journal.resources: form.resources.data
             }).where(models.Journal.slug == journal.slug).execute()
        flash("Journal was updated", "success")
        return redirect(url_for('journals'))

    return render_template('edit.html', form=form)


if __name__ == "__main__":
    models.initialize()

    try:
        models.Journal.create_journal(
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
