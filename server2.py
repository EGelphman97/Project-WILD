from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

iden = "4"
eventName = "Roomba"
dateAndTime = ""

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('train')
def train(data):
    print("train", data)
    event()

def event():
    dateAndTime = time.strftime("%c")
    emit('event', {iden:dateAndTime})

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)