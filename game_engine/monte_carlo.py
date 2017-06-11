import datetime
from random import choice


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and, optionally, some keyword arguments.
        # Initialises the list of game states, and the statistics tables.
        self.board = board
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    def get_play(self):
        # Causes the AI t calculate the best move from the current game state
        # and return it.
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()

    def run_simulation(self):
        # Plays out a 'random' game from the current position, then updates the
        # statistics tables with the result.
        states_copy = self.states[:]
        state = states_copy[-1]

        for __ in range(self.max_moves):
            legal = self.board.legal_plays(states_copy)

            play = choice(legal)
            state = self.board.next_state(state, play)
            states_copy.append(state)

            winner = self.board.winner(states_copy)
            if winner:
                break
