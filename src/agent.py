import math
import numpy as np
import random
from src.minimax import *


class AgentInterface:
    def __init__(self, color):
        self.color = color

    def get_move(self, game, actions):
        """Determine the next move for the computer player"""
        pass


class HumanAgent(AgentInterface):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game, actions):
        """Determine the next ove of the player by asking which column to play."""
        column = int(input(f"Enter column number among {actions}: "))
        return column


class ComputerAgentRandom(AgentInterface):
    """Computer Agent playing randomly."""

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game, actions):
        """Determine the next move for the computer player using a random strategy."""
        column = random.choice(actions)
        return column


class ComputerAgentMinimax(AgentInterface):
    """Computer Agent using minimax method to play."""

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game, actions):
        """Determine the next move for the computer player using the minimax algorithm."""

        maxUtility = -math.inf
        nextMove = -1
        # startTime = time.clock()

        for col in actions:
            # print("MOVE: ", col)
            child = deepcopy(game)
            child.make_move(col, game.current_player.color)
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

    def __init__(self, color, alpha=0.1, epsilon=0.1, gamma=0.9):
        self.alpha = alpha  # Learning rate
        self.epsilon = epsilon  # Exploration rate
        self.gamma = gamma  # Discount factor
        self.q_table = {} # np.zeros((6, 7, 2))  # Q-table for each (state, action) pair
        # self.prev_board = None  # Previous game state
        # self.prev_player = None  # Previous player color
        self.color = color

    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q_table.get((state, action)) is None:
            self.q_table[(state, action)] = 1.0
        return self.q_table.get((state, action))

    def get_move(self, game, actions):
        """
        This method returns the next move for the QPlayer. It takes in the current game state (board) and the \
        current player's color (player) as arguments. If this is the first move of the game, it returns a random \
        move. Otherwise, it either explores (takes a random action) or exploits (chooses the action with the highest \
        expected reward) based on the exploration rate (epsilon).
        """
        current_state = game.get_state()

        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]


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
