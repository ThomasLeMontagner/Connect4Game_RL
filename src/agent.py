"""Agent implementations for Connect Four opponents and search helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import math
import numpy as np
import random
from src.minimax import *

if TYPE_CHECKING:
    from src.game import ConnectFour

BoardState = tuple[tuple[int, ...], ...]
QTable = dict[tuple[BoardState, int], float]


class AgentInterface:
    """Base interface for Connect Four agents."""

    def __init__(self, color: int) -> None:
        """Initialize agent with assigned color."""
        self.color = color

    def get_move(self, game: ConnectFour, actions: Sequence[int]) -> int:
        """Determine the next move for the computer player."""
        raise NotImplementedError


class HumanAgent(AgentInterface):
    """Human player interacting via console input."""

    def __init__(self, color: int) -> None:
        """Initialize human agent color."""
        super().__init__(color)

    def get_move(self, game: ConnectFour, actions: Sequence[int]) -> int:
        """Prompt for a move by asking which column to play."""
        column = int(input(f"Enter column number among {actions}: "))
        return column


class ComputerAgentRandom(AgentInterface):
    """Computer Agent playing randomly."""

    def __init__(self, color: int) -> None:
        """Initialize random agent color."""
        super().__init__(color)

    def get_move(self, game: ConnectFour, actions: Sequence[int]) -> int:
        """Determine the next move for the computer player using a random strategy."""
        column = random.choice(actions)
        return column


class ComputerAgentMinimax(AgentInterface):
    """Computer Agent using minimax method to play."""

    def __init__(self, color: int) -> None:
        """Initialize minimax agent color."""
        super().__init__(color)

    def get_move(self, game: ConnectFour, actions: Sequence[int]) -> int:
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
    """Computer agent using Q-learning to play."""

    def __init__(self, color: int, alpha: float = 0.1, epsilon: float = 0.1, gamma: float = 0.9) -> None:
        """Initialize learning rates, exploration settings, and Q-table."""
        self.alpha = alpha  # Learning rate
        self.epsilon = epsilon  # Exploration rate
        self.gamma = gamma  # Discount factor
        self.q_table: QTable = {}  # Q-table for each (state, action) pair
        # self.prev_board = None  # Previous game state
        # self.prev_player = None  # Previous player color
        self.color = color

    def getQ(self, state: BoardState, action: int) -> float:
        """Return the Q-value for a state-action pair, initializing optimistically."""
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q_table.get((state, action)) is None:
            self.q_table[(state, action)] = 1.0
        return self.q_table.get((state, action))

    def get_move(self, game: ConnectFour, actions: Sequence[int]) -> int:
        """Choose the next move using an epsilon-greedy Q-learning policy."""
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
    """Node for Monte Carlo Tree Search exploration."""

    def __init__(self, parent: Node | None = None, action: int | None = None,
                 state: np.ndarray | BoardState | None = None) -> None:
        """Initialize node linkage, action, state, and statistics."""
        self.parent = parent
        self.children: list[Node] = []
        self.action = action
        self.state = state
        self.visits = 0
        self.wins = 0

    def add_child(self, action: int, state: np.ndarray | BoardState) -> Node:
        """Create and attach a child node for a given action and state."""
        child = Node(self, action, state)
        self.children.append(child)
        return child

    def update(self, result: float) -> None:
        """Update visit and win counts after a simulation."""
        self.visits += 1
        self.wins += result

    def ucb(self, c: float = 1.4142) -> float:
        """Compute the UCB score for this node."""
        if self.parent is None:
            return float('inf')
        return self.wins / self.visits + c * (2 * np.log(self.parent.visits) / self.visits) ** 0.5


def monte_carlo_tree_search(game: ConnectFour, iterations: int) -> int:
    """Run MCTS for a number of iterations and return the chosen column."""
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

    def __init__(self, iterations: int = 1000) -> None:
        """Initialize MCTS agent with iteration budget."""
        self.iterations = iterations

    def choose_move(self, game: ConnectFour) -> int:
        """Select a move using Monte Carlo Tree Search."""
        return monte_carlo_tree_search(game, self.iterations)
