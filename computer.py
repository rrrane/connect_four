'''
=====================================================================================================================================================
FILE	: Player.py
NAME	: Rohit Rane
EMAIL	: rrrane@indiana.edu
=====================================================================================================================================================
'''

import random
import board
import math

class Player:

	#======================================================== SECTION: CONSTRUCTORS =============================================================
	def __init__(self):
		self.player_board = board.Board()
		self.lmw = False
		pass
	#======================================================== SECTION END =======================================================================
	
	#======================================================== SECTION: MAIN FUNCTIONS ===========================================================
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: name
	#PARAMETERS	: none
	#DESCRIPTION	: Returns name of the player
	#RETURNS	: string (name of the player)
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def name(self):
		return '2-PLY SEARCHER'
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: make_move
	#Parameters	: move
	#DESCRIPTION	: makes a move and changes the state of its internal board
	#RETURNS	: none
	#--------------------------------------------------------------------------------------------------------------------------------------------

	def make_move(self, move):
		self.lmw = self.player_board.make_move(move)
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: get_move
	#PARAMETERS	: none
	#DESCRIPTION	: gets a move with maximum utility
	#RETURNS	: ret_mov (move with maximum utility)
	#--------------------------------------------------------------------------------------------------------------------------------------------

	def get_move(self):
	
		#Get a number representing this player
		me = self.player_board.get_player()
		
		#Get a move with maximum utility value
		v, a, b, mov = self.max_value(self.player_board, me, -math.inf, math.inf, 3)
		
		return mov
		pass
	#____________________________________________________________________________________________________________________________________________

	#============================================================== SECTION END =================================================================
	
	#============================================================== SECTION: HELPER FUNCTIONS ===================================================
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: shuffle
	#PARAMETERS	: none
	#DESCRIPTION	: shuffles the input list for move ordering
	#RETURNS	: list of moves after ordering
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def shuffle(self, lst):
		mid = math.floor(len(lst)/2)
		
		if len(lst) % 2 == 0:
			mid -=1
		
		ptr = [mid, mid + 1]
		turn = 0
		ret_lst = []
		if len(lst) > 0:
			while (turn == 0 and ptr[0] >= 0) or (turn == 1 and ptr[1] < len(lst)) :
				
				ret_lst.append(lst[ptr[turn]])
				if turn == 0:
					ptr[turn] -= 1
				else:
					ptr[turn] += 1
				
				turn ^= 1
		
		return ret_lst
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: max_value
	#PARAMETERS	: board, player, alpha, beta, depth
	#DESCRIPTION	: gets the move with maximum utility
	#		  Source- "Russel S., Norvig P., Artificial Intelligence- a modern approach 2nd edition"
	#RETURNS	: v (utility value), a (local alpha), b(local beta), ret_mov (move with maximum utility)
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def max_value(self, board, player, alpha, beta, depth):
		
		#check if terminal state
		if self.is_terminal(board):
			u, alp, bet = self.utility(board, player)
			return u, alp, bet, -1
		
		#check if depth limit is reached
		if depth == 0:
			u = 0
			return u, -1, -1, -1
		
		
		v = - math.inf
		ret_mov = -1
		a, b = alpha, beta
		
		#Get list of possible moves
		legal_moves = self.shuffle(board.generate_moves())
		
		#Search for a move with maximum utility
		for mov in legal_moves:
			board.make_move(mov)
			max_val, a1, b1, m  = self.min_value(board, player, a, b, depth - 1)
			if max_val > v:
				v, ret_mov = max_val, mov
			
			board.unmake_last_move()
			if v >= b:
				return v, a, b, ret_mov
			
			a = max(a, v)
		
		return v, a, b, ret_mov
	#____________________________________________________________________________________________________________________________________________

	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: min_value
	#PARAMETERS	: board, player, alpha, beta, depth
	#DESCRIPTION	: gets the move with minimum utility
	#		  Source- "Russel S., Norvig P., Artificial Intelligence- a modern approach 2nd edition"
	#RETURNS	: v (utility value), a (local alpha), b(local beta), ret_mov (move with minimum utility)
	#--------------------------------------------------------------------------------------------------------------------------------------------
 
	def min_value(self, board, player, alpha, beta, depth):
		
		#check if termial state
		if self.is_terminal(board):
			u, alp, bet = self.utility(board, player)
			return u, alp, bet, -1
		
		#check if depth limit is reached
		if depth == 0:
			u = 0
			return u, -1, -1, -1
		
		v = math.inf
		ret_mov = -1
		a, b = alpha, beta
		
		#Get list of all possible moves
		legal_moves = self.shuffle(board.generate_moves())
		
		#Search for a move with minimum utility
		for mov in legal_moves:
			board.make_move(mov)
			min_val, a1, b1, m = self.max_value(board, player, a, b, depth - 1)
			if min_val < v:
				v, ret_mov = min_val, mov
			
			board.unmake_last_move()
			if v <= a:
				b = v
				return v, a, b, ret_mov
			
			b = min(b, v)
			
		return v, a, b, ret_mov
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: is_terminal
	#PARAMETERS	: board
	#DESCRIPTION	: returns 'True' if board is in terminal state and 'False' otherwise
	#RETURNS	: True / False
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def is_terminal(self, board):
		
		legal_moves = board.generate_moves()
		lmw = board.last_move_won()
		
		#return true if no possible move or last move won
		if len(legal_moves) == 0 or lmw:
			return True
		
		#return false otherwise
		return False
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: utility
	#PARAMETERS	: board, player
	#DESCRIPTION	: returns utility of the leaf node
	#RETURNS	: utility of leaf node
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def utility(self, board, player):
		lmw = board.last_move_won()
		
		next_player = board.get_player()
		
		if lmw and player == next_player:
			return -1, -1, -1
		
		if lmw and player != next_player:
			return 1, 1, 1
		
		return 0, 0, 0
	#____________________________________________________________________________________________________________________________________________
	
	#============================================================ SECTION END ===================================================================


