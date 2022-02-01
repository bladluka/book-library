from app.authors.models import Author, AuthorSchema, author_schema
from flask import jsonify, request, Response
from app import db


class AuthorService:
    @staticmethod
    def get_authors() -> Response:
        authors = Author.query.all()
        authors_schema = AuthorSchema(many=True)

        return jsonify(
            {"success": "true", "data": authors_schema.dump(authors)}
        )

    @staticmethod
    def get_author(author_id: int) -> Response:
        author = Author.query.get_or_404(
            author_id, description=f"Author with id {author_id} not found"
        )
        return jsonify({"success": "true", "data": author_schema.dump(author)})

    @staticmethod
    def add_author(args: dict):
        author = Author(**args)
        db.session.add(author)
        db.session.commit()

        return (
            jsonify({"success": "true", "data": author_schema.dump(author)}),
            201,
        )

    @staticmethod
    def update_author(args: dict, author_id: int):
        author = Author.query.get_or_404(
            author_id, description=f"Author with id {author_id} not found"
        )
        author.first_and_last_name = args["first_and_last_name"]
        db.session.commit()

        return jsonify({"success": "true", "data": author_schema.dump(author)})

    @staticmethod
    def delete_author(author_id: int):
        author = Author.query.get_or_404(
            author_id, description=f"Book with id {author_id} not found"
        )
        db.session.delete(author)
        db.session.commit()

        return jsonify(
            {"data": f"Author with id {author_id} has been deleted"}
        )
