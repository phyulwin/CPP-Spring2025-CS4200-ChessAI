# Kelly Lwin
# Spring 2025 CS4200
# Assignment 2
# train_model.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import chess, chess.pgn, random
from tqdm import tqdm

# generate random self-play games and save to pgn
def generate_dataset(pgn_file="sample.pgn", games=300, max_moves=40):
    results = ["1-0", "0-1", "1/2-1/2"]
    with open(pgn_file, "w") as f:
        for _ in range(games):
            board = chess.Board()
            game = chess.pgn.Game()
            node = game
            for _ in range(max_moves):
                if board.is_game_over(): break
                mv = random.choice(list(board.legal_moves))
                board.push(mv)
                node = node.add_variation(mv)
            game.headers["Result"] = random.choice(results)
            print(game, file=f, end="\n\n")
    print("PGN dataset generated.")

# read pgn and extract fen positions with game results
def pgn_to_tensors(pgn_file="sample.pgn"):
    Xs, ys = [], []
    with open(pgn_file) as f:
        while True:
            g = chess.pgn.read_game(f)
            if g is None:
                break
            outcome = g.headers.get("Result", "")
            if outcome not in ("1-0","0-1","1/2-1/2"):
                continue
            res = {"1-0":1, "0-1":-1, "1/2-1/2":0}[outcome]
            board = g.board()
            for mv in g.mainline_moves():
                if random.random() < 0.5:
                    Xs.append(board.fen())
                    ys.append(res)
                board.push(mv)
    print("Tensors prepared.")
    return Xs, ys

# encode a single fen string into a tensor
def encode(fen):
    board = chess.Board(fen)
    arr = np.zeros((12,8,8), np.float32)
    mapping = {1:0,2:1,3:2,4:3,5:4,6:5}
    for sq,p in board.piece_map().items():
        r,c = divmod(sq,8)
        arr[mapping[p.piece_type] + (0 if p.color else 6), r, c] = 1
    return arr.flatten()

# convert fen list to tensors and save dataset
def create_dataset(Xs, ys):
    X = torch.tensor([encode(fen) for fen in tqdm(Xs)], dtype=torch.float32)
    y = torch.tensor([(r+1)/2 for r in ys], dtype=torch.float32).unsqueeze(1)
    torch.save((X, y), "fen_dataset.pt")
    print("fen_dataset.pt saved.")
    return X, y

# convert fen list to tensors and save dataset
def train_and_save_model(X, y, model_path="model.pt"):
    ds = TensorDataset(X, y)
    loader = DataLoader(ds, batch_size=2048, shuffle=True)

    net = nn.Sequential(
        nn.Linear(768,256), nn.ReLU(),
        nn.Linear(256,64),  nn.ReLU(),
        nn.Linear(64,1),    nn.Sigmoid())

    opt = optim.Adam(net.parameters(), lr=3e-4)

    for epoch in range(5):  # Adjust epochs as needed
        for xb, yb in loader:
            pred = net(xb)
            loss = nn.functional.binary_cross_entropy(pred, yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
        print(f"Epoch {epoch+1} loss={loss.item():.4f}")

    torch.save(net.state_dict(), model_path)
    print(f"Model saved to {model_path}")

# excecute this file to train the model
if __name__ == "__main__":
    generate_dataset()
    Xs, ys = pgn_to_tensors()
    X, y = create_dataset(Xs, ys)
    train_and_save_model(X, y)