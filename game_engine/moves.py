
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

    def get_root(self):
        ''' Walk up the tree to find the root node'''
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()
