from PythonicWeb import PythonicWeb
from flask_socketio import SocketIO, emit
from flask import session
import os

socketio = SocketIO(PythonicWeb)

UPLOAD_FOLDER = '~/Pythonic_2019/'
PythonicWeb.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PythonicWeb.config['SECRET_KEY'] = os.urandom(12).hex()

# On connection
@socketio.on('connect')
def onConnect(**kwargs):
    print('onConnect() called: ')

# Receiving String messages
@socketio.on('message')
def handle_message(message):
    print('Received message: {}'.format(message))
    send(message)

#Receiving JSON messages
@socketio.on('json')
def handle_json(json):
    print('received json: {}'.format(str(json)))
    send(json, json=True)

#Custom event
@socketio.on('my event')
def handle_my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)

@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')

@socketio.on('my_event')
def test_message(message):
    print('>>> test_message() called')
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

if __name__ == '__main__':
    context = ('17262165_localhost.localdomain.cert', '17262165_localhost.localdomain.key')
    socketio.run(PythonicWeb, debug=True, host='0.0.0.0', ssl_context=context)

