# Kelly Lwin
# Spring 2025 CS4200
# Assignment 2
# engine.py

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import torch, chess
# global variable
net = None

# load model if not loaded
def _load():
    global net
    if net is None:
        import torch.nn as nn
        net = nn.Sequential(
            nn.Linear(768,256), nn.ReLU(),
            nn.Linear(256,64),  nn.ReLU(),
            nn.Linear(64,1),    nn.Sigmoid())
        net.load_state_dict(torch.load("model.pt", map_location="cpu"))
        net.eval()

# encode board to tensor
def _encode(board):
    import numpy as np
    arr = np.zeros((12,8,8), np.float32)
    m = {1:0,2:1,3:2,4:3,5:4,6:5}
    for sq,p in board.piece_map().items():
        r,c = divmod(sq,8)
        arr[m[p.piece_type]+(0 if p.color else 6), r, c] = 1
    return torch.from_numpy(arr.flatten()).unsqueeze(0)

# get score from model
@torch.no_grad()
def score(board):
    _load()
    return net(_encode(board).float()).item() 
    # p = net(_encode(board).float()).item()
    # return (2*p - 1)

# search best move using minimax
def _search(board, d, a=-2, b=2):
    if d==0 or board.is_game_over():
        return score(board), None
    best, move = -2, None
    for mv in board.legal_moves:
        board.push(mv)
        val,_ = _search(board, d-1, -b, -a); val = -val
        board.pop()
        if val>best: best, move = val, mv
        a = max(a,val)
        if a>=b: break
    return best, move

# return best move from fen
def best_move(fen, depth=3):
    board = chess.Board(fen)
    return _search(board, depth)[1]