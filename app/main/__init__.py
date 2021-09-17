from flask import Blueprint
# main blueprint and views.py is to test server, will be deleted
main = Blueprint('main', __name__)

from .import views
