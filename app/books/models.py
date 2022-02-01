from app import db
from marshmallow import Schema, fields, validate
from app.authors.models import AuthorSchema, Author
from flask_sqlalchemy import BaseQuery
from werkzeug.datastructures import MultiDict
from app.utils import convert_string_to_date_format


book_author = db.Table(
    "book_author",
    db.Column(
        "book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True
    ),
    db.Column(
        "author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True
    ),
)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=True)
    published_date = db.Column(db.Date, nullable=True)
    language = db.Column(db.String(2), nullable=False)
    info_link = db.Column(db.String(255), nullable=False)
    authors = db.relationship(
        "Author",
        secondary=book_author,
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}>: {self.authors}"

    def __str__(self):
        return f"<{self.__class__.__name__}>: {self.authors}"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def apply_filter(query: BaseQuery, params: MultiDict) -> BaseQuery:
        query = query.join(Author, Book.authors)
        if "author" in params.keys():
            author_value = params["author"]
            if author_value:
                query = query.filter(
                    Book.authors.any(
                        Author.first_and_last_name.ilike(f"%{author_value}%")
                    )
                )

        if "title" in params.keys():
            title_value = params["title"]
            if title_value:
                query = query.filter(Book.title.ilike(f"%{title_value}%"))

        if "language" in params.keys():
            language_value = params["language"]
            if language_value:
                query = query.filter(
                    Book.language.ilike(f"%{language_value}%")
                )

        if "published_date[lte]" in params.keys():
            published_date_lte_value = params["published_date[lte]"]
            if published_date_lte_value:
                query = query.filter(
                    Book.published_date
                    <= convert_string_to_date_format(published_date_lte_value)
                )
        if "published_date[gte]" in params.keys():
            published_date_gte_value = params["published_date[gte]"]
            if published_date_gte_value:
                query = query.filter(
                    Book.published_date
                    >= convert_string_to_date_format(published_date_gte_value)
                )

        return query


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=100))
    isbn = fields.Integer(required=True)
    number_of_pages = fields.Integer(required=True)
    published_date = fields.Date("%Y-%m-%d", required=True)
    language = fields.String(required=True, validate=validate.Length(max=2))
    info_link = fields.String(required=True, validate=validate.Length(max=255))
    authors = fields.Pluck(
        "AuthorSchema",
        "first_and_last_name",
        many=True,
    )
    authors_book = fields.List(fields.String, load_only=True, required=True)


book_schema = BookSchema()
