'''
=====================================================================================================================================================
FILE		: state_graph.py
DESCRIPTION	: implements data structures and functions to maintain state of the board
AUTHOR		: Rohit Rane
EmAIL		: rrrane@indiana.edu
=====================================================================================================================================================
'''

import math;

class Graph:

	#================================================== SECTION: CONSTRUCTORS ===================================================================	
	def __init__(self):
		
		#graphs representing diagonal relations
		self.diagonal1 = [[]];
		self.diagonal2 = [[]];
		
		#graph representing horizontal relation
		self.horizontal = [[]];
		
		#graph representing vertical relation
		self.vertical = [[]];
		
		#list of moves made so far
		self.move_list = [[0,0]];
		
		#flag: set if last move won
		self.final_flag = False;
		
		pass
	#================================================== SECTION END =============================================================================
	
	#================================================== SECTION: FUNCTIONS ======================================================================

	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: insert_node
	#PARAMETERS	: move_no, row_index, col_index
	#DESCRIPTION	: inserts move in move_list and appropriate graph
	#RETURNS	: 'True' if last move won and 'False' otherwise
	#--------------------------------------------------------------------------------------------------------------------------------------------
	
	def insert_node(self, move_no, row_index, col_index):
		
		self.move_list.append([row_index, col_index]);
		self.build_graph(move_no, row_index, col_index);
		self.final_flag = self.check_if_done(move_no);
		return self.final_flag;
	#____________________________________________________________________________________________________________________________________________

	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: build_graph
	#PARAMETERS	: move_no, row_index, col_index
	#DESCRIPTION	: appropriate graph
	#RETURNS	: none
	#--------------------------------------------------------------------------------------------------------------------------------------------
		
	def build_graph(self, move_no, row_index, col_index):
		self.diagonal1.append([]);
		self.diagonal2.append([]);
		self.horizontal.append([]);
		self.vertical.append([]);
		
		for i in range(1, move_no):
			r1 = self.move_list[i][0]
			c1 = self.move_list[i][1]
			
			'''Check for connectivity and update appropriate graph'''
			if abs(r1 - row_index) == 1 and c1 == col_index:
				self.vertical[i].append(move_no)
				self.vertical[move_no].append(i)
			elif r1 == row_index and abs(c1 - col_index) == 1:
				self.horizontal[i].append(move_no)
				self.horizontal[move_no].append(i)
			elif (r1 - row_index == 1 and c1 - col_index == 1) or (r1 - row_index == -1 and c1 - col_index == -1):
				self.diagonal1[i].append(move_no)
				self.diagonal1[move_no].append(i)
			elif (r1 - row_index == 1 and c1 - col_index == -1) or (r1 - row_index == -1 and c1 - col_index == 1):
				self.diagonal2[i].append(move_no)
				self.diagonal2[move_no].append(i)
		
		
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: check_if_done
	#PARAMETERS	: move_no
	#DESCRIPTION	: determines whether last move won or not by traversing a graph
	#RETURNS	: 'True' if last move won and 'False' otherwise
	#--------------------------------------------------------------------------------------------------------------------------------------------

	
	def check_if_done(self, move_no):
		
		is_h_connected = False
		is_v_connected = False
		is_d1_connected = False
		is_d2_connected = False
		
		is_h_connected = self.traverse(self.horizontal, move_no)
		is_v_connected = self.traverse(self.vertical, move_no)
		is_d1_connected = self.traverse(self.diagonal1, move_no)
		is_d2_connected = self.traverse(self.diagonal2, move_no)	
		
		
		return (is_h_connected or is_v_connected or is_d1_connected or is_d2_connected)
		
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: traverse
	#PARAMETERS	: graph, node
	#DESCRIPTION	: checks if ast move won by traversing particular graph starting from a given node
	#RETURNS	: 'True' if last move won and 'False' otherwise
	#--------------------------------------------------------------------------------------------------------------------------------------------

	def traverse(self, graph, node):
		
		n = node
		hop_count = 0
		temp_queue = [n]
		isVisited = []
		
		for i in range(1, len(graph) + 1):
			isVisited.append(False)
		
		while len(temp_queue) > 0:	
			
			j = temp_queue.pop(0)
			isVisited[j] = True
			
			hop_count += 1
			
			for k in graph[j]:
				if not isVisited[k]:
					temp_queue.append(k)
			
			
		if hop_count >= 4:
			return True
		
		return False
		
		pass
	#____________________________________________________________________________________________________________________________________________
	
	#--------------------------------------------------------------------------------------------------------------------------------------------
	#NAME		: remove_last_inserted
	#PARAMETERS	: none
	#DESCRIPTION	: restores all the graphs to previous state
	#RETURNS	: last move
	#--------------------------------------------------------------------------------------------------------------------------------------------


	def remove_last_inserted(self):
		n = len(self.move_list) -1
		if self.final_flag:
			self.final_flag = False
		
		if n <= 0:
			return -1, -1, -1, False
		
		node = self.move_list.pop(n)
		
		for j in self.horizontal[n]:
			self.horizontal[j].remove(n)
		
		self.horizontal.pop(len(self.horizontal) - 1)
		
		for j in self.vertical[n]:
			self.vertical[j].remove(n)
		
		self.vertical.pop(len(self.vertical) - 1)
		
		for j in self.diagonal1[n]:
			self.diagonal1[j].remove(n)
		
		self.diagonal1.pop(len(self.diagonal1) -1)
		
		for j in self.diagonal2[n]:
			self.diagonal2[j].remove(n)
		
		self.diagonal2.pop(len(self.diagonal2) -1)
		
		return n, node[0], node[1], self.final_flag
	#____________________________________________________________________________________________________________________________________________

	#======================================================== SECTION END =======================================================================
