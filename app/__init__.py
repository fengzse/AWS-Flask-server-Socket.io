from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_application():
    application = Flask(__name__)

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_1_0_blueprint
    application.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    socketio.init_app(application, async_mode="threading", cors_allowed_origins='*')

    return application
