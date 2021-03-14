def print_books(books):
    for b in books:
        print(b.id, b.name, b.date_of_origin)


def print_reviews(reviews):
    for r in reviews:
        print(r.id, r.book.name, r.date_of_review)

