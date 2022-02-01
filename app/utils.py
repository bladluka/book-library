from datetime import datetime, date
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
from flask import request


def convert_string_to_date_format(text: str) -> date:
    text = datetime.strptime(text, "%Y-%m-%d").date()
    return text


def convert_google_date(google_date):
    if google_date:
        if len(google_date) == 4:
            published_date = f"{google_date}-01-01"
        elif len(google_date) == 7:
            published_date = f"{google_date}-01"
        else:
            published_date = google_date
    else:
        published_date = None

    return published_date


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType("Content type must be application json")
        return func(*args, **kwargs)

    return wrapper
