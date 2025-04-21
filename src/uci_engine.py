# Kelly Lwin
# Spring 2025 CS4200
# Assignment 2
# uci_engine.py

# import required modules and engine
import sys, chess, engine

# create new chess board
board = chess.Board()

while True:
    # read commands from standard input
    cmd = sys.stdin.readline().strip()
    
    # respond to uci init command
    if cmd == "uci":
        print("id name MLChess\nuciok"); sys.stdout.flush()
    # confirm readiness
    elif cmd == "isready":
        print("readyok"); sys.stdout.flush()
    # set board to starting position with optional moves
    elif cmd.startswith("position startpos"):
        board = chess.Board()
        if "moves" in cmd:
            for m in cmd.split("moves")[1].split():
                board.push_uci(m)
    # set board from given fen string
    elif cmd.startswith("position fen"):
        board = chess.Board(cmd.split(" ",2)[2])
    # calculate and return best move from current board
    elif cmd.startswith("go"):
        bm = engine.best_move(board.fen()).uci()
        print("bestmove", bm); sys.stdout.flush()
    # exit the loop and stop the engine
    elif cmd == "quit":
        break