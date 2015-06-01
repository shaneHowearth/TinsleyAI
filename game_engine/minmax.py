from world_interface import gamesforthebrain_com

class min_max():
    
    def __init__(self):
        self.game = gamesforthebrain_com.game_iface()
        
    def get_start_state(self):
        
        return self.game.get_state()
        
    def get_successors(self, board, position):   
        '''
            Return all possible successor positions of a given piece
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
        for x_pos in x_possibles:
            for y_pos in y_possibles:
                positions.append('space'+str(x_pos)+str(y_pos))
                
        if 'me' in position[0]:
            # computer
            # If any enemy, check if jumping is possible
            # If jump possible, check for double jump
            pass
        else:
            # Us
            pass
        
        # Kings
        
            
    def get_utility(self, board):
        # Having Kings is worth more
        # Losing pieces is bad
        # Jumping pieces is good
        # Control of territory is good
        # Further up the board is good
        pass 
    
    def is_complete(self, board, dictBoard):
        '''
            There are two ways to "win"
            1) remove all of the enemies pieces
            2) prevent the enemy from making any moves AND our side controls 
            more of the empty space
        '''
        if  len([x for x in board if 'me' in x[0]]) == 0:
            return True
        
        if len([self.get_successors(dictBoard, x) for x in board if 'me' in x[0]]) == 0:
            return True
        
        return False
        
    def search(self, board):
        # Depth first search (so a stacks)
        # We're limiting our depth to n, because of time constraints involved in processing the whole tree.'
        dictBoard = {v[1]: v[0] for v in board}
        if not self.is_complete(board, dictBoard):
            pass