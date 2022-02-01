from app.books.models import Book, BookSchema, book_schema
from app.authors.models import Author
from flask import jsonify, request, Response, abort
from app import db
import copy


class BookService:
    @staticmethod
    def get_books() -> Response:
        books = Book.apply_filter(Book.query, request.args)
        books_schema = BookSchema(many=True)

        return jsonify({"success": "true", "data": books_schema.dump(books)})

    @staticmethod
    def get_book(book_id: int) -> Response:
        book = Book.query.get_or_404(
            book_id, description=f"Book with id {book_id} not found"
        )
        return jsonify({"success": "true", "data": book_schema.dump(book)})

    @staticmethod
    def add_book(args: dict):
        if Book.query.filter(Book.isbn == args["isbn"]).first():
            abort(
                409,
                description=f'Book with ISBN {args["isbn"]} already exists',
            )

        args_dto = copy.deepcopy(args)
        del args["authors_book"]
        book = Book(**args)

        for author in args_dto["authors_book"]:
            author_book = Author.query.filter(
                Author.first_and_last_name == author
            ).first()
            if not author_book:
                abort(404, description=f"Author {author} not found")
            book.authors.append(author_book)
            db.session.add(book)

        db.session.commit()

        return (
            jsonify({"success": "true", "data": book_schema.dump(book)}),
            201,
        )

    @staticmethod
    def update_book(args: dict, book_id: int):
        book = Book.query.get_or_404(
            book_id, description=f"Book with id {book_id} not found"
        )
        if Book.query.filter(
            Book.isbn == args["isbn"], Book.id != book_id
        ).first():
            abort(
                409,
                description=f'Book with ISBN {args["isbn"]} already exists',
            )

        book.authors = []

        for author in args["authors_book"]:
            author_book = Author.query.filter(
                Author.first_and_last_name == author
            ).first()
            if not author_book:
                abort(404, description=f"Author {author} not found")
            book.authors.append(author_book)
            db.session.add(book)

        book.update(**args)
        db.session.commit()

        return jsonify({"success": "true", "data": book_schema.dump(book)})

    @staticmethod
    def delete_book(book_id: int):
        book = Book.query.get_or_404(
            book_id, description=f"Book with id {book_id} not found"
        )
        db.session.delete(book)
        db.session.commit()

        return jsonify({"data": f"Book with id {book_id} has been deleted"})
