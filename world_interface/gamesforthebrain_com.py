'''
This is the connector between the AI agent and the
gamesforthebrain.com/game/checkers website.
This file provides an interface for the agent to be able to interact with the
game such that the agent can get the current state of the game, nominate the
piece to move and nominate where to move it.
'''

from splinter.browser import Browser
import time

SLEEPTIME = 2


class game_iface():

    def __init__(self, game_address='http://www.gamesforthebrain.com/game/checkers/'):
        ''' Each instance of the application has its own browser. '''
        self.browser = Browser()
        self.browser.visit(game_address)

    def get_state(self):
        '''
            Get the state of the board we are playing on.
            @return: a dictionary.
                Each key is a square on the board.
        '''
        board_html = self.browser.find_by_.id('board').html.replace('\n', '')
        board = [x.split('"')[1:4] for x in str(board_html).split("><")]
        '''
            Explanation of HTML:
            owner, space name
            Black cannot be used
            Gray empty
            Me1 Computer
            Me King
            You1 Player
            You king
            y[0]: owner
            y[2]: board position
        '''
        return self.to_dict([(y[0], y[2]) for y in board if len(y) == 3])

    def to_dict(self, game):
        ''' Return a dictionary representation of the game. '''
        return {x[1]: x[0] for x in game}

    def move_piece(self, start_pos, end_pos):
        '''
            Move a piece from one position to another.

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
            # One of the elements doesn't exist and the move failed.
            return False

        # Move succeeded.
        return True

    def double_jump(self, start_pos, interim_pos, end_pos):
        '''
            Jumping over two pieces.
            
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
            time.sleep(SLEEPTIME)
            element = self.browser.find_by_name(end_pos)
            element.click()
        except AttributeError:
            # One of the elements doesn't exist and the move failed.
            return False

        # Move succeeded.
        return True
