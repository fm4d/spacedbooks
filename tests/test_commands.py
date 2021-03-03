import pytest
import datetime

from db_models import Book, Review
from peewee import SqliteDatabase
from commands import add_book


test_db = SqliteDatabase(':memory:')
test_db.bind([Book, Review], bind_refs=False, bind_backrefs=False)
test_db.connect()
test_db.create_tables([Book, Review])


def test_add_book():
    name = "Test Book 1"
    date_shift = '+0'
    add_book(name, date_shift)

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book 1"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today()


def test_add_book_shifted():
    name = "Test Book 2"
    date_shift = '+5'
    add_book(name, date_shift)

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book 1"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today()