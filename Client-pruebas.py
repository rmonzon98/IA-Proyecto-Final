import socketio
#import random

#DetermineMove:
#This process evaluates every free space on the board,
#every time a new space is tested, a value is given to it
#depending of the "quality" of the move
#Recieves: board, player_turn_id
#Return: the move with the best "quality"
def DetermineMove(board, player_turn_id):
	free = []
	free = FreeSpace(board)

	quality = -10000
	nextMove = []
	for i in free:
		#MiniMax
		score = MiniMax(board,0,False,player_turn_id,-100000,+100000,0,i)
		#In case a move with better "quality" is found, 
		#quality takes the value of score and nextMove
		#save the free space
		if (score > quality):
			nextMove.clear()
			quality = score			
			nextMove.append(i)

	return [nextMove[0][0],nextMove[0][1]]

#FreeSpace:
#This operation verifies which spaces on the board are free
#Recieves: board
#Return: a group of available spaces
def FreeSpace(board):
	free = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 99:
				free.append((i,j))
	return free

#MiniMax
def MiniMax(board, depth, isMax, player_turn_id,alpha, beta,nodeIndex,move):
#def MiniMax(board,player_turn_id,alpha,beta,depth,nodeIndex,isMax,move):
	player = player_turn_id if isMax else (player_turn_id % 2) + 1

	_,validate = NextMove(board, player_turn_id, move, not isMax)
	
	#if current board state is a terminal state :
	if (depth == 0 or validate != 0):
		return validate
	
	free = []
	free = FreeSpace(board)
	#if isMaximizingPlayer :
	if (isMax):
		quality = -100000
		for i in free:
			board = NextMove(board,player,move,isMax)
			#Minimax
			score = MiniMax(board, depth + 1,False, player, alpha, beta,0, i)
			quality = max(quality, score)
			alpha = max(alpha, score)
			if (beta <= alpha):
				break

		board[move[0]][move[1]] = 99
		return quality

	#if isMinimizingPlayer :
	if (not(isMax)):
		quality = 100000
		for j in free:
			board = NextMove(board,player,move,isMax)
			#Minimax
			score = MiniMax(board,depth + 1, True,  player,  alpha, beta,0, j)
			quality = min(quality,score)
			beta = min(beta, score)

		board[move[0]][move[1]] = 99
		return quality

	return 0


#This code is based on the algorithm shared on the class's forum
def NextMove(board, player_turn, move, isMAx):
	
	N = 6
	EMPTY = 99

	contadorPuntos = 0
	contadorPuntos2 = 0

	acumulador = 0
	contador = 0

	board = list(map(list,board))
	for i in range(len(board[0])):
		if ((i +1) % 6) != 0:
			if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
				contadorPuntos = contadorPuntos + 1
			acumulador = acumulador + N
		else: 
			contador = contador + 1
			acumulador = 0
	
	acumulador = 0
	contador = 0	
	
	board[move[0]][move[1]] = 0

	board = list(map(list,board))
	for i in range(len(board[0])):
		if ((i +1) % 6) != 0:
			if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
				contadorPuntos2 = contadorPuntos2 + 1
			acumulador = acumulador + N
		else: 
			contador = contador + 1
			acumulador = 0

	diferencia = contadorPuntos2 - contadorPuntos
	if (contadorPuntos < contadorPuntos2):
		if (player_turn == 1):
			if (diferencia == 2):
				board[move[0]][move[1]] = 2
			if (diferencia == 1):
				board[move[0]][move[1]] = 1
		elif (player_turn == 2):
			if (diferencia == 2):
				board[move[0]][move[1]] = -2
			if (diferencia == 1):
				board[move[0]][move[1]] = -1

	if (isMAx):
		return (board,diferencia)
	else:
		return (board, diferencia * -1)
			


#New address
host_address = '40.88.136.34'
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
			'user_name': 'prrros',
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

