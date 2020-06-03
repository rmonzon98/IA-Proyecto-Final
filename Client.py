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
	_,validate = LookAhead(board, player_turn_id, move, not isMaximizingPlayer)
	
	#if current board state is a terminal state :
	if (depth == 0 or validate != 0):
		return validate
	
	free = []
	free = FreeSpace(board)
	#if isMaximizingPlayer :
	if (isMaximizingPlayer):
		quality = -100000
		for i in free:
			board = LookAhead(board,player,move,isMaximizingPlayer)
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
			board = LookAhead(board,player,move,isMaximizingPlayer)
			#Minimax
			score = MiniMax(board, player, alpha, beta, depth + 1, 0, True, j)
			quality = min(quality,score)
			beta = min(beta, score)

		board[move[0]][move[1]] = 99
		return quality

	return 0

#DetermineMove:
#This function evaluates all the available moves using minimax() and 
#then returns the best move the maximizer can make.
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
		if (score > quality):
			nextMove.clear()
			quality = score			
			nextMove.append(i)

	return [nextMove[0][0],nextMove[0][1]]

#This code was upload to class's forum
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

#This code was upload to class's forum
def humanBoard(board):
    resultado = ''
    acumulador = 0

    for i in range(int(len(board[0])/5)):
        if board[0][i] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+6] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+12] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+18] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+24] == 99:
            resultado = resultado + '*   *\n'
        else:
            resultado = resultado + '* - *\n'

        if i != 5:
            for j in range(int(len(board[1])/5)):
                if board[1][j + acumulador] == 99:
                    resultado = resultado + '    '
                else:
                    resultado = resultado + '|   '
            acumulador = acumulador + 6
            resultado = resultado + '\n'

    return resultado

#LookAhead
#We compare the actual state of the board with the state of the board after the move
#Receives: board, player_turn, move, isMax
#Returns: state of the board and the diferrence in the score
def LookAhead(board, player_turn, move, isMAx):

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

"""
-------------------------------------------------------------------------------
							BEGIN OF PROGRAM	
-------------------------------------------------------------------------------
"""
			
#New address
host_address = '198.154.2 2'
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
			'user_name': 'Raul Monzon (Pantera negra)',
        	'tournament_id': tour_id,
        	'user_role': 'player'
		}
	)
	print('Connection has been completed\n')


#Beginning of the game
@socket.on('ready')
def on_ready(data):

	visualizeBoard = humanBoard (data['board'])
	print(visualizeBoard)

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
	print('Your statistics are:')
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
	print('----------------------------------------------')
	if (won_games_counter == 50):
		print('You are doing great')
	elif (won_games_counter == 100):
		print('You are killin it')
	elif (won_games_counter == 200):
		print ('You already passed the class')
	if (lost_games_counter == 50):
		print('You are being destroyed')
	elif (lost_games_counter == 100):
		print('Quit the tournament, at least you have honor')
	elif (lost_games_counter == 200):
		print ('You should have left the tournament')
	print(' ')

