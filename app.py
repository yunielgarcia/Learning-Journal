from flask import (Flask, g, render_template, flash,
                   redirect, url_for, abort)
import datetime

import models


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
    return render_template("journal_list.html")


if __name__ == "__main__":
    models.initialize()

    try:
        models.Journal.create_journal(
            title="Initial Journal",
            time_spent=55,
            content_learned="Trying to pass the project",
            resources="Treehouse"
        )
    except ValueError:
        print('value error')
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)