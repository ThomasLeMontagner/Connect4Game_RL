import math
import numpy as np
import random
from src.minimax import *

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

        for col in range(game.COLUMNS):
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

    def get_move(self, game):
        """Determine the next move for the computer player using a random strategy."""
        column = -1
        while True:
            column = random.randint(0, 6)
            if game.is_column_valid(column):
                break
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

        for col in range(7):
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

    def __init__(self, color, alpha=0.1, epsilon=0.1, discount=0.9):
        self.alpha = alpha  # Learning rate
        self.epsilon = epsilon  # Exploration rate
        self.discount = discount  # Discount factor
        self.q_table = np.zeros((6, 7, 2))  # Q-table for each (state, action) pair
        self.prev_board = None  # Previous game state
        self.prev_player = None  # Previous player color
        self.color = color

    def get_move(self, board, player):
        """This method returns the next move for the QPlayer. It takes in the current game state (board) and the \
        current player's color (player) as arguments. If this is the first move of the game, it returns a random \
        move. Otherwise, it either explores (takes a random action) or exploits (chooses the action with the highest \
        expected reward) based on the exploration rate (epsilon)."""
        # Check if this is the first move
        if self.prev_board is None:
            self.prev_board = board
            self.prev_player = player
            return np.random.randint(0, COLUMNS)  # Return a random move

        # Check if we should explore (take a random action) or exploit (choose the best action)
        if np.random.random() < self.epsilon:
            return np.random.randint(0, COLUMNS)  # Return a random move
        else:
            # Choose the action with the highest expected reward
            q_values = self.q_table[:, :, player]  # Get the Q-values for the current player
            max_q = np.max(q_values)  # Find the maximum Q-value
            best_actions = np.argwhere(q_values == max_q)  # Find all actions with the maximum Q-value
            action = np.random.choice(best_actions)  # Choose one of the best actions at random
            return action

    def update(self, reward, board, player):
        """This method updates the Q-table based on the reward received from the previous move and the current game \
        state. It takes in the reward (reward), the current game state (board), and the current player's color (player)\
        as arguments. It updates the Q-value for the previous state and action pair using the reward received and the\
         maximum Q-value, and updates the previous board and player to the current board and player."""
        # Update the Q-table
        q_values = self.q_table[:, :, self.prev_player]  # Get the Q-values for the previous player
        max_q = np.max(q_values)  # Find the maximum Q-value
        q_values[self.prev_board == self.prev_player] = reward + self.discount * max_q  # Update the Q-value

        # Update the previous state and player
        self.prev_board = board


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
