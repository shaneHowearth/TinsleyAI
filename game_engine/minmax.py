from world_interface import gamesforthebrain_com

class min_max():
    
    def __init__(self):
        self.game = gamesforthebrain_com.game_iface()
        
    def get_start_state(self):
        
        return self.game.get_state()
        
    def get_successors(self, dictBoard, position):   
        '''
            Return all possible successor positions of a given piece
            List of Tuples; The tuples contain the move, and the utility of the board for that move 
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
        x,y = position[1][-2:-1],position[1][-1:]
        x_possibles = []
        y_possibles = []
        if x < 7:
            x_possibles.append(x+1)
        if x > 0:
            x_possibles.append(x-1)
        if y < 7:
            y_possibles.append(y+1)
        if y > 0:
            y_possibles.append(y-1)
           
        positions = [] 
        for y_pos in y_possibles:
            for x_pos in x_possibles:
                positions.append('space'+str(x_pos)+str(y_pos))
        
        # single jumps
        # X+2 y+2
        # X+2 y-2
        # x-2 y+2
        # x-2 y-2
        # double jumps
        # x+4 y+4
        # x+4 y-4 
        # x-4 y+4
        # x-4 y-4
        # x y+4
        # x y-4
        # king only 
        # x+4 y
        # x-4 y   
        if 'me' in dictBoard(position):
            # computer
            # Check forward two 
            if "gray.gif" in dictBoard(positions[0]):
                possible_moves.append(positions[0])
            if "gray.gif" in dictBoard(positions[1]):
                possible_moves.append(positions[1])
            # If King Check backward two 
            if "me2k" in dictBoard(position):
                if "gray.gif" in dictBoard(positions[2]):
                    possible_moves.append(positions[2])
                if "gray.gif" in dictBoard(positions[3]):
                    possible_moves.append(positions[3])
            # If any enemy, check if jumping is possible
            # If jump possible, check for double jump
            pass
        else:
            # Us
            if "gray.gif" in dictBoard(positions[2]):
                possible_moves.append(positions[2])
            if "gray.gif" in dictBoard(positions[3]):
                possible_moves.append(positions[3])
            # If King Check backward two 
            if "you2k" in dictBoard(position):
                if "gray.gif" in dictBoard(positions[0]):
                    possible_moves.append(positions[0])
                if "gray.gif" in dictBoard(positions[1]):
                    possible_moves.append(positions[1])
            pass
        
        # Kings
        
            
    def get_utility(self, dictBoard):
        # Having Kings is worth more
        us_kings = []
        computer_kings = []
        us_norm = []
        computer_norm = []
        for position in dictBoard.items():
            if 'me1.gif' in dictBoard[position]:
                computer_norm.append((position, dictBoard[position]))
            if 'you1.gif' in dictBoard[position]:
                us_norm.append((position, dictBoard[position]))
            if "you2k.gif" in dictBoard[position]:
                us_kings.append((position, dictBoard[position]))
            if "me2k.gif" in dictBoard[position]:
                computer_kings.append((position, dictBoard[position]))
                
                
        # Losing pieces is bad
        # Jumping pieces is good
        # Control of territory is good
        # Further up the board is good
        return ((len(us_norm)+len(us_kings)*5)-(len(computer_norm)+len(computer_kings)*5))
        
    
    def is_complete(self, board, dictBoard):
        '''
            There are two ways to "win"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            1) remove all of the enemies pieces
            2) prevent the enemy from making any moves AND our side controls 
            more of the empty space
        '''
        # No enemies left
        if  len([x for x in board if 'me' in x[0]]) == 0:
            return True
        
        # Enemy has no moves
        if len([self.get_successors(dictBoard, x) for x in board if 'me' in x[0]]) == 0:
            return True
        
        return False
        
    def search(self, board):
        closed = set()
        # Depth first search (so a stacks)
        # We're limiting our depth to n, because of time constraints involved in processing the whole tree.'
        # Create a copy of the list of tuples as a dictionary using dict comprehension.
        # if the board is empty, die a horrible death
        # Do it here so it's only done once, and it can be passed to all the helper methods 
        
        dictBoard = {v[1]: v[0] for v in board}
        
        if not self.is_complete(board, dictBoard):
            pass
        