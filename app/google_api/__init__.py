from flask import Blueprint

google_bp = Blueprint("google", __name__)

from app.google_api import service
