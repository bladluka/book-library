from app.books import books_bp
from flask import render_template, redirect, flash, request, url_for
from app.books.models import Book
from app import db
from .forms import BookForm
from app.google_api.service import (
    get_books_google_api,
    load_authors,
    load_books,
    google_api_books,
    google_api_authors,
)


def add_edit_book(book_id):
    errors = None
    if book_id is None:
        form = BookForm()
        book = Book(
            title=form.title.data,
            isbn=form.isbn.data,
            number_of_pages=form.number_of_pages.data,
            published_date=form.published_date.data,
            language=form.language.data,
            info_link=form.info_link.data,
            authors=form.authors.data,
        )
    else:
        book = Book.query.filter_by(id=book_id).first_or_404()
        form = BookForm(obj=book)

    if request.method == "POST":
        if form.validate_on_submit():
            if book_id is None:
                db.session.add(book)
                db.session.commit()
                flash("Book has been added")
                return redirect(url_for("books.get_all_books"))
            else:
                form.populate_obj(book)
                db.session.commit()
                flash("Book has been edited")
                return redirect(url_for("books.get_all_books"))
        else:
            errors = form.errors
    return render_template("book_form.html", form=form, errors=errors)


@books_bp.route("/books", methods=["GET", "POST"])
def get_all_books():
    books = Book.apply_filter(Book.query, request.args)
    _books = Book.query.all()
    for book in books:
        authors = ", ".join(map(str, book.authors))
        authors = authors.replace("<Author>:", "")
        book.stringAuthors = authors

    return render_template("books.html", books=books)


@books_bp.route("/new-book", methods=["GET", "POST"])
def add_new_book():
    return add_edit_book(None)


@books_bp.route("/edit/book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    return add_edit_book(book_id)


@books_bp.route("/delete/book/<int:book_id>", methods=["POST"])
def delete_single_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book has been deleted")
    return redirect(request.referrer)


@books_bp.route("/google/books", methods=["GET", "POST"])
def add_google_book():
    if request.method == "POST":
        search_value = request.form.get("search_value")
        print(search_value)
        get_books_google_api(search_value)
        load_authors(google_api_authors)
        load_books(google_api_books)
        flash(
            f"Books from https://www.googleapis.com/books/v1/volumes?q={search_value} have been added"
        )
        return redirect(url_for("books.get_all_books"))

    return render_template("google_api.html")
