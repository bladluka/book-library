from app.books import books_bp
from app.books.service import BookService
from app.books.models import book_schema
from webargs.flaskparser import use_args
from app.utils import validate_json_content_type


@books_bp.route("/api/v1/books", methods=["GET"])
def get_books():
    return BookService.get_books()


@books_bp.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id: int):
    return BookService.get_book(book_id)


@books_bp.route("/api/v1/books", methods=["POST"])
@validate_json_content_type
@use_args(book_schema, error_status_code=400)
def add_book(args: dict):
    return BookService.add_book(args)


@books_bp.route("/api/v1/books/<int:book_id>", methods=["PUT"])
@validate_json_content_type
@use_args(book_schema, error_status_code=400)
def update_book(args: dict, book_id: int):
    return BookService.update_book(args, book_id)


@books_bp.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    return BookService.delete_book(book_id)
