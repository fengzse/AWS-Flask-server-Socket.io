from flask import render_template

from . import main


# main blueprint and views.py is to test server, will be deleted
@main.route('/', methods=['GET'])
def index():
    return render_template('socketio_demo.html')
