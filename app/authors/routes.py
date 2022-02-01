from app.authors import authors_bp
from app.authors.service import AuthorService
from app.authors.models import author_schema
from webargs.flaskparser import use_args
from app.utils import validate_json_content_type


@authors_bp.route("/api/v1/authors", methods=["GET"])
def get_authors():
    return AuthorService.get_authors()


@authors_bp.route("/api/v1/authors/<int:author_id>", methods=["GET"])
def get_author(author_id: int):
    return AuthorService.get_author(author_id)


@authors_bp.route("/api/v1/authors", methods=["POST"])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def add_author(args: dict):
    return AuthorService.add_author(args)


@authors_bp.route("/api/v1/authors/<int:author_id>", methods=["PUT"])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(args: dict, author_id: int):
    return AuthorService.update_author(args, author_id)


@authors_bp.route("/api/v1/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id: int):
    return AuthorService.delete_author(author_id)
