from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

@app.route('/')
def index():
        return render_template('index.html')

@socketio.on('join', namespace='/test')
def join_event(joinmsg):
    x = randint(0, 600)
    y = randint(0, 400)
    emit('joined', {'x': x, 'y': y})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
