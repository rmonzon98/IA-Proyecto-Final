import socketio
import random

#New address
host_address = 'localhost'
port_address = '4000'
address = 'http://' + host_address + ':' + port_address

#New socket 
socket = socketio.Client()

# connect to server
socket.connect(address)

#Tournament id
tour_id = 12

possibleMovements = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29]]

#Validate movement
def validateMovement(movement):

	#Null
	if movement == []:
		return False
	
	num = None

	for conv in (int, float, complex):
		try: 
			num = conv(movement[0])
			break
		except ValueError:
			pass
	
	if num is None:
		return False
	
	for conv in (int, float, complex):
		try: 
			num = conv(movement[1])
			break
		except ValueError:
			pass

	if num is None:
		return False

	movement = [int(movement[0]), int(movement[1])]

	if movement[0] < 0 or movement[0] >1:
		return False

	if movement[1] < 0 or movement[1] >29:
		return False

	return True
	
#Client connection
@socket.on('connect')
def on_connect():
	socket.emit('signin',
		{
			'user_name': 'Raul Monzon',
        	'tournament_id': tour_id,
        	'user_role': 'player'
		}
	)
	print('Connection has been completed\n')

#Client disconnection
@socket.on('disconnect')
def on_disconnect():
   
    socket.disconnect() print('Disconnection has been completed\n')


#Beginning of the game
@socket.on('ready')
def on_ready(data):

	#Client move
	print("The game is about to start.\n")

	movement = random.choice(possibleMovements)

	while validateMovement(movement) != True:
		movement = random.choice(possibleMovements)
		possibleMovements.remove(movement)

	socket.emit('play', 
		{	
			'tournament_id': tour_id,
			'player_turn_id': data['player_turn_id'],
			'game_id': data['game_id'],
			'movement': movement
        }
    )

#End of the game
@socket.on('finish')
def finish(data): 

	global possibleMovements
	possibleMovements = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29]]

	socket.emit('player_ready', 
		{
        	"tournament_id":tour_id,
        	"game_id":data['game_id'],
        	"player_turn_id":data['player_turn_id']
        }
    )
	print("The game has finished, waiting for new round\n")


