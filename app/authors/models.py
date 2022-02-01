from app import db
from marshmallow import Schema, fields, validate


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    first_and_last_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}>: {self.first_and_last_name}"

    def __str__(self):
        return f"<{self.__class__.__name__}>: {self.first_and_last_name}"


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_and_last_name = fields.String(
        required=True, validate=validate.Length(max=100)
    )


author_schema = AuthorSchema()
