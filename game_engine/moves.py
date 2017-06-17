
class MoveNode():

    def __init__(self,
                 board=None,
                 utility=None,
                 path=None,
                 parent=None,
                 children=[]
                 ):
        self.board = board
        self.utility = utility
        self.path = path
        self.parent = parent
        self.children = children

    def __eq__(self, other=None):
      """ Compare each object's board because the board is what denotes the state"""
      return self.board == other.board
    
    def get_root(self):
        ''' Walk up the tree to find the root node'''
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()
