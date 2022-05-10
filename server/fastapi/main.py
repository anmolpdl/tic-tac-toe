from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import math
from node import MCTSNode


def MCTS(state, turn, n, c):
    root = MCTSNode(state=state, turn=turn)
    root.expand()

    for i in range(n):
        node = root
        # select a node
        while node.children:
            ucbs = []
            for child in node.children:
                if child.wins != 0 and child.plays != 0:
                    ucb = (child.wins / child.plays) + (
                        c * ((math.log(i) / child.plays) ** (1 / 2))
                    )
                else:
                    ucb = math.inf
                ucbs.append(ucb)

            node = node.children[ucbs.index(max(ucbs))]

        # expand the node
        node = node.expand()
        # node.expand()

        # simulate the node
        outcome = (
            node.simulate_rnd()
        )  # determine what was game outcome, win=1, draw=0.5, loss=0

        # backpropagate values to parent(s)
        node.backpropagate(outcome)

    final_scores = [
        child.wins / child.plays if child.plays != 0 else 0 for child in root.children
    ]
    final_node = root.children[final_scores.index(max(final_scores))]

    for child in root.children:
        child.visualize_tree()
    return final_node.parent_move


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

    print(f"Received payload: {payload_json}")

    # randomly moving
    # valid_moves = []
    # for i, row in enumerate(payload_json["state"]):
    #    for j, col in enumerate(row):
    #        if not col:
    #            valid_moves.append((i, j))

    # move = random.choice(valid_moves)

    move = MCTS(payload_json["state"], payload_json["turn"], 2000, 0.77)

    return {"row": move[0], "col": move[1]}
