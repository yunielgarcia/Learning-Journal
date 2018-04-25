from peewee import *
import datetime
from slugify import slugify

DATABASE = SqliteDatabase('journal.db')


class Journal(Model):
    slug = CharField(unique=True)
    title = CharField()
    date = DateField()
    time_spent = IntegerField()
    content_learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        # And since order_by is a tuple (you can use a list if you want),
        # we have to include that trailing comma if there's only one tuple member.
        order_by = ('-date',)

    @classmethod
    def create_journal(cls, title, date, time_spent, content_learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    slug=slugify(title),
                    date=date,
                    title=title,
                    time_spent=time_spent,
                    content_learned=content_learned,
                    resources=resources
                )
        except IntegrityError:  # Meaning a field already exits
            print('error initialation')
            raise ValueError("Journal with that title already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()