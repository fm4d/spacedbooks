import datetime

from peewee import *


db = SqliteDatabase('books.db')


class Book(Model):
    name = CharField()
    date_created = DateField(default=datetime.date.today)
    date_of_origin = DateField(default=datetime.date.today)

    class Meta:
        database = db


class Review(Model):
    book = ForeignKeyField(Book)
    date_created = DateField(default=datetime.date.today)
    date_of_review = DateField(default=datetime.date.today)

    class Meta:
        database = db