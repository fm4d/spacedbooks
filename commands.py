import datetime

from db_models import Book, Review
from config import SPACED_REPETITION_INTERVALS


def add_book(name, date_shift):
    if date_shift[0] == '+':
        adjusted_date = datetime.date.today() + datetime.timedelta(int(date_shift[1:]))
    elif date_shift[0] == '-':
        adjusted_date = datetime.date.today() - datetime.timedelta(int(date_shift[1:]))
    else:
        raise Exception("Only +XX or -XX allowed for add_book date")

    Book(name=name, date_origin=adjusted_date).save()


def get_book(name_or_id):
    if name_or_id.isdigit():
        book = Book.get(Book.id == name_or_id)
    else:
        book = Book.get(Book.name == name_or_id)

    return book


def remove_book(name_or_id):
    book_to_remove = get_book(name_or_id)
    book_to_remove.delete_instance()


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

    books = Book.select().order_by(order_field)
    for b in books:
        print(b.id, b.name, b.date_of_origin)


def add_review(name_or_id, date_shift):
    if date_shift[0] == '+':
        adjusted_date = datetime.date.today() + datetime.timedelta(int(date_shift[1:]))
    elif date_shift[0] == '-':
        adjusted_date = datetime.date.today() - datetime.timedelta(int(date_shift[1:]))
    else:
        raise Exception("Only +XX or -XX allowed for add_review date")

    book = get_book(name_or_id)
    Review(book=book, date_of_review=adjusted_date).save()


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

    reviews = Review.select().join(Book, on=(Review.book == Book.id)).order_by(order_field)
    for r in reviews:
        print(r.id, r.book.name, r.date_of_review)


def list_books_to_review():
    for b in Book.select():
        reviews = Review.select().join(Book, on=(Review.book == Book.id)).where(Book.id == b.id).order_by(Review.date_of_review.asc())

        if not reviews:
            days_since_last_review = (datetime.date.today() - b.date_of_origin)
            if days_since_last_review > datetime.timedelta(SPACED_REPETITION_INTERVALS[0]):
                print(b.id, b.name)
        else:
            days_since_last_review = (datetime.date.today() - reviews[-1].date_of_review)
            if days_since_last_review > datetime.timedelta(SPACED_REPETITION_INTERVALS[len(reviews)]):
                print(b.id, b.name)