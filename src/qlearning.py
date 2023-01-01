#from agent import *
from game import *


def train_qlearing_agent():
    qplayer = ComputerAgentQLearning(color=1)  # Initialize the QPlayer object
    opponentPlayer = ComputerAgentRandom(2) # ComputerAgentMinimax(2)

    num_games = 1000  # Number of games to play
    for i in range(num_games):
        game = ConnectFour(mode='0')
        game.player1 = qplayer
        game.player2 = opponentPlayer
        qplayer.prev_board = None  # Reset the QPlayer's previous board and player
        qplayer.prev_player = None

        game_over = False

        print(i)
        # Play the game
        while not game_over:
            # Get the player's move
            if game.current_player == 1:
                # QPlayer
                move = qplayer.get_move(game.board, game.current_player)
            else:
                # Other player
                move = opponentPlayer.get_move(game)

            # Make the move
            game.make_move(move, game.current_player.color)
            # game.display_board()

            # Check if the game is over
            reward = 0
            if all(game.board[0]):
                reward = 0
            elif game.check_winner():
                print(f"Player {game.current_player.color} wins!")
                # if qplayer lost the game
                if game.current_player == 1:
                    reward += 1
                # is qplayer won the game
                else:
                    reward -= 1
                game_over = True

            # Update the QPlayer's Q-table
            qplayer.update(reward, game.board, game.current_player)

            # Switch players
            game.switch_player()

if __name__ == '__main__':
    train_qlearing_agent()
