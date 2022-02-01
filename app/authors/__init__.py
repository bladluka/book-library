from flask import Blueprint

authors_bp = Blueprint("authors", __name__)

from app.authors import models, routes
