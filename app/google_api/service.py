import requests
import json
from app.books.models import Book
from app.authors.models import Author
from app import db
from datetime import date
from app.utils import convert_google_date


google_api_authors = []
google_api_books = []


def get_books_google_api(search_value):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={search_value}"
    )
    try:
        data_json = response.json()["items"]
        for item in data_json:
            title = item.get("volumeInfo").get("title")
            identifier_types = item.get("volumeInfo").get(
                "industryIdentifiers"
            )
            isbn = ""
            if identifier_types:
                for identifier in identifier_types:
                    if identifier["type"] == "ISBN_13":
                        isbn = identifier["identifier"]
            number_of_pages = item.get("volumeInfo").get("pageCount")
            published_date = convert_google_date(
                item.get("volumeInfo").get("publishedDate")
            )
            language = item.get("volumeInfo").get("language")
            info_link = item.get("volumeInfo").get("infoLink")
            authors = item.get("volumeInfo").get("authors")

            google_api_fields = [
                title,
                isbn,
                number_of_pages,
                published_date,
                language,
                info_link,
                authors,
            ]

            if isbn != "" and authors is not None:
                google_api_books.append(google_api_fields)
                google_api_authors.append(google_api_fields[6])

    except Exception as e:
        print(e)


def load_authors(author_list):
    author_keys = Author.__table__.columns.keys()[1:]
    new = []
    for authors in author_list:
        if len(authors) > 1:
            author_list.remove(authors)
            for author in authors:
                author = [author]
                new.append(author)
    final = author_list + new
    for author in final:
        if not Author.query.filter(
            Author.first_and_last_name == author
        ).first():
            author = dict(zip(author_keys, author))
            author = Author(**author)
            db.session.add(author)
            db.session.commit()
    db.session.close()
    google_api_authors.clear()


def load_books(book_list):
    book_keys = Book.__table__.columns.keys()[1:]
    for book in book_list:
        if not Book.query.filter(Book.isbn == book[1]).first():
            _book = dict(zip(book_keys, book))
            _book = Book(**_book)
            for author in book[6]:
                if author is not None:
                    author_book = Author.query.filter(
                        Author.first_and_last_name == author
                    ).first()
                    _book.authors.append(author_book)
            db.session.add(_book)
            db.session.commit()
    db.session.close()
    google_api_books.clear()
