from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from random import randint
from classes.Player import Player
from classes.Spaceship import Spaceship

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

players = {}
ships = {}

@app.route('/')
def index():
        return render_template('index.html')

@socketio.on('join', namespace='/test')
def join_event(joinmsg):
    current_sock = request.sid
    user = Player(request.sid)
    ship = Spaceship()
    players[user.playerid] = {"shipid":ship.shipid, "colour":ship.colour, "x":ship.x, "y":ship.y, "v":ship.velocity}
    
    emit('joined', players)

@socketio.on('disconnect', namespace='/test')
def leave_event():
    del players[request.sid]

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
