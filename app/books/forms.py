from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FieldList,
    DateField,
    validators,
    FormField,
)
from wtforms.validators import DataRequired, InputRequired, NumberRange
from werkzeug.routing import ValidationError
from app.books.models import Book


class BookForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    isbn = IntegerField("ISBN", validators=[InputRequired()])
    number_of_pages = IntegerField(
        "Number of pages", validators=[DataRequired()]
    )
    published_date = DateField("Published date", validators=[DataRequired()])
    language = StringField(
        "Language",
        validators=[
            DataRequired(),
            validators.Length(min=2, max=2, message="Użyj 2-literowego skótu"),
        ],
    )
    info_link = StringField("Info link", validators=[DataRequired()])
    authors = FieldList(StringField("Authors"))

    # def validate_isbn(self, field):
    #     check = Book.query.filter(Book.isbn == field.data).first()
    #     if check:
    #         raise ValidationError("Book with this ISBN already exists")
    #     return field.data


# class Unique(object):
#     """ validator that checks ISBN uniqueness """
#     def __init__(self, model, field, message=None):
#         self.model = model
#         self.field = field
#         if not message:
#             message = 'Book with this ISBN already exists'
#         self.message = message
#
#     def __call__(self, form, field):
#         check = self.model.query.filter(self.field == field.data).first()
#         if check:
#             raise ValidationError(self.message)
