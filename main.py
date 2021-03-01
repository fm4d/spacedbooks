#!/usr/bin/env python3

import datetime
import argparse
from peewee import *

db = SqliteDatabase('books.db')


class Book(Model):
    name = CharField()
    date_created = DateField(default=datetime.date.today)
    date_of_origin = DateField(default=datetime.date.today)

    class Meta:
        database = db # This model uses the "people.db" database.


class Review(Model):
    book = ForeignKeyField(Book)
    date_created = DateField(default=datetime.date.today)
    date_of_review = DateField(default=datetime.date.today)

    class Meta:
        database = db


def create_argparser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    add_book_parser = subparsers.add_parser('add-book')
    add_book_parser.add_argument('name', type=str, help="book name", action='store')
    add_book_parser.add_argument('date_shift', type=str, help="+ or - X days",
                                 nargs='?', default='+0')

    remove_book_parser = subparsers.add_parser('remove-book')
    remove_book_parser.add_argument('name', type=str, help="book name or id", action='store')

    list_books_parser = subparsers.add_parser('list-books')
    list_books_parser.add_argument('order_by', type=str, help="name or date_of_origin or date_created",
                                   action='store', nargs='?', default='id')
    list_books_parser.add_argument('asc_or_desc', type=str, help="asc or desc",
                                   action='store', nargs='?', default='asc')

    list_reviews_parser = subparsers.add_parser('list-reviews')
    list_reviews_parser.add_argument('order_by', type=str, help="name or date_of_review or date_created",
                                     action='store', nargs='?', default='id')
    list_reviews_parser.add_argument('asc_or_desc', type=str, help="asc or desc",
                                     action='store', nargs='?', default='asc')

    add_review_parser = subparsers.add_parser('add-review')
    add_review_parser.add_argument('name', type=str, help="book name or id", action='store')
    add_review_parser.add_argument('date_shift', type=str,
                                   help="+ or - X days since/to review",
                                   nargs='?', default='+0')

    return parser


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


if __name__ == '__main__':
    db.connect()
    db.create_tables([Book, Review])

    arg_parser = create_argparser()
    cli_args = arg_parser.parse_args()
    if cli_args.command == 'add-book':
        add_book(cli_args.name, cli_args.date_shift)
    elif cli_args.command == 'remove-book':
        remove_book(cli_args.name)
    elif cli_args.command == 'list-books':
        list_books(cli_args.order_by, cli_args.asc_or_desc)
    elif cli_args.command == 'add-review':
        add_review(cli_args.name, cli_args.date_shift)
    elif cli_args.command == 'list-reviews':
        list_reviews(cli_args.order_by, cli_args.asc_or_desc)



