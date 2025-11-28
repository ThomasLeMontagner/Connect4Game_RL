from __future__ import annotations

import random

import numpy as np
from game import ConnectFour

# create an empty dataset
DatasetEntry = tuple[np.ndarray, int]
dataset: list[DatasetEntry] = []

# simulate a large number of games
for i in range(10000):
    game = ConnectFour(mode='0')
    while True:
        # choose a random column to make a move in
        column = random.randint(0, 6)
        try:
            game.make_move(column)
        except ValueError:
            continue
        winner = game.check_winner()
        if winner != 0:
            break
    # add the board state and label to the dataset
    board_state = game.board.flatten()
    label = 1 if winner == game.player else -1 if winner == -game.player else 0
    dataset.append((board_state, label))

# shuffle the dataset and split it into training and test sets
random.shuffle(dataset)
train_size = int(len(dataset) * 0.8)
train_set: list[DatasetEntry] = dataset[:train_size]
test_set: list[DatasetEntry] = dataset[train_size:]
