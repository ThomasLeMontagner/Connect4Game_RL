# Connect4Game with Reinforcement Learning

Connect Four is a two-player strategy game in which players take turns dropping colored discs from the top into a grid. The goal is to get four of your discs in a row (horizontally, vertically, or diagonally) before your opponent does.
<br>
![image](https://user-images.githubusercontent.com/56484383/210179364-32c988d8-b767-4574-a203-31294c142025.png) <br>
*source image: https://www.101computing.net/connect4-challenge/*


This `README.md` file provides a brief description of the Connect4 game, as well as instructions for installing the required packages, running the game from the command line, playing against an AI opponent, and starting the web API.


## Requirements

- Python 3.6 or later

## Installation

To install the required packages, run:

```bash
pip install -r requirements.txt
```
## Usage

To start a game run game.py
```
python game.py
```
You will be able to choose different modes: <br>
  * '0' for computer against computer
  * '1' for 1 human player against computer
  * '2' for 2 humans agaisnt each other <br>
  
Then the board is displayed in the terminal.

## Computer Agents
### Minimax
A computer agent using the minimax algorithm to choose the best action.

### Q-learning
A computer agent using q-learning apporach to choose the best action.
