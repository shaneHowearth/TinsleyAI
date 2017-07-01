"""
This is the agent. This is the code that looks at the tree and searches for the optimum move.
"""
import time

from .minmax import min_max, US
from world_interface import gamesforthebrain_com


MAX_DEEP = 4

class agent():

    def solve(self, board):
        """"""
        # build a tree
        game = min_max(debug=False, game=gamesforthebrain_com.game_iface())
        while min_max.is_complete(game.get_state()):
            move = self._find_move(game)
            if move:
                game.move_piece(move)
                time.sleep(5)
            else:
                print "No moves"
                break
        
    def _find_move(self, board)        
        tree = board.build_tree(a.get_state(), target=US, parent=None, levels=MAX_DEEP)
        return self.search(tree)

    def search(self, tree):
        move = None
        return move

