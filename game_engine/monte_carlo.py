class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and, optionally, some keyword arguments.
        # Initialises the list of game states, and the statistics tables.
        self.board = board
        self.states = []

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    def get_play(self):
        # Causes the AI t calculate the best move from the current game state
        # and return it.
        pass

    def run_simulation(self):
        # Plays out a 'random' game from the current position, then updates the
        # statistics tables with the result.
        pass
