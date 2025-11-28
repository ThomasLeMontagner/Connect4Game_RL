"""FastAPI service exposing Connect Four gameplay endpoints."""

from __future__ import annotations

import fastapi
import uvicorn
from pydantic import BaseModel
from game import ConnectFour


game: ConnectFour = ConnectFour(mode="1")

class MoveRequest(BaseModel):
    """Payload describing the requested column move."""
    column: int

class GameStateResponse(BaseModel):
    """Response containing the board state and winner flag."""
    board: list[list[int]]
    winner: int | None

app: fastapi.FastAPI = fastapi.FastAPI()

@app.post("/make_move")
def make_move(request: MoveRequest) -> GameStateResponse:
    """Apply a move to the shared game and return the updated state."""
    column = request.column
    game.make_move(column)
    winner = game.check_winner()
    return GameStateResponse(board=game.board, winner=winner)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
