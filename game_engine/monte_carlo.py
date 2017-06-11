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
        self.wins = {}
        self.plys = {}

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
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for __ in range(self.max_moves):
            legal = self.board.legal_plays(states_copy)

            play = choice(legal)
            state = self.board.next_state(state, play)
            states_copy.append(state)

            # `player` here refers to the player who moved into that state.
            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break
            
            for player, state in visited_states:
                if (player, state) not in self.plays:
                    continue
                self.plays[(player, state)] += 1
                if player == winner:
                    self.wins[(player, state)] += 1
