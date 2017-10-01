from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from random import randint
from classes.Player import Player
from classes.Spaceship import Spaceship

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

all_players = {}
all_ships = {}

@app.route('/')
def index():
        return render_template('index.html')

@socketio.on('join', namespace='/test')
def join_event(joinmsg):
    user = Player(request.sid)
    ship = Spaceship()
    user.shipid = ship.shipid

    #store arrays of ship and player objects in memory indexed by respective IDs
    all_ships[ship.shipid]=ship
    all_players[user.playerid]=user

    #Python objects are not translatable to JSON
    #Build a JSON object containing ship data to return to the client
    players_json = build_json()

    emit('draw', players_json)


@socketio.on('move_ship', namespace='/test')
def move_event(direction):
    player = all_players[request.sid]
    ship = all_ships[player.shipid]
    ship = ship.move(ship, direction)
    
    all_ships[player.shipid] = ship

    ret = build_json()

    emit('draw', ret)

@socketio.on('disconnect', namespace='/test')
def leave_event():
    #Remove players who have disconnected from the stored game data
    player = all_players[request.sid]
    del all_players[request.sid]
    del all_ships[player.shipid]

def build_json():
    #Python dictionaries are essentially the same format as JSON
    ret = {}
    for player in all_players:
        ship = all_ships[all_players[player].shipid]
        #index the data by playerid
        ret[player] = {"shipid":ship.shipid, "colour":ship.colour, "x":ship.x, "y":ship.y, "v":ship.velocity}
    return ret

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
