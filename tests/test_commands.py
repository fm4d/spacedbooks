import pytest
import datetime

from db_models import Book, Review
from peewee import SqliteDatabase
from commands import add_book, get_book, list_books, remove_book, add_review, remove_review



test_db = SqliteDatabase(':memory:')


def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    test_db.bind([Book, Review], bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables([Book, Review])


def teardown_function(function):
    """ teardown any state that was previously setup with a setup_function
    call.
    """
    test_db.drop_tables([Book, Review])
    test_db.close()


def test_add_book():
    add_book("Test Book", '+0')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today()


def test_add_book_shifted_plus():
    add_book("Test Book", '+5')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today() + datetime.timedelta(5)


def test_add_book_shifted_minus():
    add_book("Test Book", '-5')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today() - datetime.timedelta(5)


def test_get_book():
    add_book("Test Book 1", '+0')
    add_book("Test Book 2", '+0')
    add_book("Test Book 3", '+0')

    book1 = get_book("Test Book 1")
    book2 = get_book('2')

    assert (book1.id == 1 and book1.name == "Test Book 1")
    assert (book2.id == 2 and book2.name == "Test Book 2")


def test_remove_book():
    add_book("Test Book 1", '+0')
    add_book("Test Book 2", '+0')
    add_book("Test Book 3", '+0')

    remove_book("Test Book 1")
    remove_book("Test Book 3")

    books = list(Book.select())

    assert len(books) == 1
    assert books[0].name == "Test Book 2"