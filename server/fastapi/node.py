import random
import copy
import functools


class MCTSNode:
    def __init__(self, state, turn, parent_move=None, parent=None):
        self.parent_move = parent_move
        self.state = state
        self.parent = parent
        self.turn = turn
        self.children = []
        self.plays = 0
        self.wins = 0

    @staticmethod
    def check_game_won(state):
        if (
            state[0][0] == state[1][1] == state[2][2] != ""
            or state[0][2] == state[1][1] == state[2][0] != ""
        ):
            return True

        for i in range(3):
            if state[i][0] == state[i][1] == state[i][2] != "":
                return True
            elif state[0][i] == state[1][i] == state[2][i] != "":
                return True

        return False

    @staticmethod
    def get_valid_moves(state):
        valid_moves = []
        for i, row in enumerate(state):
            for j, col in enumerate(row):
                if not col:
                    valid_moves.append((i, j))

        return valid_moves

    def is_terminal(self):
        if self.turn > 8 or self.check_game_won(self.state):
            return True

    def expand(self):
        new_node = self
        if self.check_game_won(self.state) is False:
            for move in self.get_valid_moves(self.state):
                nextstate = copy.deepcopy(self.state)

                nextstate[move[0]][move[1]] = "x" if (self.turn % 2 == 0) else "o"
                child = MCTSNode(nextstate, (self.turn) + 1, move, self)
                if child.is_terminal() is False:
                    new_node = child
                self.children.append(child)
        return new_node

    def simulate_rnd(self):
        game_turn = self.turn
        game_state = copy.deepcopy(self.state)

        while game_turn <= 8 and self.check_game_won(game_state) is False:
            moveset = self.get_valid_moves(game_state)
            rand_move = random.choice(moveset)
            game_state[rand_move[0]][rand_move[1]] = (
                "x" if (game_turn % 2 == 0) else "o"
            )
            game_turn += 1

        if self.check_game_won(game_state):
            if (game_turn - self.turn) % 2 == 0:
                return 1
            else:
                return 0
        else:
            return 0.5

    def backpropagate(self, outcome):
        self.plays += 1
        self.wins += outcome
        if self.parent:
            self.parent.backpropagate(
                -outcome
            )  # negative since two consecutive nodes are opponents of each other

    def visualize_tree(self):  # for debugging nodes
        print("   " * self.turn, end="")
        print(f"Move: {self.parent_move}", end="")
        print(self.state, end="")
        print(f"Wins: {self.wins}, Plays: {self.plays}")

        if self.children:
            for child in self.children:
                child.visualize_tree()
