import json
from pathlib import Path
from app import db
from app.authors.models import Author
from app.books.models import Book
from app.commands import db_manage_bp
from datetime import datetime
from app.google_api.service import (
    get_books_google_api,
    load_authors,
    load_books,
    google_api_books,
    google_api_authors,
)


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / "samples" / file_name
    with open(json_path, encoding="utf8") as file:
        data_json = json.load(file)
    return data_json


@db_manage_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """ "Add sample data to database" """
    try:
        data_json = load_json_data("authors.json")
        for item in data_json:
            author = Author(**item)
            db.session.add(author)

        data_json = load_json_data("books.json")
        for item in data_json:
            item["published_date"] = datetime.strptime(
                item["published_date"], "%Y-%m-%d"
            )
            book = Book(**item)
            db.session.add(book)

        data_json = load_json_data("book_author.json")
        for item in data_json:
            author_id = item["author_id"]
            author = Author.query.get_or_404(author_id)
            book_id = item["book_id"]
            book = Book.query.get_or_404(book_id)
            author.books.append(book)

            db.session.add_all([author, book])

        db.session.commit()
        print("Data has been successfully added to database")

    except Exception as exc:
        print("Unexpected error: {}".format(exc))


@db_manage.command()
def add_google_books():
    """ "Add books from google api to database" """
    try:
        get_books_google_api("Hobbit")
        load_authors(google_api_authors)
        load_books(google_api_books)
        print("Data has been successfully added to database")

    except Exception as exc:
        print("Unexpected error: {}".format(exc))


@db_manage.command()
def remove_data():
    """ "Remove data from database" """
    try:
        db.session.execute("DELETE FROM book_author")
        db.session.execute("DELETE FROM books")
        db.session.execute("ALTER TABLE books AUTO_INCREMENT = 1")
        db.session.execute("DELETE FROM authors")
        db.session.execute("ALTER TABLE authors AUTO_INCREMENT = 1")
        db.session.commit()
        print("Data has been successfully removed from database")
    except Exception as exc:
        print("Unexpected error: {}".format(exc))
