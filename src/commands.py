import datetime

from src.db_models import Book, Review
from config import SPACED_REPETITION_INTERVALS, LOGGER


def add_book(name, author, isbn='', date_shift='+0'):
    if date_shift[0] == '+':
        adjusted_date = datetime.date.today() + datetime.timedelta(int(date_shift[1:]))
    elif date_shift[0] == '-':
        adjusted_date = datetime.date.today() - datetime.timedelta(int(date_shift[1:]))
    else:
        raise Exception("Only +XX or -XX allowed for add_book date")

    Book(name=name, author=author, isbn=isbn, date_of_origin=adjusted_date).save()

    LOGGER.debug("Created new Book(id, name={}, date_origin={})".format(id, name, adjusted_date))


def _get_book(name_or_id):
    if name_or_id.isdigit():
        book = Book.get(Book.id == name_or_id)
    else:
        book = Book.get(Book.name == name_or_id)

    return book


def remove_book(name_or_id):
    book_to_remove = _get_book(name_or_id)
    id, name = book_to_remove.id, book_to_remove.name
    book_to_remove.delete_instance()

    LOGGER.debug("Removed Book(id={}, name={})".format(id, name))


def list_books(order_by, asc_or_desc):
    mapper = {
        'id': Book.id,
        'date_created': Book.date_created,
        'date_of_origin': Book.date_of_origin,
        'name': Book.name
    }

    if asc_or_desc == 'asc':
        order_field = mapper[order_by].asc()
    else:
        order_field = mapper[order_by].desc()

    return list(Book.select().order_by(order_field))


def add_review(name_or_id, date_shift):
    if date_shift[0] == '+':
        adjusted_date = datetime.date.today() + datetime.timedelta(int(date_shift[1:]))
    elif date_shift[0] == '-':
        adjusted_date = datetime.date.today() - datetime.timedelta(int(date_shift[1:]))
    else:
        raise Exception("Only +XX or -XX allowed for add_review date")

    book = _get_book(name_or_id)
    Review(book=book, date_of_review=adjusted_date).save()

    LOGGER.debug("Created Review(Book.name={}, date_of_review={})".format(
        book.name,
        adjusted_date
    ))


def remove_review(id):
    r = Review.get_by_id(id)
    r.delete_instance()


def list_reviews(order_by, asc_or_desc):
    mapper = {
        'id': Review.id,
        'date_created': Review.date_created,
        'date_of_review': Review.date_of_review,
        'book_name': Book.name,
        'book_id': Book.id
    }

    if asc_or_desc == 'asc':
        order_field = mapper[order_by].asc()
    else:
        order_field = mapper[order_by].desc()

    return list(Review.select().join(Book, on=(Review.book == Book.id)).order_by(order_field))


def _get_books_and_overdue_days_to_review():
    for b in Book.select():
        reviews = Review.select().join(Book, on=(Review.book == Book.id)).where(Book.id == b.id).order_by(Review.date_of_review.asc())

        if not reviews:
            days_since_last_review = (datetime.date.today() - b.date_of_origin).days
            if days_since_last_review > SPACED_REPETITION_INTERVALS[0]:
                days_overdue = days_since_last_review - SPACED_REPETITION_INTERVALS[0]
                yield (days_overdue, b)
        else:
            days_since_last_review = (datetime.date.today() - reviews[-1].date_of_review).days
            # days_past_scheduled_review = SPACED_REPETITION_INTERVALS[len(reviews)]) - days_since_last_review
            if days_since_last_review > SPACED_REPETITION_INTERVALS[len(reviews)]:
                days_overdue = days_since_last_review - SPACED_REPETITION_INTERVALS[0]
                yield (days_overdue, b)


def list_books_to_review():
    """ sort (days_overdue, book) tuple by days_overdue, more days_overdue => first in sorted list"""
    days_books_pairs = list(_get_books_and_overdue_days_to_review())
    days_books_pairs.sort(key=lambda t: t[0], reverse=True)
    return [p[1] for p in days_books_pairs]