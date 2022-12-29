import unittest
import numpy as np
from game import *

class TestConnectFour(unittest.TestCase):
    def test_init_game(self):
        game = ConnectFour(0)
        self.assertEqual(game.player1.color, RED)
        self.assertEqual(game.player2.color, YELLOW)

    def test_make_move(self):
        game = ConnectFour(0)
        board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.assertEqual(game.current_player.color, RED)
        column = 3

        game.make_move(column, color=1)
        board[ROWS-1][column] = 1
        np.testing.assert_array_equal(game.board, board)

        game.make_move(column, color=2)
        board[ROWS-2][column] = 2
        np.testing.assert_array_equal(game.board, board)

    def test_invalid_column_range(self):
        game = ConnectFour(0)
        self.assertTrue(game.is_column_valid(3))
        self.assertTrue(game.is_column_valid(0))
        self.assertTrue(game.is_column_valid(COLUMNS-1))
        self.assertFalse(game.is_column_valid(-1))
        self.assertFalse(game.is_column_valid(COLUMNS))

    def test_invalid_column_full(self):
        game = ConnectFour(0)
        column = 1
        for row in range(ROWS):
            self.assertTrue(game.is_column_valid(column))
            game.make_move(1, column)
        self.assertFalse(game.is_column_valid(column))

    def test_undo_move(self):
        game = ConnectFour(0)
        board = np.zeros((ROWS, COLUMNS), dtype=int)
        column = 1
        game.make_move(column, 1)
        game.undo_move(column)
        np.testing.assert_array_equal(game.board, board)

    def test_check_winner_horizontal(self):
        game = ConnectFour(0)
        self.assertFalse(game.check_winner())
        game.board[0][0] = game.board[0][1] = game.board[0][2] = game.board[0][3] = 1
        self.assertTrue(game.check_winner())

    def test_check_winner_vertical(self):
        game = ConnectFour(0)
        self.assertFalse(game.check_winner())
        game.board[0][0] = game.board[1][0] = game.board[2][0] = game.board[3][0] = 1
        self.assertTrue(game.check_winner())

    def test_check_winner_diagonal(self):
        game = ConnectFour(0)
        self.assertFalse(game.check_winner())
        game.board[0][0] = game.board[1][1] = game.board[2][2] = game.board[3][3] = 1
        self.assertTrue(game.check_winner())

        game = ConnectFour(0)
        self.assertFalse(game.check_winner())
        game.board[3][0] = game.board[2][1] = game.board[1][2] = game.board[0][3] = 1
        self.assertTrue(game.check_winner())

if __name__ == "__main__":
    unittest.main()
