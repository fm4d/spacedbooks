import datetime

from src.db_models import Book, Review
from peewee import SqliteDatabase
from src.commands import add_book, _get_book, list_books, remove_book, add_review, remove_review, list_books_to_review
from config import SPACED_REPETITION_INTERVALS


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
    add_book("Test Book", "Test Author", date_shift='+0')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today()


def test_add_book_shifted_plus():
    add_book("Test Book", "Test Author", date_shift='+5')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today() + datetime.timedelta(5)


def test_add_book_shifted_minus():
    add_book("Test Book", "Test Author", date_shift='-5')

    assert len(Book.select()) == 1

    book = Book.select()[0]
    assert book.name == "Test Book"
    assert book.date_created == datetime.date.today()
    assert book.date_of_origin == datetime.date.today() - datetime.timedelta(5)


def test_get_book():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_book("Test Book 2", "Test Author", date_shift='+0')
    add_book("Test Book 3", "Test Autohr", date_shift='+0')

    book1 = _get_book("Test Book 1")
    book2 = _get_book('2')

    assert (book1.id == 1 and book1.name == "Test Book 1")
    assert (book2.id == 2 and book2.name == "Test Book 2")


def test_remove_book():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_book("Test Book 2", "Test Author", date_shift='+0')
    add_book("Test Book 3", "Test Author", date_shift='+0')

    remove_book("Test Book 1")
    remove_book("Test Book 3")

    books = list(Book.select())

    assert len(books) == 1
    assert books[0].name == "Test Book 2"


def test_list_books():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_book("Test Book 2", "Test Author", date_shift='+5')
    add_book("Test Book 3", "Test Author", date_shift='-5')

    books = list_books('name', 'asc')

    assert (books[0].id == 1 and books[0].name == "Test Book 1" and books[0].date_of_origin == datetime.date.today())
    assert (books[1].id == 2 and books[1].name == "Test Book 2"
            and books[1].date_of_origin == datetime.date.today() + datetime.timedelta(5))
    assert (books[2].id == 3 and books[2].name == "Test Book 3"
            and books[2].date_of_origin == datetime.date.today() - datetime.timedelta(5))


def test_add_review_by_name():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_review("Test Book 1", '-3')

    reviews = list(Review.select().join(Book, on=(Review.book == Book.id)))

    assert len(reviews) == 1
    assert reviews[0].date_of_review == datetime.date.today() - datetime.timedelta(3)
    assert reviews[0].book.name == "Test Book 1"


def test_add_review_by_id():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_review('1', '+3')

    reviews = list(Review.select().join(Book, on=(Review.book == Book.id)))

    assert len(reviews) == 1
    assert reviews[0].date_of_review == datetime.date.today() + datetime.timedelta(3)
    assert reviews[0].book.name == "Test Book 1"


def test_remove_review():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_review('1', '+3')

    reviews = list(Review.select().join(Book, on=(Review.book == Book.id)))
    assert len(reviews) == 1

    remove_review(1)
    reviews_after_remove = list(Review.select().join(Book, on=(Review.book == Book.id)))
    assert len(reviews_after_remove) == 0


def test_list_reviews():
    add_book("Test Book 1", "Test Author", date_shift='+0')
    add_book("Test Book 2", "Test Author", date_shift='+0')
    add_review("Test Book 1", '-3')
    add_review("Test Book 1", '-3')
    add_review("Test Book 2", '-3')

    assert len(list(Review.select().
                    join(Book, on=(Review.book == Book.id)).
                    where(Book.name == "Test Book 1"))) == 2
    assert len(list(Review.select().
                    join(Book, on=(Review.book == Book.id)).
                    where(Book.name == "Test Book 2"))) == 1


def test_list_books_to_review_without_reviews():
    add_book("Test Book 1", "Test Author", date_shift='-31')

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 1
    assert books_to_review[0].name == "Test Book 1"


def test_list_books_to_review_short():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0]))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 0


def test_list_books_to_review():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 1))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 1
    assert books_to_review[0].name == "Test Book 1"


def test_list_books_to_review_multiple_books():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 1))
    add_book("Test Book 2", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 3))
    add_book("Test Book 3", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 5))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 3
    assert books_to_review[0].name == "Test Book 3"
    assert books_to_review[1].name == "Test Book 2"
    assert books_to_review[2].name == "Test Book 1"


def test_list_books_to_review_multiple_books_with_shorts():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 1))
    add_book("Test Book 2", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 3))
    add_book("Test Book 3", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] - 3))
    add_book("Test Book 4", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 5))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 3
    assert books_to_review[0].name == "Test Book 4"
    assert books_to_review[1].name == "Test Book 2"
    assert books_to_review[2].name == "Test Book 1"


def test_list_books_to_review_multiple_reviews():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[3] + 5))
    add_review("Test Book 1", '-' + str((SPACED_REPETITION_INTERVALS[3] + 5) - (SPACED_REPETITION_INTERVALS[0] + 1)))
    add_review("Test Book 1", '-' + str((SPACED_REPETITION_INTERVALS[3] + 5) - (SPACED_REPETITION_INTERVALS[1] + 1)))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 1
    assert books_to_review[0].name == "Test Book 1"


def test_list_books_to_review_multiple_reviews_short():
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[3] - 5))
    add_review("Test Book 1", '-' + str((SPACED_REPETITION_INTERVALS[3] - 5) - (SPACED_REPETITION_INTERVALS[0] + 1)))
    add_review("Test Book 1", '-' + str((SPACED_REPETITION_INTERVALS[3] - 5) - (SPACED_REPETITION_INTERVALS[1] + 1)))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 0


def test_list_books_to_review_with_sort_multiple_reviews():
    add_book("Test Book 2", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[2]))
    add_review("Test Book 2", '-' + str(SPACED_REPETITION_INTERVALS[2] - (SPACED_REPETITION_INTERVALS[0] + 2)))
    add_book("Test Book 1", "Test Author", date_shift='-' + str(SPACED_REPETITION_INTERVALS[0] + 5))

    books_to_review = list_books_to_review()

    assert len(books_to_review) == 2
    assert books_to_review[0].name == "Test Book 2"
    assert books_to_review[1].name == "Test Book 1"