def print_books(books):
    for b in books:
        print('[{}] "{}" by {} {}(first read on {})'.format(
            b.id,
            b.name,
            b.author,
            '(isbn {})'.format(b.isbn) if b.isbn else '',
            b.date_of_origin
        ))


def print_books_to_review(books):
    for b in books:
        print('[{}] "{}" by {}'.format(
            b.id,
            b.name[:50] + "..." if len(b.name) > 50 else b.name,
            b.author
        ))


def print_reviews(reviews):
    for r in reviews:
        print(r.id, r.book.name, r.books.author, r.date_of_review)

