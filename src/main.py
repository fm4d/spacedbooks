#!/usr/bin/env python3

import argparse

from src.db_models import db, Book, Review
from src.commands import (add_review, add_book, list_reviews, list_books,
                          remove_book, list_books_to_review, remove_review)
from src.util import print_reviews, print_books


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

    remove_review_parser = subparsers.add_parser('remove-review')
    remove_review_parser.add_argument('id', type=id, help="review id", action='store')

    return parser


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
        print_books(list_books(cli_args.order_by, cli_args.asc_or_desc))
    elif cli_args.command == 'add-review':
        add_review(cli_args.name, cli_args.date_shift)
    elif cli_args.command == 'remove-review':
        remove_review(cli_args.id)
    elif cli_args.command == 'list-reviews':
        print_reviews(list_reviews(cli_args.order_by, cli_args.asc_or_desc))
    else:
        list_books_to_review()
