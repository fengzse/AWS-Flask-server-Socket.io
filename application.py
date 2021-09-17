from app import create_application, socketio
from flask_cors import *

application = create_application()
CORS(application, supports_credentials=True)  # CORS(application, resources=r'/*')
app = application


@socketio.on('connected', namespace='/client_name')
def connected_msg(msg):
    print(msg)
    socketio.emit('connectConfirm', {'Server': 'Connect confirmed'}, namespace='/client_name')


# front-end sends request by giving <tag_timestamp> in url, server responds
if __name__ == '__main__':
    socketio.run(application, port=8000, debug=True)
