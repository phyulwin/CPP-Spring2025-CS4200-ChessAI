# Kelly Lwin
# Spring 2025 CS4200
# Assignment 2
# main.py 

# import libraries and engine model
import chess
import tkinter as tk
from PIL import Image, ImageTk
import engine

PIECE_IMAGES = {}

# map chess pieces to image files
PIECE_NAME_MAP = {
    'r': 'darkRook.png',
    'n': 'darkKnight.png',
    'b': 'darkBishop.png',
    'q': 'darkQueen.png',
    'k': 'darkKing.png',
    'p': 'darkPawn.png',
    'R': 'lightRook.png',
    'N': 'lightKnight.png',
    'B': 'lightBishop.png',
    'Q': 'lightQueen.png',
    'K': 'lightKing.png',
    'P': 'lightPawn.png'
}

# gui class for the chess game
class ChessGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("CS4200 Assignment2 Chess ML")
        self.board = chess.Board()
        self.canvas = tk.Canvas(self.window, width=480, height=480)
        self.canvas.pack()
        self.entry = tk.Entry(self.window)
        self.entry.pack()
        self.button = tk.Button(self.window, text="Move", command=self.player_move)
        self.button.pack()
        self.load_images()
        self.update_board()

    # load piece images into memory
    def load_images(self):
        for symbol, filename in PIECE_NAME_MAP.items():
            img = Image.open(f'pieces/{filename}')
            img = img.resize((60, 60), Image.LANCZOS)
            PIECE_IMAGES[symbol] = ImageTk.PhotoImage(img)
    
    # draw and update the board and pieces
    def update_board(self):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]
        for row in range(8):
            for col in range(8):
                x = col * 60
                y = (7 - row) * 60
                self.canvas.create_rectangle(x, y, x+60, y+60, fill=colors[(row + col) % 2])
                piece = self.board.piece_at(row * 8 + col)
                if piece:
                    symbol = piece.symbol()
                    self.canvas.create_image(x, y, anchor=tk.NW, image=PIECE_IMAGES[symbol])
    
    # handle user move input and update board
    def player_move(self):
        move_uci = self.entry.get()
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.entry.delete(0, tk.END)
                self.update_board()
                self.window.after(500, self.ai_move)
            else:
                print("Illegal move")
        except Exception as e:
            print("Invalid input:", e)
    
    # get ai move, print it, and update board
    def ai_move(self):
        if self.board.turn:
            return
        move = engine.best_move(self.board.fen())
        if move:
            print(f"AI plays: {move.uci()}\n")
            self.board.push(move)
            self.update_board()
            copy_board = chess.Board(self.board.fen())
            copy_board.turn = chess.WHITE
            score, mv = engine._search(copy_board, 3)
            if mv:
                print(f"Suggested White move: {mv.uci()}\n")
        else:
            print("Game over or no legal moves")
    
    # start the application
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ChessGUI()
    app.run()