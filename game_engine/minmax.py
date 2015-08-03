from world_interface import gamesforthebrain_com
import sys
import time

class min_max():
    
    def __init__(self):
        
        self.game = gamesforthebrain_com.game_iface()
        
    def get_start_state(self):
        
        return self.game.get_state()
        
    def get_successors(self, dict_board, position):   
        '''
            Return all possible successor positions of a given piece
            List of Tuples; The tuples contain the move, and the utility of the board for that move 
            
            Inputs
            @dict_board: current state of the board
            
            @position: position on board being checked
        '''
        # Check the position, is it us or them
        # If us, is it a normal piece, or a king
        # If normal King check for positions heading down the board
        # Check heading up the board
        # If enemy occupies successor, check if jump possible
        # if jump possible check successors of that position for other enemies
        #
        possible_moves = []
        # convert position to x,y
        x,y = int(position[0][-2:-1]),int(position[0][-1:])
        start_space = 'space'+str(x)+str(y)
        # Check there's room to the right to move
        if x < 7:
            move_to = 'space'+str(x+1)+str(y+1)
            if y < 7 and dict_board[move_to] == 'gray.gif':
                # 0
                possible_moves.append(('move', 1, start_space, move_to))
                
            move_to = 'space'+str(x+1)+str(y-1)
            if y > 0 and dict_board[move_to] == 'gray.gif':
                # 1
                possible_moves.append(('move', 1, start_space, move_to))
        # Check there's room to the left to move
        if x > 0:
            move_to = 'space'+str(x-1)+str(y+1)
            if y < 7 and dict_board[move_to] == 'gray.gif':
                # 2
                possible_moves.append(('move', 1, start_space, move_to))
            move_to = 'space'+str(x-1)+str(y-1)
            if y > 0 and dict_board[move_to] == 'gray.gif':
                # 3
                possible_moves.append(('move', 1, start_space, move_to))
                
        # All possible jumps
        jump_possibles = []
        while True:
            before = len(jump_possibles)
            jump_possibles += self.check_jump(dict_board, position)
            if len(jump_possibles) == before:
                break
        for jump_possible in jump_possibles:
            possible_moves.append(jump_possible)
        # print possible_moves
        return possible_moves
        
    def check_jump(self, dict_board, start_pos):
        '''
            Check if a jump is possible from the given position
            @dict_board: State of current board
            @start_pos: Position of piece
            
            
            @return: int
        '''
        jump_positions = []
        # Jumps require that y +/- 1 and x +/- 1 contain an opposing piece
        # and y +/- 2 and x +/- 2 is possible to land on
        # Kings can go in any direction
        # Computer normals y can only be decreased
        # Player normals y can only be increased
        start_pos_x,start_pos_y = int(start_pos[0][-2:-1]),int(start_pos[0][-1:])
        #start_pos = start_pos[0]
        ###################################################
        # Computer #
        ###################################################
        friend = 'me'
        enemy = 'you'
        friend_king = 'me2k'
        enemy_king = 'you2k'
        if friend in start_pos[1]:
            # Computer
            # Forward check: x +/- 1, y - 1 for opposition
            # But keep in mind that we cannot jump off the board
            gain = 0
            if start_pos_x < 6 and start_pos_y > 1:
                check_pos = 'space'+str(start_pos_x+1)+str(start_pos_y-1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x+2)+str(start_pos_y-2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
            gain = 0           
            if start_pos_x > 1 and start_pos_y > 1:
                check_pos = 'space'+str(start_pos_x-1)+str(start_pos_y-1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x-2)+str(start_pos_y-2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
                        
        if friend_king in start_pos[1]:
            # King so check backwards
            gain = 0
            if start_pos_x < 6 and start_pos_y < 6:
                check_pos = 'space'+str(start_pos_x+1)+str(start_pos_y+1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x+2)+str(start_pos_y+2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
            
            gain = 0           
            if start_pos_x > 1 and start_pos_y < 6:
                check_pos = 'space'+str(start_pos_x-1)+str(start_pos_y+1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x-2)+str(start_pos_y+2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
                        
        ###################################################
        # Us #
        ###################################################
        
        friend = 'you'
        enemy = 'me'
        friend_king = 'you2k'
        enemy_king = 'me2k'
        if friend in start_pos[1]:
            # Forward check: x +/- 1, y + 1 for us
            # But keep in mind that we cannot jump off the board
            gain = 0
            if start_pos_x < 6 and start_pos_y < 6:
                check_pos = 'space'+str(start_pos_x+1)+str(start_pos_y+1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x+2)+str(start_pos_y+2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
            
            gain = 0           
            if start_pos_x > 1 and start_pos_y < 6:
                check_pos = 'space'+str(start_pos_x-1)+str(start_pos_y+1)            
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x-2)+str(start_pos_y+2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
                        
        if friend_king in start_pos[1]:
            # King so check backwards
            gain = 0
            if start_pos_x < 6 and start_pos_y > 1:
                check_pos = 'space'+str(start_pos_x+1)+str(start_pos_y-1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x+2)+str(start_pos_y-2)
                    if "gray.gif" in dict_board[end_pos]:
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
            
            gain = 0           
            if start_pos_x > 1 and start_pos_y > 1:
                check_pos = 'space'+str(start_pos_x-1)+str(start_pos_y-1)
                if enemy in dict_board[check_pos]:
                    if enemy_king in dict_board[check_pos]:
                        gain += 8
                    else:
                        gain += 3
                    end_pos = 'space'+str(start_pos_x-2)+str(start_pos_y-2)
                    if "gray.gif" in dict_board[end_pos]:
                        
                        copied_board = dict_board.copy()
                        copied_board[check_pos] = 'gray.gif'
                        jump_positions.append((start_pos, 
                                               check_pos, 
                                               end_pos, gain, copied_board))
                        
                        return self.check_jump(copied_board, end_pos)
        
        return jump_positions
            
    def get_utility(self, dict_board):
        # Having Kings is worth more
        # Enemy having Kings is worth less to us (ie. more to them)
        # Enemy having pieces is worth less to us (more to them)
        # Us having pieces is worth more
        us_kings = []
        computer_kings = []
        us_norm = []
        computer_norm = []
        for position in dict_board.items():
            if 'me1.gif' in position:
                computer_norm.append(position)
            if 'you1.gif' in position:
                us_norm.append(position)
            if "you2k.gif" in position:
                us_kings.append(position)
            if "me2k.gif" in position:
                computer_kings.append(position)
        #TODO list:       
        # Control of territory is good
        # Further up the board is good
        return ((len(us_norm)+len(us_kings)*5)-(len(computer_norm)+len(computer_kings)*5))
        
    
    def is_complete(self, dict_board):
        '''
            There are two ways to "win"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            1) remove all of the enemies pieces
            2) prevent the enemy from making any moves AND our side controls 
            more of the empty space
        '''
        # No enemies left
        if  len([x for x in dict_board.items() if 'me' in x[1]]) == 0:
            return True
        
        # Enemy has no moves
        if len([self.get_successors(dict_board, x) for x in dict_board.items() if 'me' in x[1]]) == 0:
            return True
        
        return False
        
    def get_max(self, dict_board, depth):
        if self.is_complete(dict_board) or depth>=10:
            return (None, self.get_utility(dict_board))
        
        highest_score = -sys.maxint - 1
        move = (None, sys.maxint)
        for move_list in [self.get_successors(dict_board, x) for x in dict_board.items() if 'you' in x[1]]:
            for move in move_list:
                # clone the dict_board
                copied_board = dict_board.copy()
                # simulate the move
                copied_board[move[-1:]]=copied_board[move[2]][0]
                for space in move[2:-1]:
                    copied_board[space]='gray.gif'
                depth += 1
                score = self.get_min(copied_board, depth)[1]
                if score > highest_score:
                    highest_score = score
        return move
    
    def get_min(self, dict_board, depth):
        if self.is_complete(dict_board) or depth>=10:
            return (None, self.get_utility(dict_board))
        
        lowest_score = sys.maxint
        move = None
        for move_list in [self.get_successors(dict_board, x) for x in dict_board.items() if 'me' in x[1]]:
            for move in move_list:
                # clone the dict_board
                copied_board = dict_board.copy()
                # simulate the move
                copied_board[move[-1:]]=copied_board[move[2]][0]
                for space in move[2:-1]:
                    copied_board[space]='gray.gif'
                depth += 1
                score = self.get_max(copied_board, depth)[1]
                if score < lowest_score:
                    lowest_score = score
        return move
    
    def search(self, board):
	# Just a dirty hack, ignore me. Need it in the git repo though
        # sys.setrecursionlimit(1500)
        # Depth first search (so a stacks)
        # We're limiting our depth to n, because of time constraints involved in processing the whole tree.'
        # Create a copy of the list of tuples as a dictionary using dict comprehension.
        # if the board is empty, die a horrible death
        # Do it here so it's only done once, and it can be passed to all the helper methods 
        
        dict_board = {v[1]: v[0] for v in board}
        
        if not self.is_complete(dict_board):
            highest_score = -sys.maxint - 1
            best_move = None
            for move_list in [self.get_successors(dict_board, us_item) for us_item in dict_board.items() if 'you' in us_item[1]]:
                for move in move_list:
                    score = self.get_min(dict_board.copy(), 0)[1]
                    if score > highest_score:
                        highest_score = score
                        best_move = move
            self.game.move_piece(best_move[2], best_move[-1:][0])
            time.sleep(5)
            self.search(self.get_start_state())
            return best_move
        