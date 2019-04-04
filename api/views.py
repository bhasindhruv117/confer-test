from api.run import app
from flask import jsonify
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
socketio = SocketIO(app)
@app.route('/')
def index():
    socketio.run(app)
    return jsonify({'message': 'Hello, World!'})
@app.route('/chat')
def chat():
    return render_template("ChatApp.html")

def messageRecived():
        print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json):
   print('recived my event: ' + str(json))
   socketio.emit('my response', json)

# @socketio.on('my_event_msg')
# def handle_my_msg_event(json):
#    print('recived my msg: ' + str(json))
#    socketio.emit('my response', json)
#
#
# @socketio.on('on typing')
# def connectuser():
#     socketio.emit('on typing', typing)
#
#
# @socketio.on('chat message')
# def chat_message(msg):
#    print('recived my chat message: ' + str(msg))
#    socketio.emit('chat message', msg)
#
#
# @socketio.on('connect user')
# def connect_user(user):
#    print('connect user: ' + str(user))
#    socketio.emit('connect user', user)

