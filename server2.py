from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

iden = "0"

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('train')
def train(data):
	while True:
		try:
			status = open("status.txt", "r")
			iden = status.read()
			status.close()
			emit('event', {iden:time.strftime("%c")})
			print("*********SENT**********")
			os.remove("status.txt")
			time.sleep(1)
		except IOError:
			pass
	time.sleep(2)


if __name__ == '__main__':
	socketio.run(app)