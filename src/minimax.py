import time
from copy import deepcopy
from game import *
import math

max_depth = 5 # maximum authorized depth
max_time = 0.05 # maximum computation time


def minimize(game, current_depth, alpha, beta):
    #print(" -- minimize --")
    if game.check_winner() or current_depth == 0:
        # return a heuristic score for the current board state
        return evaluate_board(game)

    minUtility = math.inf

    for child in get_next_games(game):
        utility = maximize(child, current_depth +1, alpha, beta)

        if utility < minUtility:
            minUtility = utility

        if minUtility <= alpha:
            break

        if minUtility < beta:
            beta = minUtility

    # print("Minimize utility: ", minUtility)
    return minUtility


def maximize(game, current_depth, alpha, beta):
    #print(" -- maximize --")
    if game.check_winner() or current_depth == 0:
        # return a heuristic score for the current board state
        return evaluate_board(game)

    maxUtility = -math.inf

    for col in range(COLUMNS):
        child_game = deepcopy(game)
        child_game.make_move(col)
        child_game.switch_player()

        # print("MOVE: ", move)
        utility = minimize(child_game, current_depth + 1, alpha, beta)

        if utility > maxUtility:
            maxUtility = utility

        if maxUtility >= beta:
            break

        if maxUtility > alpha:
            alpha = maxUtility

    # print("Maximize utility: ", maxUtility)
    return maxUtility


def decision(game):
    # start = time.clock()
    return minimize(game, 0, -math.inf, math.inf)


def evaluate_board(game):
    """Evaluate the current board state and return a heuristic score."""
    # define some constants for the heuristic evaluation
    SINGLE_THREAT_SCORE = 10
    TWO_IN_A_ROW_SCORE = 100
    THREE_IN_A_ROW_SCORE = 1000
    FOUR_IN_A_ROW_SCORE = 10000

    score = 0
    player_color = game.current_player.color
    adverse_color = RED
    if player_color == RED:
        adverse_color = YELLOW

    # check for horizontal opportunities: for every subsection of 4 places, check is there are 2 or 3 same,
    # with empy spaces in-between
    for row in range(ROWS):
        r = game.board[row, :]
        for col in range(COLUMNS - 4 + 1):
            sub = r[col:col+4]
            if np.count_nonzero(sub == player_color) == 2 and np.count_nonzero(sub == 0) == 2:
                score += TWO_IN_A_ROW_SCORE
            if np.count_nonzero(sub == player_color) == 3 and np.count_nonzero(sub == 0) == 1:
                score += THREE_IN_A_ROW_SCORE
            if np.count_nonzero(sub == player_color) == 4:
                score += FOUR_IN_A_ROW_SCORE

    # check for vertical opportunities
    for col in range(COLUMNS):
        column = game.board[:, col]
        for row in range(ROWS - 4 + 1):
            sub = column[row:row+4]
            if np.count_nonzero(sub == player_color) == 2 and np.count_nonzero(sub == 0) == 2:
                score += TWO_IN_A_ROW_SCORE
            if np.count_nonzero(sub == player_color) == 3 and np.count_nonzero(sub == 0) == 1:
                score += THREE_IN_A_ROW_SCORE
            if np.count_nonzero(sub == player_color) == 4:
                score += FOUR_IN_A_ROW_SCORE

    # check for diagonal opportunities
    # TODO

    # check for horizontal threats: for every subsection of 4 places, check is there are 2 or 3 same,
    # with empy spaces in-between
    for row in range(ROWS):
        r = game.board[row, :]
        for col in range(COLUMNS - 4 + 1):
            sub = r[col:col+4]
            if np.count_nonzero(sub == adverse_color) == 2 and np.count_nonzero(sub == 0) == 2:
                score -= TWO_IN_A_ROW_SCORE
            if np.count_nonzero(sub == adverse_color) == 3 and np.count_nonzero(sub == 0) == 1:
                score -= THREE_IN_A_ROW_SCORE
            if np.count_nonzero(sub == adverse_color) == 4:
                score -= FOUR_IN_A_ROW_SCORE

    # check for vertical threats
    for col in range(COLUMNS):
        column = game.board[:, col]
        for row in range(ROWS - 4 + 1):
            sub = column[row:row+4]
            if np.count_nonzero(sub == adverse_color) == 2 and np.count_nonzero(sub == 0) == 2:
                score -= TWO_IN_A_ROW_SCORE
            if np.count_nonzero(sub == adverse_color) == 3 and np.count_nonzero(sub == 0) == 1:
                score -= THREE_IN_A_ROW_SCORE
            if np.count_nonzero(sub == adverse_color) == 4:
                score -= FOUR_IN_A_ROW_SCORE

    # check for diagonal opportunities
    # TODO

    # print('\n BOARD:')
    # print(game.board)
    # print(f"score: {score}")
    return score

def get_next_games(game):
    games = []
    for col in range(COLUMNS):
        if game.is_column_valid(col):
            new_game = game.clone()
            game.make_move(col)
            game.switch_players()
            games.append(new_game)
    return games