import math
import random
from agent import *

# Constants for the game board
ROWS = 6
COLUMNS = 7

# Constants for the players
RED = 1
YELLOW = 2

class ConnectFour:
    def __init__(self, mode):
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)  # initialize board with empty 0s

        if mode == '0':  # computer vs computer
            self.player1 = ComputerAgentRandom(RED)
            self.player2 = ComputerAgentRandom(YELLOW)
        elif mode == '1':  # computer vs human
            self.player1 = HumanAgent(RED)
            self.player2 = ComputerAgentRandom(YELLOW)
        else:
            self.player1 = HumanAgent(RED)
            self.player2 = HumanAgent(YELLOW)

        self.player = self.player1  # current player playing

    def is_column_valid(self, column):
        """Check the validity of the column to make a move."""
        if not column in range(0, COLUMNS):
            return False
        if self.board[0][column] != 0:
            return False
        else:
            return True

    def make_move(self, column, color):
        """Make a move by dropping a disc into the specified column."""
        for row in range(5, -1, -1):  # start from bottom row and work upwards
            if self.board[row][column] == 0:
                self.board[row][column] = color
                break
        else:
            raise ValueError("Invalid move: column is full")

    def undo_move(self, column):
        for row in range(ROWS):
            if self.board[row][column] != 0:
                self.board[row][column] == 0
                break
        else:
            raise ValueError("Invalid move: column is already empty")

    def switch_player(self):
        """Switch to the other player."""
        if self.player == self.player1:
            self.player = self.player2
        else:
            self.player = self.player1

    def check_winner(self):
        """Check if the current player has won the game."""
        # check for horizontal wins
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == \
                        self.board[row][col + 3] == self.player.color:
                    return True
        # check for vertical wins
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == \
                        self.board[row + 3][col] == self.player.color:
                    return True
        # check for diagonal wins
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == \
                        self.board[row + 3][col + 3] == self.player.color:
                    return True
                if self.board[row][col + 3] == self.board[row + 1][col + 2] == self.board[row + 2][col + 1] == \
                        self.board[row + 3][col] == self.player.color:
                    return True
        return False

    def game_over(self):
        """Check if the game is over (either because a player has won or the board is full)."""
        return self.check_winner() or all(self.board[0])

    def play(self):
        while not self.game_over():
            self.display_board()
            column = self.player.get_move(self.board)
            print(f"Player is playing column {column}")
            while not self.is_column_valid(column):
                print('column invalid.')
                column = self.player.get_move(self.board)
            self.make_move(column, self.player.color)
            if self.check_winner():
                self.display_board()
                print(f"Player {self.player.color} wins!")
                break
            self.switch_player()
        else:
            self.display_board()
            print("Game over: it's a draw!")

    def display_board(self):
        """Print the current state of the board to the console."""
        print('\n' + '-' * 13)
        for row in self.board:
            l = [str(i) for i in row]
            print('|'.join(l))
        print('-' * 13)


def main():
    print(a == b == b)
    mode = input("Enter '0' for computer against computer, '1' to play against the computer, '2' to play against "
                 "another player: ")
    if mode == '0' or mode == '1' or mode == '2':
        game = ConnectFour(mode)
        game.play()
    else:
        print('Entry incorrect.')


if __name__ == '__main__':
    main()
