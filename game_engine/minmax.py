import datetime

from .moves import MoveNode
from world_interface import gamesforthebrain_com

US = 1
COMPUTER = 2
LEFTHANDSIDE = 7
RIGHTHANDSIDE = 0
TOPSIDE = 7
BOTTOMSIDE = 0

class min_max():

    def __init__(self, debug=False):
        '''Start a new game'''
        self.debug = debug
        self.game = gamesforthebrain_com.game_iface()

    def get_state(self):
        '''Get the current state of the game'''
        if self.debug:
            print datetime.datetime.now()
            print self.game.get_state()
        return self.game.get_state()

    def is_complete(self, dict_board):
        '''
            There are two ways to "win"
            1) remove all of the enemies pieces
            2) prevent the enemy from making any moves AND our side controls
            more of the empty space
        '''
        # No enemies left
        if len([x for x in dict(dict_board).items() if 'me' in x[1]]) == 0:
            return True

        # Enemy has no moves
        if self.debug:
            print "Checking if Enemy has any moves"
        if len([self.get_successors(dict_board, x, None, None)
                for x in dict_board.items() if 'me' in x[1]]) == 0:
            return True

        return False

    def get_utility(self, dict_board):
        '''
            Calculate the value of the board using the following 'formula'
            Having Kings is worth more
            Enemy having Kings is worth less to us (ie. more to them)
            Enemy having pieces is worth less to us (more to them)
            Us having pieces is worth more
        '''
        us_kings = []
        computer_kings = []
        us_norm = []
        computer_norm = []
        for position in dict_board.values():
            if 'me1.gif' in position:
                computer_norm.append(position)
            if 'you1.gif' in position:
                us_norm.append(position)
            if "you2k.gif" in position:
                us_kings.append(position)
            if "me2k.gif" in position:
                computer_kings.append(position)
        # TODO list:
        # Control of territory is good
        # Further up the board is good
        KING_BONUS = 5
        return ((len(us_norm) + len(us_kings) * KING_BONUS) -
                (len(computer_norm) + len(computer_kings) * KING_BONUS))

    def get_successors(self, dict_board, position, path, parent):
        '''
            Return all possible successor positions of a given piece
            Inputs
            @dict_board: a copy of the current state of the board
            @position: position on board being checked

            @return list of move objects
        '''
        # Check the position, is it us or them
        # If us, is it a normal piece, or a king
        # If normal King check for positions heading down the board
        # Check heading up the board
        # If enemy occupies successor, check if jump possible
        # if jump possible check successors of that position for other enemies
        possible_moves = []
        for move in self.check_single_moves(position,
                                            dict_board.copy(),
                                            path,
                                            parent
                                            ):
            if move:
                possible_moves.append(move)

        for move in self.check_jumps(position,
                                     dict_board.copy(),
                                     path,
                                     parent
                                     ):
            if move:
                possible_moves.extend(move)
        return possible_moves

    def check_jumps(self, position, dict_board, path, parent):
        '''
            Check if a jump is possible from the given position
            @dict_board: State of current board
            @start_pos: Position of piece
            @path: list of previous moves to here

            @return: int
        '''
        if self.debug:
            print "Start Pos: ", position
        # Jumps require that y +/- 1 and x +/- 1 contain an opposing piece
        # and y +/- 2 and x +/- 2 is possible to land on
        # Kings can go in any direction
        # Computer normals y can only be decreased
        # Player normals y can only be increased
        start_piece = position[1]
        # Board directions
        left = 2
        right = -2
        down = -2
        up = 2
        ###################################################
        # Computer #
        ###################################################
        friend = 'me'
        enemy = 'you'
        friend_king = 'me2k'
        jump_possibles = []
        if friend in start_piece:
            # Computer
            # Forward check: x +/- 2, y - 2 for opposition.
            jump_possibles.append(self.jump_possible(position,
                                                     [
                                                        [left, down],
                                                        [right, down]
                                                     ],
                                                     enemy,
                                                     dict_board,
                                                     path,
                                                     parent))

        if friend_king in start_piece:
            # King so check backwards too.
            jump_possibles.append(self.jump_possible(position,
                                                     [[left, up], [right, up]],
                                                     enemy,
                                                     dict_board,
                                                     path,
                                                     parent))

        ###################################################
        # Us #
        ###################################################

        friend = 'you'
        enemy = 'me'
        friend_king = 'you2k'
        if friend in start_piece:
            # Forward check: x +/- 2, y + 2 for us.
            jump_possibles.append(self.jump_possible(position,
                                                     [
                                                        [left, up],
                                                        [right, up]
                                                     ],
                                                     enemy,
                                                     dict_board,
                                                     path,
                                                     parent))

        if friend_king in start_piece:
            # King so check backwards
            jump_possibles.append(self.jump_possible(position,
                                                     [
                                                        [left, down],
                                                        [right, down]
                                                     ],
                                                     enemy,
                                                     dict_board,
                                                     path,
                                                     parent))

        return jump_possibles

    def jump_possible(self,
                      position,
                      landings,
                      enemy,
                      dict_board,
                      path,
                      parent
                      ):
        '''Calculate the new move'''
        start_x = int(position[0][-2:-1])
        start_y = int(position[0][-1:])
        for landing in landings:
            if start_x + landing[0] <= 7 and start_x + landing[0] >= 0 and \
                    start_y + landing[1] <= 7 and start_y + landing[1] >= 0:
                # if a jump is possible return the new move
                move_to = 'space' + str(start_x + landing[0]) + \
                        str(start_y + landing[1])
                mid_position = 'space' + str(start_x + landing[0] / 2) + \
                    str(start_y + landing[1] / 2)
                new_board = dict_board.copy()
                if (new_board[move_to] == 'gray.gif' and
                        enemy in new_board[mid_position]):
                    # move the piece to the new position
                    new_board[move_to] = new_board[position[0]]
                    # remove the piece from the old position
                    new_board[position[0]] = 'gray.gif'
                    # remove the enemey from the board
                    new_board[mid_position] = 'gray.gif'
                    new_path = path, position[0], move_to
                    jump_list = []
                    jump_list.append(
                            MoveNode(board=new_board,
                                     utility=self.get_utility(new_board),
                                     path=new_path,
                                     parent=parent
                                     )
                                    )
                    # recursive loop, we want to know if it's possible to make
                    # more jumps from the landing point
                    for jump in self.check_jumps(position,
                                                 new_board.copy(),
                                                 path,
                                                 parent
                                                 ):
                        if jump:
                          jump_list.extend(jump)
                    if jump_list:
                      return jump_list

    def check_single_moves(self, position, dict_board, path, parent):
        '''
           Check the right hand side for a possible move.
          
           @return: List of possible moves
        '''
        # convert position to more useful x and y
        x, y = int(position[0][-2:-1]), int(position[0][-1:])
        possible_moves = []
        if x < LEFTHANDSIDE:
            move_to = 'space' + str(x + 1) + str(y + 1)
            if y < TOPSIDE and ('you' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                ''' Only Us or kings can move upwards. '''
                # copy the board and make the move
                new_board = dict_board.copy()
                new_board[move_to] = new_board[position[0]]
                new_board[position[0]] = 'gray.gif'
                new_path = path, position[0], move_to
                possible_moves.append(
                                MoveNode(board=new_board,
                                         parent=parent,
                                         utility=self.get_utility(new_board),
                                         path=new_path
                                         )
                                )

            move_to = 'space' + str(x + 1) + str(y - 1)
            if y > BOTTOMSIDE and ('me' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                ''' Only Computer or king can move downwards. '''
                # copy the board and make the move
                new_board = dict_board.copy()
                new_board[move_to] = new_board[position[0]]
                new_board[position[0]] = 'gray.gif'
                new_path = path, position[0], move_to
                possible_moves.append(
                                MoveNode(board=new_board,
                                         parent=parent,
                                         utility=self.get_utility(new_board),
                                         path=new_path
                                         )
                                )
        if x > RIGHTHANDSIDE:
            move_to = 'space' + str(x - 1) + str(y + 1)
            if y < TOPSIDE and ('you' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                ''' Only Us or kings can move upwards. '''
                # copy the board and make the move
                new_board = dict_board.copy()
                new_board[move_to] = new_board[position[0]]
                new_board[position[0]] = 'gray.gif'
                new_path = path, position[0], move_to
                possible_moves.append(
                                MoveNode(board=new_board,
                                         parent=parent,
                                         utility=self.get_utility(new_board),
                                         path=new_path
                                         )
                                )
            move_to = 'space' + str(x - 1) + str(y - 1)
            if y > BOTTOMSIDE and ('me' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                ''' Only Computer or king can move downwards. '''
                # copy the board and make the move
                new_board = dict_board.copy()
                new_board[move_to] = new_board[position[0]]
                new_board[position[0]] = 'gray.gif'
                new_path = path, position[0], move_to
                possible_moves.append(
                                MoveNode(board=new_board,
                                         parent=parent,
                                         utility=self.get_utility(new_board),
                                         path=new_path
                                         )
                                )
        return possible_moves

    def build_tree(self, dict_board, target=US, parent=None, levels=3):
        '''
            Build the tree that is to be searched.
            @input
            dict_board: Dictionary, current positions of all pieces on the
                        board.
            target: Int, denoting whose move it is.
            parent: MoveNode, that is being appende to.
            levels: Int, number of levels left to calculate.
            @return the root of the tree
        '''
        if parent is None:
            # Root is the current board
            rootnode = MoveNode(board=dict_board.copy(),
                                utility=self.get_utility(dict_board.copy()),
                                parent=None,
                                children=[]
                                )
            # find all the children
            rootnode.children = self.populate_layer(dict_board,
                                                    target=target,
                                                    parent=rootnode
                                                    )

            return self.build_tree(dict_board.copy(),
                                   target=3-target,
                                   parent=rootnode,
                                   levels=levels-1
                                   )

        for child in parent.children:

            for move in child:
                move.children = self.populate_layer(move.board,
                                                    target=target,
                                                    parent=move)
                if levels:
                    self.build_tree(move.board.copy(),
                                    target=3-target,
                                    parent=move,
                                    levels=levels-1
                                    )
        return parent.get_root()

    def populate_layer(self, dict_board, target, parent):
        if target == US:
            target = 'you'
        else:
            target = 'me'
        return [self.get_successors(self.get_state(), x, None, parent)
                for x in dict_board.items() if target in x[1]]

