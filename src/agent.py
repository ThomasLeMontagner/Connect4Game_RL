import math
import numpy as np
import random
from minimax import *
from game import *


class AgentInterface:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        """Determine the next move for the computer player"""
        pass


class HumanAgent(AgentInterface):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        """Determine the next ove of the player by asking which column to play."""
        column = int(input("Enter column number (0-6): "))
        return column


class ComputerAgentRandom(AgentInterface):
    """Computer Agent playing randomly."""

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        """Determine the next move for the computer player using a random strategy."""
        column = random.randint(0, 6)
        return column


class ComputerAgentMinimax(AgentInterface):
    """Computer Agent using minimax method to play."""

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game):
        """Determine the next move for the computer player using the minimax algorithm."""

        maxUtility = -math.inf
        nextMove = -1
        # startTime = time.clock()

        for col in range(COLUMNS):
            if game.is_column_valid(col):
                # print("MOVE: ", col)
                child = deepcopy(game)
                child.make_move(col, game.current_player.color)
            else:
                continue

            utility = decision(child)
            # print("utility: ", utility)
            if utility >= maxUtility:
                maxUtility = utility
                nextMove = col
        # endTime = time.clock()
        # print("Time: ", endTime - startTime)
        return nextMove


class ComputerAgentQLearning(AgentInterface):
    """Computer Agent using Q-Learning method to play;"""

    def __init__(self, alpha=0.1, discount_factor=0.9):
        self.alpha = alpha
        self.discount_factor = discount_factor
        self.board = np.zeros((6, 7), dtype=np.int)
        self.q_values = {}
        self.player = 1

    def reset_board(self):
        self.board = np.zeros((6, 7), dtype=int)

    def get_state(self):
        return self.board.tostring()

    def get_valid_actions(self):
        valid_actions = []
        for col in range(7):
            if self.board[0][col] == 0:
                valid_actions.append(col)
        return valid_actions

    def get_q_value(self, state, action):
        if (state, action) not in self.q_values:
            self.q_values[(state, action)] = 0.0
        return self.q_values[(state, action)]

    def get_best_action(self, state):
        best_action = None
        max_q_value = -float('inf')
        for action in self.get_valid_actions():
            q_value = self.get_q_value(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action
        return best_action


class Node:
    def __init__(self, parent=None, action=None, state=None):
        self.parent = parent
        self.children = []
        self.action = action
        self.state = state
        self.visits = 0
        self.wins = 0

    def add_child(self, action, state):
        child = Node(self, action, state)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def ucb(self, c=1.4142):
        if self.parent is None:
            return float('inf')
        return self.wins / self.visits + c * (2 * np.log(self.parent.visits) / self.visits) ** 0.5


def monte_carlo_tree_search(game, iterations):
    root = Node(state=game.board)
    for _ in range(iterations):
        node = root
        game_copy = game.copy()
        while node.children:
            node = max(node.children, key=lambda x: x.ucb())
            game_copy.make_move(node.action)
            winner = game_copy.check_winner()
            if winner:
                break
        if not node.children:
            for action in game_copy.get_valid_actions():
                child_state = game_copy.get_state(action)
                node.add_child(action, child_state)
        node = node.children[-1]
        game_copy.make_move(node.action)
        winner = game_copy.check_winner()
        while node is not None:
            node.update(winner)
            node = node.parent
    return max(root.children, key=lambda x: x.visits).action


class ComputerAgentMCTS(AgentInterface):
    """Computer Agent using Monte-Carlo Tree Search to play."""

    def __init__(self, iterations=1000):
        self.iterations = iterations

    def choose_move(self, game):
        return monte_carlo_tree_search(game, self.iterations)
