from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Lock
from random import randint
from classes.Player import Player
from classes.Spaceship import Spaceship
from classes.Gamespace import Gamespace

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

game_data = Gamespace()

@app.route('/')
def index():
        return render_template('index.html')


#Start the background thread to 'animate' the game objects
def init_game():
    global thread
    with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=update_game)

@socketio.on('join', namespace='/test')
def join_event(joinmsg):
    global game_data
    game_data.new_player(request.sid)
 
 #Python objects are not translatable to JSON
    #Build a JSON object containing ship data to return to the client
    players_json = build_json()
    init_game()
    emit('draw', players_json)

#move_ship is triggered when the user presses an arrow key
#This function sets the direction of movement
@socketio.on('move_ship', namespace='/test')
def move_event(direction):
    global game_data
    player = game_data.players[request.sid]
    if player.shipid in game_data.spaceships:
        ship = game_data.spaceships[player.shipid]
        ship.set_direction(direction)

@socketio.on('fire', namespace='/test')
def fire_missile():
    global game_data
    
    player = game_data.players[request.sid]
    if player.shipid in game_data.spaceships:
        game_data.new_projectile(request.sid)

#Re-draw the canvas 30x a second
def update_game():
    global game_data
    while True:
        socketio.sleep(1.0/30.0)
        if game_data.gameover():
            game_data.reset()
        else :
            game_data.update()
        ret = build_json()
        socketio.emit('draw', ret, namespace='/test')

#Builds data in format that the client side can understand
def build_json():
    global game_data
    #Python dictionaries are essentially the same format as JSON
    ret = {}
    ret["players"] = {}
    ret["projectiles"] = []
    ret["asteroids"] = []

    for projectile in game_data.projectiles:
        projectile_json = {'x':projectile.x, 'y':projectile.y, 'rot':projectile.rotation}
        ret["projectiles"].append(projectile_json)

    for a in game_data.asteroids:
        asteroid_json = {'x':a.x, 'y':a.y, 'radius':a.radius, 'spin':a.spin, 'points':a.points}
        ret["asteroids"].append(asteroid_json)

    for player in game_data.players:
        if game_data.players[player].shipid in game_data.spaceships:
            ship = game_data.spaceships[game_data.players[player].shipid]
            #index the data by playerid
            ret["players"][player] = {'shipid':ship.shipid, 'radius': ship.radius, 'colour':ship.colour, 'x':ship.x, 'y':ship.y, 'rot':ship.rotation}
    
    return ret

@socketio.on('disconnect', namespace='/test')
def leave_event():
    global game_data
    #Remove players who have disconnected from the stored game data
    player = game_data.players[request.sid]
    del game_data.players[request.sid]
    del game_data.spaceships[player.shipid]


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
