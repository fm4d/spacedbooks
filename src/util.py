from config import MAIL_ADDRESS_SENDER, MAIL_ADDRESS_RECEIVER, MAIL_PASSWORD

import ssl
import smtplib
from email.mime.text import MIMEText


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


def send_mail(books):
    def book_to_mail_str(book):
        return '[{}] "{}" by {}'.format(
            book.id,
            book.name[:50] + "..." if len(book.name) > 50 else book.name,
            book.author
        )

    msg = MIMEText("\n".join(book_to_mail_str(book) for book in books))
    msg['Subject'] = "Spacedbooks daily review"
    msg['From'] = MAIL_ADDRESS_SENDER
    msg['To'] = MAIL_ADDRESS_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', '465', context=ssl.create_default_context()) as server:
        server.login(MAIL_ADDRESS_SENDER, MAIL_PASSWORD)
        server.sendmail(MAIL_ADDRESS_SENDER, MAIL_ADDRESS_RECEIVER, msg.as_string())
        server.quit()
