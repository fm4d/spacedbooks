def print_books(books):
    for b in books:
        print('[{}] "{}" by {} {}(first read on {})'.format(
            b.id,
            b.name,
            b.author,
            '(isbn {})'.format(b.isbn) if b.isbn else '',
            b.date_of_origin
        ))


def print_reviews(reviews):
    for r in reviews:
        print(r.id, r.book.name, r.books.author, r.date_of_review)

