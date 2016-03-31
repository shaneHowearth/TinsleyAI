from world_interface import gamesforthebrain_com
import sys
import time
import datetime
from moves import MoveNode


class min_max():

    def __init__(self, debug=False):
        self.debug = debug
        self.game = gamesforthebrain_com.game_iface()

    def get_start_state(self):
        print datetime.datetime.now()
        if self.debug:
            print self.game.get_state()
        return self.game.get_state()

    def get_successors(self, dict_board, position):
        '''
            Return all possible successor positions of a given piece
            List of Tuples; The tuples contain the move, and the utility of
            the board for that move

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
        x, y = int(position[0][-2:-1]), int(position[0][-1:])
        start_space = position[0]
        # Check there's room to the right to move
        adjustor = 1
        if 'me' in position[1]:
            adjustor = -1

        # Origin of the board is bottom right hand corner
        if x < 7:
            move_to = 'space'+str(x+1)+str(y+1)
            if y < 7 and ('you' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                # 0
                possible_moves.append((1*adjustor, start_space, move_to))

            move_to = 'space'+str(x+1)+str(y-1)
            if y > 0 and ('me' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                # 1
                possible_moves.append((1*adjustor, start_space, move_to))
        # Check there's room to the left to move
        if x > 0:
            move_to = 'space'+str(x-1)+str(y+1)
            if y < 7 and ('you' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                # 2
                possible_moves.append((1*adjustor, start_space, move_to))

            move_to = 'space'+str(x-1)+str(y-1)
            if y > 0 and ('me' in position[1] or 'k' in position[1]) \
                    and 'gray.gif' in dict_board[move_to]:
                # 3
                possible_moves.append((1*adjustor, start_space, move_to))

        # All possible jumps
        # Need to fix a MASSIVE bug here.
        # Do we need a separate jump_possible for each path?
        # If so, how do we represent that
        jump_possibles = self.check_jump(dict_board,
                                         position,
                                         [0, start_space])
        for jump_possible in jump_possibles:
            possible_moves.append(tuple(jump_possible))
        if self.debug:
            print possible_moves
        return possible_moves

    def check_jump(self, dict_board, start_pos, prev_moves):
        '''
            Check if a jump is possible from the given position
            @dict_board: State of current board
            @start_pos: Position of piece
            @prev_moves: list of previous moves to hear

            @return: int
        '''
        if self.debug:
            print "Start Pos: ", start_pos
        # Jumps require that y +/- 1 and x +/- 1 contain an opposing piece
        # and y +/- 2 and x +/- 2 is possible to land on
        # Kings can go in any direction
        # Computer normals y can only be decreased
        # Player normals y can only be increased
        start_piece = start_pos[1]
        start_pos_x = int(start_pos[0][-2:-1])
        start_pos_y = int(start_pos[0][-1:])
        ###################################################
        # Computer #
        ###################################################
        friend = 'me'
        enemy = 'you'
        friend_king = 'me2k'
        enemy_king = 'you2k'
        adjust = -1
        jump_possibles = []
        if friend in start_piece:
            # Computer
            # Forward check: x +/- 1, y - 1 for opposition
            if start_pos_x < 6 and start_pos_y > 1:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [1, 2],
                                                         [-1, -2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

            if start_pos_x > 1 and start_pos_y > 1:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [-1, -2],
                                                         [-1, -2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

        if friend_king in start_piece:
            # King so check backwards
            if start_pos_x < 6 and start_pos_y < 6:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [1, 2],
                                                         [1, 2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

            if start_pos_x > 1 and start_pos_y < 6:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [-1, -2],
                                                         [1, 2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

        ###################################################
        # Us #
        ###################################################

        friend = 'you'
        enemy = 'me'
        friend_king = 'you2k'
        enemy_king = 'me2k'
        adjust = 1
        if friend in start_pos[1]:
            # Forward check: x +/- 1, y + 1 for us
            if start_pos_x < 6 and start_pos_y < 6:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [1, 2],
                                                         [1, 2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

            if start_pos_x > 1 and start_pos_y < 6:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [-1, -2],
                                                         [1, 2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

        if friend_king in start_piece:
            # King so check backwards
            if start_pos_x < 6 and start_pos_y > 1:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [1, 2],
                                                         [-1, -2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

            if start_pos_x > 1 and start_pos_y > 1:
                jump_possibles.append(self.jump_possible(start_pos,
                                                         start_pos_x,
                                                         start_pos_y,
                                                         [-1, -2],
                                                         [-1, -2],
                                                         enemy,
                                                         enemy_king,
                                                         adjust,
                                                         dict_board,
                                                         prev_moves))

        return jump_possibles

    def jump_possible(self, start_pos, start_pos_x, start_pos_y, x_adjust,
                      y_adjust, enemy, enemy_king, adjust, dict_board,
                      prev_moves):
        gain = 0

        start_position = start_pos[0]
        check_pos = 'space' + str(start_pos_x + x_adjust[0]) + \
                    str(start_pos_y + y_adjust[0])
        if enemy in dict_board[check_pos]:
            if enemy_king in dict_board[check_pos]:
                gain += 8
            else:
                gain += 3
            end_pos = 'space' + str(start_pos_x + x_adjust[1]) + \
                      str(start_pos_y + y_adjust[1])
            if "gray.gif" in dict_board[end_pos]:
                copied_board = dict_board.copy()
                copied_board[start_pos] = 'gray.gif'
                copied_board[check_pos] = 'gray.gif'
                copied_board[end_pos] = dict_board[start_position]
                prev_moves[0] += gain * adjust
                prev_moves.append(end_pos)
                if self.debug:
                    print "Computer check jump", end_pos
                return self.check_jump(copied_board, end_pos, prev_moves)

    def get_utility(self, dict_board):
        # Having Kings is worth more
        # Enemy having Kings is worth less to us (ie. more to them)
        # Enemy having pieces is worth less to us (more to them)
        # Us having pieces is worth more
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
        return ((len(us_norm)+len(us_kings)*5) -
                (len(computer_norm)+len(computer_kings)*5))

    def is_complete(self, dict_board):
        '''
            There are two ways to "win"
            1) remove all of the enemies pieces
            2) prevent the enemy from making any moves AND our side controls
            more of the empty space
        '''
        # No enemies left
        if len([x for x in dict_board.items() if 'me' in x[1]]) == 0:
            return True

        # Enemy has no moves
        if self.debug:
            print "Checking if Enemy has any moves"
        if len([self.get_successors(dict_board, x)
                for x in dict_board.items() if 'me' in x[1]]) == 0:
            return True
        return False

    def get_max(self, dict_board, depth):
        if self.is_complete(dict_board) or depth >= 10:
            return (None, self.get_utility(dict_board))

        highest_score = -sys.maxint - 1
        best_move = (-sys.maxint-1, None)
        if self.debug:
            print "Get Max"
        for move_list in [self.get_successors(dict_board, x)
                          for x in dict_board.items() if 'you' in x[1]]:
            if move_list[0]:
                for move in move_list:
                    # clone the dict_board
                    copied_board = dict_board.copy()
                    # simulate the move
                    copied_board[move[-1:]] = copied_board[move[1]][0]
                    for space in move[1:-1]:
                        copied_board[space] = 'gray.gif'
                    depth += 1
                    score = self.get_min(copied_board, depth)[0]
                    if score > highest_score:
                        highest_score = score
                        # print "Highest Score: ", highest_score
                        best_move = move
        return best_move

    def get_min(self, dict_board, depth):
        if self.is_complete(dict_board) or depth >= 10:
            return (None, self.get_utility(dict_board))

        lowest_score = sys.maxint
        worst_move = (sys.maxint, None)
        if self.debug:
            print "Get Min"
        for move_list in [self.get_successors(dict_board, x)
                          for x in dict_board.items() if 'me' in x[1]]:
            if move_list[0]:
                for move in move_list:
                    # clone the dict_board
                    copied_board = dict_board.copy()
                    # simulate the move
                    copied_board[move[-1:]] = copied_board[move[1]][0]
                    for space in move[1:-1]:
                        copied_board[space] = 'gray.gif'
                    depth += 1
                    score = self.get_max(copied_board, depth)[0]
                    if score is not None and score < lowest_score:
                        lowest_score = score
                        # print "Lowest Score: ", lowest_score
                        worst_move = move
        return worst_move

    def search(self, board):
        # Just a dirty hack, ignore me. Need it in the git repo though
        # sys.setrecursionlimit(1500)
        # Depth first search (so a stacks)
        # in processing the whole tree.'
        # We're limiting our depth to n, because of time constraints involved
        # Create a copy of the list of tuples as a dictionary using dict
        # comprehension. if the board is empty, die a horrible death
        # Do it here so it's only done once, and it can be passed to all the
        # helper methods
        # Turn the board into a dictionary
        dict_board = {v[1]: v[0] for v in board}

        if not self.is_complete(dict_board):
            highest_score = -sys.maxint - 1
            best_move = None
            if self.debug:
                print "Search", dict_board
            for move_list in [self.get_successors(dict_board, us_item)
                              for us_item in dict_board.items()
                              if 'you' in us_item[1]]:
                if move_list[0]:
                    for move in move_list:
                        score = self.get_min(dict_board.copy(), 0)[0]
                        if score > highest_score:
                            highest_score = score
                            best_move = move
            print best_move[1], best_move[-1:][0]
            self.game.move_piece(best_move[1], best_move[-1:][0])
            time.sleep(5)
            if self.debug:
                print "Recursive search call"
            self.search(self.get_start_state())
            return best_move
