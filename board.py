'''
=====================================================================================================================================================
FILE	: board.py
NAME	: Rohit Rane
EMAIL	: rrrane@indiana.edu
=====================================================================================================================================================
'''


import state_graph

class Board:
	
	#===================================================== SECTION: CONSTRUCTOR =================================================================
	
	def __init__(self):
		
		#Initialize pointers to all columns
		self.current_state = [0,0,0,0,0,0,0]
		
		#Initialize a list indicating which column is full
		self.isfull = [False, False, False, False, False, False, False]
		
		#Initialize graphs for both the players
		#These graphs store current state of the board from both player's perspective
		self.graph = [state_graph.Graph(), state_graph.Graph()]
		
		#Initialize move-number for both players
		#Move-number is used to identify each different move made by player
		self.move_no = [0, 0]
		
		#lmw: Variable to store 'last-move-won' status
		#Initialized to False
		self.lmw = False
		
		#board-state: string representing current state of the board
		self.board_state = [['-', '-', '-', '-', '-', '-', '-'],  ['-', '-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-', '-']] 
		
		#player: player who will make a move now
		self.player = 0
		pass
	#____________________________________________________________________________________________________________________________________________
	#========================================================== END SECTION =====================================================================	

	#====================================================== SECTION: FUNCTION ===================================================================

	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME 		: generate_moves():
	#PARAMETERS	: none
	#DESCRIPTION	: A function to find columns available to make a move
	#RETURNS	: list of possible moves
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def generate_moves(self):
		
		possible_moves = [];
		
		for i in range(0, 7):
			if not self.isfull[i]:
				possible_moves.append(i);
		
		return possible_moves;
		pass
	
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME 		: make_move
	#PARAMETERS 	: move
	#DESCRIPTION	: makes a move for a current player
	#RETURNS	: none
	#--------------------------------------------------------------------------------------------------------------------------------------------

	def make_move(self, move):
		
		#Increase pointer to the column 'move' by 1
		self.current_state[move] += 1;
		
		#Update colum status if current move causes it to become full
		if self.current_state[move] == 6:
			self.isfull[move] = True;
		
		#Update move-number for current player
		self.move_no[self.player] += 1
		
		#Update state graph for current player
		#Store value of 'last_move_won' status [True / False] returned by insert_node() operation
		self.lmw = self.graph[self.player].insert_node(self.move_no[self.player], self.current_state[move] - 1, move)
		
		#Update board-state string
		if self.player == 0:
			self.board_state[self.current_state[move] - 1][move] = 'o'
		else:
			self.board_state[self.current_state[move] - 1][move] = 'x'
		
		#Switch to other player
		self.player ^= 1
    		
		pass
	
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: unmake_last_move
	#PARAMETERS	: none
	#DESCRIPTION	: restores previous state of the board
	#RETURNS	: none
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def unmake_last_move(self):
		
		#Check if game has already started
		if self.move_no[self.player ^ 1] > 0:

			#Swith player to previous
			self.player ^= 1
			
			#Restore previous state of the graph
			mov, row, col, self.lmw = self.graph[self.player].remove_last_inserted()
			
			#Update move-number to previous value
			self.move_no[self.player] = mov - 1
			
			#Update column pointer to previous
			self.current_state[col] -= 1
			
			#Update column-status to False
			self.isfull[col] = False;
			
			#Update board-state string
			self.board_state[row][col] = '-'
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: last_move_won
	#PARAMETERS	: none
	#DESCRIPTION	: returns 'True' if last move resulted in win for any player and 'False' otherwise
	#RETURNS	: self.lmw [True / False]
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def last_move_won(self):
		return self.lmw
		pass
	#____________________________________________________________________________________________________________________________________________
 	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: __str__
	#PARAMETERS	: none
	#DESCRIPTION 	: returns current state of the board as a string
	#RETURNS	: state
	#--------------------------------------------------------------------------------------------------------------------------------------------
	 
	def __str__(self):
		state = ''
		for i in self.board_state:
			row = ''
			for j in i:
				row = row + '\t' + str(j)
			state = row + '\n' + state
		return state
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: get_player
	#PARAMETERS	: none
	#DESCRIPTION	: returns current player
	#RETURNS	: self.player
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def get_player(self):
		return self.player
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: is_first_move
	#PARAMETERS	: none
	#DESCRIPTION	: returns 'True' if current player has not played yet and 'False' otherwise
	#RETURNS	: True / False
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def is_first_move(self):
		if self.move_no[self.player] == 0:
			return True

		return False
	#___________________________________________________________________________________________________________________________________________
	#=========================================================== END SECTION ===================================================================
	
