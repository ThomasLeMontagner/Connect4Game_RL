import fastapi
import uvicorn
from pydantic import BaseModel
from game import *
class MoveRequest(BaseModel):
    column: int

class GameStateResponse(BaseModel):
    board: List[List[int]]
    winner: Optional[int]

app = fastapi.FastAPI()

@app.post("/make_move")
def make_move(request: MoveRequest):
    column = request.column
    game.make_move(column)
    winner = game.check_winner()
    return GameStateResponse(board=game.board, winner=winner)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
