from __future__ import annotations

from copy import deepcopy
from typing import Sequence

#from agent import *
from game import *


def train_qlearing_agent() -> None:
    qplayer = ComputerAgentQLearning(color=1)  # Initialize the QPlayer object
    opponentPlayer = ComputerAgentRandom(2) # ComputerAgentMinimax(2)

    num_games = 1000  # Number of games to play
    for i in range(num_games):
        game = ConnectFour(mode='0')
        game.player1 = qplayer
        game.player2 = opponentPlayer

        game_over = False

        print(i)
        # Play the game
        while not game_over:
            # Get the player's move
            actions: Sequence[int] = game.get_possible_moves()
            if game.current_player == 1:
                # QPlayer
                move = qplayer.get_move(game, actions)
            else:
                # Other player
                move = opponentPlayer.get_move(game, actions)

            # Make the move
            game.previous_state = deepcopy(game.board)
            game.make_move(move, game.current_player.color)
            # game.display_board()

            # Check if the game is over
            reward = 0
            if all(game.board[0]):
                game_over = True
            elif game.check_winner():
                print(f"Player {game.current_player.color} wins!")
                # if qplayer lost the game
                if game.current_player == 1:
                    reward = 1
                # is qplayer won the game
                else:
                    reward = -2
                game_over = True

            # Update the QPlayer's Q-table
            prev_state = game.get_prev_state()
            prev = qplayer.getQ(prev_state, move)
            result_state = game.get_state()
            maxqnew = max([qplayer.getQ(result_state, a) for a in actions])
            qplayer.q_table[(prev_state, move)] = prev + qplayer.alpha * ((reward + qplayer.gamma*maxqnew) - prev)

            # Switch players
            game.switch_player()

if __name__ == '__main__':
    train_qlearing_agent()
