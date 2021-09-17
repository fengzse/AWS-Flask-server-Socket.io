from flask import jsonify, request, url_for, g, json
import datetime
from . import api
from ..import socketio


'''
url_prefix='/api/v1.0' for redirecting to endpoints adding url_prefix automatically.
manually input URL into browser for testing using this full 
url: http://localhost:5000/api/v1.0/action/<tag_timestamp> to run 
'''


# front-end sends request by giving <tag_timestamp> in url, server responds
@api.route('/start/<int:start_timestamp>', methods=['GET'])
def api_start(start_timestamp):
    # example timestamp 1559568302
    start_time = datetime.datetime.fromtimestamp(start_timestamp)
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    str_start_time = start_time.strftime(time_format)

    send_start = {
        'message': 'Start recording',
        'start_time': str_start_time
    }
    socketio.emit('start', json.dumps(send_start), json=True, namespace='/client_name')
    return jsonify(send_start)


@api.route('/records/<int:tag_timestamp>', methods=['GET'])
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


@api.route('/stop/<int:stop_timestamp>', methods=['GET'])
def api_action(stop_timestamp):
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

'''
# these two functions are alternatives, not need now
@api.route('/api/v1.0/info', methods=['GET'])
def api_output():
    return jsonify(g.data_sent)


@api.route('/api/v1.0/send/<int:code>', methods=['POST'])
def api_input(code):
    json_data = request.json
    code = json_data.get('code')
    message = json_data.get('message')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    g.data_sent = {
        'code': code,
        'action': message,
        'action time': current_time
    }

    return jsonify(g.data_sent), 201, {'Location': url_for('api.api_output', code=code)}'''
