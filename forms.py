from slugify import slugify
from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, ValidationError,
                                Length, Optional)

from models import Journal


def title_exists(form, field):
    if Journal.select().where(Journal.slug == slugify(field.data)).exists():
        raise ValidationError('Journal with that title already exists.')


class JournalForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(min=2), title_exists])
    date = DateField('Date', format='%Y-%m-%d')
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    content_learned = TextAreaField('What You Learned',  validators=[DataRequired()])
    resources = TextAreaField('Resources to Remember', validators=[DataRequired()])


# render_kw={"placeholder": "format: yyyy-mm-dd"}
