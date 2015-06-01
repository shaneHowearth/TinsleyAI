'''
This is the connector between our AI agent and the gamesforthebrain.com/game/checkers
website. This file provides an interface for the agent to be able to interact with the game
such that the agent can get the current state of the game, and nominate the piece to move
and move that piece.
'''

from splinter.browser import Browser
import time 

class game_iface():
    
    def __init__(self):
        # we could have multiple games running, so we want each instance to have 
        # its own browser. 
        self.browser = Browser()
        self.browser.visit('http://www.gamesforthebrain.com/game/checkers/')
        
    
    # Get State
    def get_state(self):
        '''
            Get the state of the board we are playing on.
            Returns a list of tuples
        '''
        board = self.browser.find_by_id('board').html.replace('\n', '')
        # yay soup \o/ :(
        # split everything on ><
        raw_soup = [x.split('"')[1:4] for x in str(board).split("><")]
        # owner, space name
        # Black cannot be used
        # Gray empty
        # Me1 Computer
        # Me King
        # You1 Player
        # You king
        return [(y[0],y[2]) for y in raw_soup  if len(y)==3]
     
    # Move piece
    def move_piece(self, start_pos, end_pos):
        '''
            @start_pos: string
                name of the position of the piece to be moved
                
            @end_pos: string
                name of the position where the move ends

            @return: boolean 
                If the move succeeded or failed
        '''
        try:
            element = self.browser.find_by_name(start_pos)
            element.click()
            
            element = self.browser.find_by_name(end_pos)
            element.click()
            
        except AttributeError:
            # One of the elements doesn't exist and the move failed
            return False
        
        # Move succeeded
        return True
    
    def double_jump(self, start_pos, interim_pos, end_pos):
        '''
            @start_pos: string
                name of the position of the piece to be moved
                
            @interim_pos: string
                name of the position that finishes the first jump
            
            @end_pos: string
                name of the position where the move ends

            @return: boolean 
                If the move succeeded or failed
        '''
        try:
            self.move_piece(start_pos, interim_pos)
            time.sleep(2)
            element = self.browser.find_by_name(end_pos)
            element.click()
            
        except AttributeError:
            # One of the elements doesn't exist and the move failed
            return False
        
        # Move succeeded
        return True
        