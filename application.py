from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Lock
from random import randint
from classes.Player import Player
from classes.Spaceship import Spaceship

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

all_players = {}
all_ships = {}

@app.route('/')
def index():
        return render_template('index.html')


@socketio.on('join', namespace='/test')
def join_event(joinmsg):
    global all_players
    global all_ships
    user = Player(request.sid)
    ship = Spaceship()
    user.shipid = ship.shipid

    #store arrays of ship and player objects in memory indexed by respective IDs
    all_ships[ship.shipid]=ship
    all_players[user.playerid]=user

    #Python objects are not translatable to JSON
    #Build a JSON object containing ship data to return to the client
    players_json = build_json()
    init_game()
    emit('draw', players_json)

#move_ship is triggered when the user presses an arrow key
#This function sets the direction of movement
@socketio.on('move_ship', namespace='/test')
def move_event(direction):
    global all_players
    global all_ships
    player = all_players[request.sid]
    ship = all_ships[player.shipid]
    ship.set_direction(direction)
    
    game_data = build_json()

    emit('draw', game_data)


#Start the background thread to 'animate' the game objects
def init_game():
    global thread
    with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=update_game)

#Re-draw the canvas 30x a second
def update_game():
    global all_ships
    while True:
        socketio.sleep(1.0/30.0)
        for ship in all_ships:
            all_ships[ship].move()
        game_data = build_json()
        socketio.emit('draw', game_data, namespace='/test')

#Builds data in format that the client side can understand
def build_json():
    global all_players
    global all_ships
    #Python dictionaries are essentially the same format as JSON
    ret = {}
    for player in all_players:
        ship = all_ships[all_players[player].shipid]
        #index the data by playerid
        ret[player] = {'shipid':ship.shipid, 'colour':ship.colour, 'x':ship.x, 'y':ship.y, 'v':ship.velocity, 'rotation':ship.rotation}
    return ret

@socketio.on('disconnect', namespace='/test')
def leave_event():
    global all_players
    global all_ships
    #Remove players who have disconnected from the stored game data
    player = all_players[request.sid]
    del all_players[request.sid]
    del all_ships[player.shipid]

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
