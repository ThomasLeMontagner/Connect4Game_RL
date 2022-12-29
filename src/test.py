import unittest
from game import *

class TestConnectFour(unittest.TestCase):
    def test_make_move(self):
        game = ConnectFour()
        game.make_move(3)
        self.assertEqual(game.board, [[0, 0, 0, 0, 0, 0, 0] for _ in range(6)])
        self.assertEqual(game.current_player, -1)
        game.make_move(3)
        self.assertEqual(game.board, [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]])
        self.assertEqual(game.current_player, 1)

    def test_check_winner(self):
        game = ConnectFour()
        game.board[5][3] = game.board[4][3] = game.board[3][3] = 1
        self.assertEqual(game.check_winner(), 0)
        game.board[2][3] = 1
        self.assertEqual(game.check_winner(), 1)
        game = ConnectFour()
        game.board[5][3] = game.board[4][3] = game.board[3][3] = -1
        self.assertEqual(game.check_winner(), 0)
        game.board[2][3] = -1
        self.assertEqual(game.check_winner(), -1)
        game = ConnectFour()
        game.board[5][3] = game.board[4][3] = game.board[3][3] = 1
        game.board[5][4] = game.board[4][4] = game.board[3][4] = 1
        self.assertEqual(game.check_winner(), 0)
        game.board[2][4] = 1
        self.assertEqual(game.check_winner(), 1)

if __name__ == "__main__":
    unittest.main()
