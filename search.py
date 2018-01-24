'''
=====================================================================================================================================================
FILE	: search.py
NAME	: Rohit Rane
EMAIL	: rrrane@indiana.edu
=====================================================================================================================================================
'''

import board
import random
import math

#======================================================== SECTION: MAIN FUNCTIONS ===================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: perft
#PARAMETERS	: board, depth
#Description	: counts number of leaf nodes at given depth
#RETURN		: count (number of leaf nodes)
#----------------------------------------------------------------------------------------------------------------------------------------------------

def perft(board, depth):
	
	#Get all possible moves
	legal_moves = board.generate_moves()
	
	#Check if last move caused win
	lmv = board.last_move_won()
	
	#if last move won the game or no valid move available
	if lmv or len(legal_moves) <= 0:
		#Unmake last move made by calling function
		board.unmake_last_move()
		return 1
	
	#if last move did not win the game and valid moves are available,
	#but depth limit is reached
	if depth == 1:
		board.unmake_last_move()
		return len(legal_moves)
	
	#initialize variable to count leaf nodes visited so far
	count = 0
	
	#For all legal moves from current state, call perft recursively
	for i in legal_moves:
		board.make_move(i)
		count += perft(board, depth - 1)
	
	#Unmake last move made by calling function before returning count
	board.unmake_last_move()
	
	#return number of leaf nodes visited
	return count
	
	pass
#____________________________________________________________________________________________________________________________________________________

#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: find_win
#PARAMETERS	: board, depth
#DESCRIPTION	: determines if there is a Forced Win at given depth
#RETURNS	: string message
#----------------------------------------------------------------------------------------------------------------------------------------------------

def find_win(board, depth):
	
	#Get which player has a turn now
	me = board.get_player()
	
	#Select move with maximum utility
	v, a, b, m = max_value(board, me, -math.inf, math.inf, depth)
	
	#Return appropriate result
	if v == 1:
		strng =  'WIN BY PLAYING ' + str(m)
		return strng
	
	if v == -1:
		return 'ALL MOVES LOSE'
	
	return 'NO FORCED WIN IN ' + str(depth) + ' MOVES'
	pass
#____________________________________________________________________________________________________________________________________________________
#======================================================== SECTION END ===============================================================================

#======================================================== SECTION: HELPER FUNCTIONS =================================================================

#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: shuffle
#PARAMETERS	: lst (list to shuffle)
#DESCRIPTION	: shuffles the list to reorder the moves
#RETURNS	: ret_lst (reordered list of moves)
#----------------------------------------------------------------------------------------------------------------------------------------------------

def shuffle(lst):
	mid = math.floor(len(lst)/2)
	
	#check if length of the list is even
	if len(lst) % 2 == 0:
		mid -=1
	
	#initialize pointers, one to scan downwards and other to scan upwards from the middle element
	ptr = [mid, mid + 1]
	turn = 0
	
	#Initialize empty list to return
	ret_lst = []
	
	#if input list is not empty then perform shuffling
	if len(lst) > 0:
		while (turn == 0 and ptr[0] >= 0) or (turn == 1 and ptr[1] < len(lst)) :
			
			ret_lst.append(lst[ptr[turn]])
			if turn == 0:
				ptr[turn] -= 1
			else:
				ptr[turn] += 1
			
			turn ^= 1
	
	return ret_lst
#____________________________________________________________________________________________________________________________________________________	
	
#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: max_value
#PARAMETERS	: board, plyer, alpha, beta, depth
#DESCRIPTION	: gets a move with maximum utility
#		  Source - "Russel S., Norvig P.; Artificial Intelligence- A modern approach 2nd edition"
#RETURNS	: v (maximum value), a (local alpha), b (local beta), ret_mov (move with maximum utility)
#----------------------------------------------------------------------------------------------------------------------------------------------------

def max_value(board, player, alpha, beta, depth):
	
	#if terminal state then return utility of leaf node
	if is_terminal(board):
		u, alp, bet = utility(board, player)
		return u, alp, bet, -1
	
	#if reached depth limit then return utility 0
	#that is consider it a draw
	if depth == 0:
		u = 0
		return u, -1, -1, -1
	
	
	v = - math.inf
	ret_mov = -1
	a, b = alpha, beta
	
	#get list of possible moves and shuffle it
	legal_moves = shuffle(board.generate_moves())
	
	#find move with maximum utility	
	for mov in legal_moves:
		board.make_move(mov)
		max_val, a1, b1, m  = min_value(board, player, a, b, depth - 1)
		if max_val > v:
			v, ret_mov = max_val, mov
		
		board.unmake_last_move()
		if v >= b:
			return v, a, b, ret_mov
		
		a = max(a, v)

	return v, a, b, ret_mov
#____________________________________________________________________________________________________________________________________________________

#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: min_value
#PARAMETERS	: board, player, alpha, beta, depth
#DESCRIPTION	: gets a move with minimum utility
#		  Source - "Russel S., Norvig P.; Artificial Intelligence- A modern approach 2nd edition"
#RETURNS	: v (minimum value), a (local alpha), b (local beta), ret_mov (move with minimum utility
#----------------------------------------------------------------------------------------------------------------------------------------------------
	
def min_value(board, player, alpha, beta, depth):
	
	#if terminal state then return utility of leaf node
	if is_terminal(board):
		u, alp, bet = utility(board, player)
		return u, alp, bet, -1
	
	#if reached depth limit then return utility 0
	#that is, consider it a draw
	if depth == 0:
		u = 0
		return u, -1, -1, -1
	
	v = math.inf
	ret_mov = -1
	a, b = alpha, beta
	
	#get list of possible moves and shuffle it
	legal_moves = shuffle(board.generate_moves())
	
	#find a move with minimum utility
	for mov in legal_moves:
		board.make_move(mov)
		min_val, a1, b1, m = max_value(board, player, a, b, depth - 1)
		if min_val < v:
			v, ret_mov = min_val, mov
		
		board.unmake_last_move()
		if v <= a:
			b = v
			return v, a, b, ret_mov
		
		b = min(b, v)
		
	return v, a, b, ret_mov
#____________________________________________________________________________________________________________________________________________________

#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: is_terminal
#PARAMETERS	: board
#DESCRIPTION	: checks if a board is in its terminal state
#RETURNS	: True / False
#----------------------------------------------------------------------------------------------------------------------------------------------------

def is_terminal(board):
	
	#Get possible moves		
	legal_moves = board.generate_moves()
	
	#Check if last move caused any player win the game
	lmw = board.last_move_won()
	
	#Return 'True' in either of the two conditions is true
	if len(legal_moves) == 0 or lmw:
		return True
	
	#Return 'False' otherwise
	return False
#____________________________________________________________________________________________________________________________________________________

#----------------------------------------------------------------------------------------------------------------------------------------------------
#NAME		: utility
#PARAMETERS	: board, player
#DESCRIPTION	: gets utility of the leaf node
#RETURNS	: utility of the leaf node
#----------------------------------------------------------------------------------------------------------------------------------------------------
	
def utility(board, player):
	
	#check if last_move_won
	lmw = board.last_move_won()
	
	#get the player who has a turn
	next_player = board.get_player()
	
	#Return -1 if calling player loses
	if lmw and player == next_player:
		return -1, -1, -1
	
	#Return 1 if calling player wins
	if lmw and player != next_player:
		return 1, 1, 1
	
	#Return 0 otherwise
	return 0, 0, 0
#____________________________________________________________________________________________________________________________________________________
#======================================================= SECTION END ================================================================================
