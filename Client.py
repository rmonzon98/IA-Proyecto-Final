"""
Raul Monzon 
17014
Client.py
"""

import socketio

#FreeSpace:
#This operation verifies which spaces on the board are free
#Recieves: board
#Returns: a group of available spaces
def FreeSpace(board):
	free = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 99:
				free.append((i,j))
	return free

#MiniMax
#Recieves: board, id of the player, alpha, beta, depth of tree, node index, ¿are we maximizing player?, move to be tested
#Returns: optimal move depending on their quality
def MiniMax(board,player_turn_id,alpha,beta,depth,nodeIndex,isMaximizingPlayer,move):
	player = player_turn_id if isMaximizingPlayer else (player_turn_id % 2) + 1

	_,validate = NextMove(board, player_turn_id, move, not isMaximizingPlayer)
	
	#if current board state is a terminal state :
	if (depth == 0 or validate != 0):
		return validate
	
	free = []
	free = FreeSpace(board)
	#if isMaximizingPlayer :
	if (isMaximizingPlayer):
		quality = -100000
		for i in free:
			board = NextMove(board,player,move,isMaximizingPlayer)
			#Minimax
			score = MiniMax(board, player, alpha, beta, depth + 1, 0, False, i)
			quality = max(quality, score)
			alpha = max(alpha, score)
			if (beta <= alpha):
				break

		board[move[0]][move[1]] = 99
		return quality

	#if isMinimizingPlayer :
	if (not(isMaximizingPlayer)):
		quality = 100000
		for j in free:
			board = NextMove(board,player,move,isMaximizingPlayer)
			#Minimax
			score = MiniMax(board, player, alpha, beta, depth + 1, 0, True, j)
			quality = min(quality,score)
			beta = min(beta, score)

		board[move[0]][move[1]] = 99
		return quality

	return 0

#DetermineMove:
#This process evaluates every free space on the board,
#every time a new space is tested, a value is given to it
#depending of the "quality" of the move
#Recieves: board, player_turn_id
#Returns: the move with the best "quality"
def DetermineMove(board, player_turn_id):
	free = []
	free = FreeSpace(board)

	quality = -10000
	nextMove = []
	for i in free:
		#MiniMax
		score = MiniMax(board, player_turn_id, -100000, +100000, 0, 0, False, i)
		#In case a move with better "quality" is found, 
		#quality takes the value of score and nextMove
		#save the free space
		if (score > quality):
			nextMove.clear()
			quality = score			
			nextMove.append(i)

	return [nextMove[0][0],nextMove[0][1]]

#This code was taken from the class's forum
def ContarPuntos(board):
	acumuladorPuntos= 0
	N = 6
	EMPTY = 99
	acumulador = 0
	contador = 0
	for i in range(len(board[0])):
		if ((i +1) % 6) != 0:
			if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
				acumuladorPuntos = acumuladorPuntos + 1
			acumulador = acumulador + N
		else: 
			contador = contador + 1
			acumulador = 0
	return acumuladorPuntos

#NextMove
#We compare the actual state of the board with the state of the board after the move
#Receives: board, player_turn, move, isMax
#Returns: state of the board and the diferrence in the score
def NextMove(board, player_turn, move, isMAx):

	board = list(map(list,board))
	acumuladorPuntos = ContarPuntos(board)

	board[move[0]][move[1]] = 0
	board = list(map(list,board))
	acumuladorPuntos2 = ContarPuntos(board)

	diferencia = acumuladorPuntos2 - acumuladorPuntos
	if (acumuladorPuntos < acumuladorPuntos2):
		if (player_turn == 1):
			board[move[0]][move[1]] = 2 if diferencia == 2 else 1
		elif (player_turn == 2):
			board[move[0]][move[1]] = -2 if diferencia == 2 else -1

	if (isMAx):
		return (board,diferencia)
	else:
		return (board, diferencia * -1)
			
#New address
host_address = 'localhost'
port_address = '4000'
address = 'http://' + host_address + ':' + port_address

#New socket 
socket = socketio.Client()

#Tournament id
tour_id = 12

#counters of game
won_games_counter = 0
lost_games_counter = 0

# connect to server
socket.connect(address)

#Client connection
@socket.on('connect')
def on_connect():
	print('Connecting with server')
	socket.emit('signin',
		{
			'user_name': '1 decada de mala suerte al que me gane - Raul Monzon',
        	'tournament_id': tour_id,
        	'user_role': 'player'
		}
	)
	print('Connection has been completed\n')


#Beginning of the game
@socket.on('ready')
def on_ready(data):

	movement = DetermineMove(data["board"],data["player_turn_id"])
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

	global won_games_counter
	global lost_games_counter

	if (data['player_turn_id'] == data ['winner_turn_id']):
		won_games_counter = won_games_counter + 1
	else:
		lost_games_counter = lost_games_counter + 1
	
	games_counter=lost_games_counter + won_games_counter
	print('Game number', games_counter, 'has finished')
	print('----------------------------------------------')
	print('Your scores are:')
	print('Won games: ', won_games_counter)
	print('Lost games: ', lost_games_counter)

	socket.emit('player_ready', 
		{
        	"tournament_id":tour_id,
        	"game_id":data['game_id'],
        	"player_turn_id":data['player_turn_id']
        }
    )
	print('This match has finished, waiting for a new match')

