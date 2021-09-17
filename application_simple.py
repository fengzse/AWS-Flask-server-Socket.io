from flask import Flask, json
from flask import jsonify, render_template, current_app, request, url_for, g
import datetime
from flask_cors import *
from flask_socketio import SocketIO, emit

application = Flask(__name__)
socketio = SocketIO(application, async_mode="threading", cors_allowed_origins='*')
CORS(application, supports_credentials=True)


@application.route('/', methods=['GET'])
def index():
    return render_template('socketio_demo.html')


@socketio.on('connected', namespace='/client_name')
def connected_msg(msg):
    print(msg)
    socketio.emit('connectConfirm', {'Server': 'Connect confirmed'}, namespace='/client_name')


def send_start_trigger(send_start):
    socketio.emit('start', json.dumps(send_start), json=True, namespace='/client_name')


# front-end sends request by giving <tag_timestamp> in url, server responds
@application.route('/start/<int:start_timestamp>', methods=['GET'])
def api_start(start_timestamp):
    # example timestamp 1559568302
    start_time = datetime.datetime.fromtimestamp(start_timestamp)
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    str_start_time = start_time.strftime(time_format)

    send_start = {
        'message': 'Start recording',
        'start_time': str_start_time
    }
    send_start_trigger(send_start)
    current_app.logger.info('the api_start implemented')

    return jsonify(send_start)


@application.route('/records/<int:tag_timestamp>', methods=['GET'])
def api_send_records(tag_timestamp):
    # example timestamp 1559568302
    tag_time = datetime.datetime.fromtimestamp(tag_timestamp)
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    str_tag_time = tag_time.strftime(time_format)
    delta_time = datetime.timedelta(seconds=5)
    five_second_backward = tag_time - delta_time
    five_second_forward = tag_time + delta_time
    str_5s_back = five_second_backward.strftime(time_format)
    str_5s_forw = five_second_forward.strftime(time_format)
    send_record = {
        'message': 'Records start to send',
        'tag_time': str_tag_time,
        'send_record_from': str_5s_back,
        'sending_ends_at': str_5s_forw
    }
    socketio.emit('records', json.dumps(send_record), json=True, namespace='/client_name')
    return jsonify(send_record)


@application.route('/stop/<int:stop_timestamp>', methods=['GET'])
def api_stop(stop_timestamp):
    # example timestamp 1559568302
    stop_time = datetime.datetime.fromtimestamp(stop_timestamp)
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    str_stop_time = stop_time.strftime(time_format)

    send_stop = {
        'message': 'Stop recording',
        'stop_time': str_stop_time
    }
    socketio.emit('stop', json.dumps(send_stop), json=True, namespace='/client_name')
    return jsonify(send_stop)


if __name__ == '__main__':
    socketio.run(application, port=8000, debug=True)
