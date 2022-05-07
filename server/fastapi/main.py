from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://bhoos.github.io"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

@app.post("/play")
async def root(payload: Request):
    payload_json = await payload.json()
    
    valid_moves = []
    for i, row in enumerate(payload_json["state"]):
        for j, col in enumerate(row):
            if not col:
                valid_moves.append((i, j))
    
    move = random.choice(valid_moves)
    
    return {"row":move[0], "col":move[1]}
