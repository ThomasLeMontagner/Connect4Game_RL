import math
import numpy as np
import random


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

        def minimax(game, depth, maximizing_player):
            """Recursive function to determine the best move using minimax."""
            if game.check_winner() or depth == 0:
                # return a heuristic score for the current board state
                return self.evaluate_board()
            if maximizing_player:
                best_score = -math.inf
                for column in range(7):
                    try:
                        game.make_move(column, self.color)
                    except ValueError:
                        continue
                    score = minimax(game, depth - 1, False)
                    game.undo_move(column)
                    best_score = max(best_score, score)
                return best_score
            else:
                best_score = math.inf
                for column in range(7):
                    try:
                        if self.color == -1:
                            game.make_move(column, 1)
                        else:
                            game.make_move(column, -1)
                    except ValueError:
                        continue
                    score = minimax(game, depth - 1, True)
                    self.undo_move(column)
                    best_score = min(best_score, score)
                return best_score
        def evaluate_board(self):
            """Evaluate the current board state and return a heuristic score."""
            # define some constants for the heuristic evaluation
            SINGLE_THREAT_SCORE = 10
            DOUBLE_THREAT_SCORE = 100
            TRIPLE_THREAT_SCORE = 1000
            FOUR_IN_A_ROW_SCORE = 10000

            score = 0
            # check for horizontal threats
            for row in range(6):
                for col in range(4):
                    if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.player and self.board[row][col + 3] == ' ':
                        score += SINGLE_THREAT_SCORE
                    if self.board[row][col] == ' ' and self.board[row][col + 1] == self.player and self.board[row][
                        col + 2] == self.player and self.board[row][col + 3] == self.player:
                        score += SINGLE_THREAT_SCORE
                    if self.board[row][col] == self.player and self.board[row][col + 1] == ' ' and self.board[row][
                        col + 2] == self.player and self.board[row][col + 3] == self.player:
                        score += SINGLE_THREAT_SCORE
                    if self.board[row][col] == self.player and self.board[row][col + 1] == self.player and self.board[row][
                        col + 2] == ' ' and self.board[row][col + 3] == self.player:
                        score += SINGLE_THREAT_SCORE
                    if self.board[row][col] == self.player and self.board[row][col + 1] == self.player and self.board[row][
                        col + 2] == self.player and self.board[row][col + 3] == self.player:
                        score += FOUR_IN_A_ROW_SCORE
                # check for vertical threats
                for row in range(3):
                    for col in range(7):
                        if self.board[row][col] == self.player and self.board[row + 1][col] == self.player and \
                                self.board[row + 2][col] == self.player and self.board[row + 3][col] == ' ':
                            score += SINGLE_THREAT_SCORE
                        if self.board[row][col] == ' ' and self.board[row + 1][col] == self.player and self.board[row + 2][
                            col] == self.player and self.board[row + 3][col] == self.player:
                            score += SINGLE_THREAT_SCORE
                        # if self.board[row][col] == self.player and self.board[row+1][col] == ' ' and self.board[row+2][col] == self.player and self.board[row+3][col] == self.player:
                        #    score += SINGLE_THREAT_SCORE
                        ### TO BE CONTINUED...

        best_score = -math.inf
        best_column = None
        for column in range(7):
            try:
                self.make_move(column)
            except ValueError:
                continue
            score = minimax(self.board, 6, False)
            self.undo_move(column)
            if score > best_score:
                best_score = score
                best_column = column
        return best_column


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
        return self.wins / self.visits + c * (2 * np.log(self.parent.visits) / self.visits)**0.5

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

