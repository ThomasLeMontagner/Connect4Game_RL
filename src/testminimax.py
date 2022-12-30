import unittest
from minimax import *
from game import *


class TestMinimax(unittest.TestCase):
    def test_count_horizontal_score(self):
        game = ConnectFour(0)
        for col in range(1, 3):
            game.board[0][col] = 1
        self.assertEqual(count_horizontal_score(game, 1), 2 * TWO_IN_A_ROW_SCORE)

        game = ConnectFour(0)
        for col in range(4):
            game.board[0][col] = 1
        self.assertEqual(count_horizontal_score(game, 1), FOUR_IN_A_ROW_SCORE + THREE_IN_A_ROW_SCORE + \
                         TWO_IN_A_ROW_SCORE)

    def test_count_vertical_score(self):
        game = ConnectFour(0)
        for row in range(1, 3):
            game.board[row][0] = 1
        self.assertEqual(2 * TWO_IN_A_ROW_SCORE, count_vertical_score(game, 1))

        game = ConnectFour(0)
        for row in range(4):
            game.board[row][0] = 1
        self.assertEqual(FOUR_IN_A_ROW_SCORE + THREE_IN_A_ROW_SCORE + TWO_IN_A_ROW_SCORE, count_vertical_score(game, 1))

    def test_count_diagonal_score(self):
        game = ConnectFour(0)
        game.board[2][0] = 1
        game.board[3][1] = 1
        self.assertEqual(TWO_IN_A_ROW_SCORE, count_diagonal_score(game, 1))

        game = ConnectFour(0)
        game.board[0][3] = 1
        game.board[1][4] = 1
        self.assertEqual(TWO_IN_A_ROW_SCORE, count_diagonal_score(game, 1))

        game = ConnectFour(0)
        game.board[3][0] = 1
        game.board[2][1] = 1
        self.assertEqual(TWO_IN_A_ROW_SCORE, count_diagonal_score(game, 1))

        game = ConnectFour(0)
        game.board[ROWS - 1][3] = 1
        game.board[ROWS - 2][4] = 1
        self.assertEqual(TWO_IN_A_ROW_SCORE, count_diagonal_score(game, 1))


if __name__ == '__main__':
    unittest.main()
