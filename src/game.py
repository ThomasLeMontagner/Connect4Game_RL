from __future__ import annotations

from copy import deepcopy

import numpy as np
from src.agent import *
from src.constants import *

class ConnectFour:
    def __init__(self, mode: str) -> None:
        self.board: np.ndarray = np.zeros((ROWS, COLUMNS), dtype=int)  # initialize board with empty 0s
        self.previous_state: tuple[tuple[int, ...], ...] | None = None
        self.mode: str = mode

        if mode == '0':  # computer vs computer
            self.player1 = ComputerAgentMinimax(RED)
            self.player2 = ComputerAgentMinimax(YELLOW)
        elif mode == '1':  # computer vs human
            self.player1 = HumanAgent(RED)
            self.player2 = ComputerAgentMinimax(YELLOW)
        else:
            self.player1 = HumanAgent(RED)
            self.player2 = HumanAgent(YELLOW)

        self.current_player: AgentInterface = self.player1  # current player playing

    def is_column_valid(self, column: int) -> bool:
        """Check the validity of the column to make a move."""
        if not column in range(0, COLUMNS):
            # print(f"The column is out of range. It should be between 0 and {COLUMNS - 1}")
            return False
        if self.board[0][column] != 0:
            # print("Invalid move: column is full")
            return False
        else:
            return True

    def make_move(self, column: int, color: int | None = None) -> None:
        """Make a move by dropping a disc into the specified column and the specified color."""
        for row in range(5, -1, -1):  # start from bottom row and work upwards
            if self.board[row][column] == 0:
                if color is None:
                    self.board[row][column] = self.current_player.color
                else:
                    self.board[row][column] = color
                break
        else:
            raise ValueError("Invalid move")

    def undo_move(self, column: int) -> None:
        for row in range(ROWS):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break
        else:
            raise ValueError("Invalid move: column is already empty")

    def switch_player(self) -> None:
        """Switch to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def check_winner(self) -> bool:
        """Check if the current player has won the game."""
        # check for horizontal wins
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == \
                        self.board[row][col + 3] == self.current_player.color:
                    return True
        # check for vertical wins
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == \
                        self.board[row + 3][col] == self.current_player.color:
                    return True
        # check for diagonal wins
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == \
                        self.board[row + 3][col + 3] == self.current_player.color:
                    return True
                if self.board[row][col + 3] == self.board[row + 1][col + 2] == self.board[row + 2][col + 1] == \
                        self.board[row + 3][col] == self.current_player.color:
                    return True
        return False

    def game_over(self) -> bool:
        """Check if the game is over (either because a player has won or the board is full)."""
        return self.check_winner() or all(self.board[0])

    def get_possible_moves(self) -> list[int]:
        """Return list of non-full columns."""
        return [i for i in range(COLUMNS) if self.board[0][i] == 0]

    def get_state(self) -> tuple[tuple[int, ...], ...]:
        """
        Return the 2d list numerical representation of the board
        """
        result = tuple(tuple(x) for x in self.board)

        return result

    def get_prev_state(self) -> tuple[tuple[int, ...], ...] | None:
        """
        Return the previous state of the board
        """
        result = tuple(tuple(x) for x in self.previous_state)

        return result

    def play(self) -> None:
        while not self.game_over():
            self.display_board()
            possible_moves = self.get_possible_moves()
            column = self.current_player.get_move(self, possible_moves)
            print(f"Player {self.current_player} is playing column {column}")

            while not self.is_column_valid(column):
                print('column invalid.')
                column = self.current_player.get_move(self, possible_moves)

            self.previous_state = deepcopy(self.board)
            self.make_move(column, self.current_player.color)

            if self.check_winner():
                self.display_board()
                print(f"Player {self.current_player.color} wins!")
                break
            self.switch_player()
        else:
            self.display_board()
            print("Game over: it's a draw!")

    def display_board(self) -> None:
        """Print the current state of the board to the console."""
        print('\n' + '-' * 13)
        for row in self.board:
            l = [str(i) for i in row]
            print('|'.join(l))
        print('-' * 13)


def main() -> None:
    mode = input("Enter '0' for computer against computer, '1' to play against the computer, '2' to play against "
                 "another player: ")
    if mode == '0' or mode == '1' or mode == '2':
        game = ConnectFour(mode)
        game.play()
    else:
        print('Entry incorrect.')


if __name__ == '__main__':
    main()
