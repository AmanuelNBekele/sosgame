import tkinter as tk
from tkinter import messagebox

class SOS:

    def __init__(self, root) -> None:
        self.root = root
        self.root.title("SOS")

        self.blue_player = tk.StringVar(value ='Human')
        self.blue_symbol = tk.StringVar(value ='S')
        self.red_player = tk.StringVar(value ='Human')
        self.red_symbol = tk.StringVar(value ='S')
        self.record_game = tk.BooleanVar(value =False)

        self.current_turn = "Blue"
        self.board_size = tk.IntVar(value = 8)
        self.game_mode = tk.StringVar(value = 'Simple')
        self.blue_sos_count = 0
        self.red_sos_count = 0

        self.setup_ui()

        self.board = tk.Frame(root)
        self.board.grid(row = 7, column = 0, columnspan = 6, padx = 5, pady = 5)
        self.squares = []
        self.create_board(self.board_size.get())

    def setup_ui(self):
        tk.Label(self.root, text = "Game Mode:").grid(row = 0, column = 0, padx = 5, pady = 5)
        tk.Radiobutton(self.root, text = "Simple", variable = self.game_mode, value = 'Simple').grid(row = 0, column = 1)
        tk.Radiobutton(self.root, text = "General", variable = self.game_mode, value = 'General').grid(row = 0, column = 2)

        tk.Label(self.root, text="Board Size:").grid(row = 0, column = 3)
        self.board_size_entry = tk.Entry(self.root, width = 2)
        self.board_size_entry.grid(row = 0, column = 4)
        self.board_size_entry.insert(0, "8")

        self.setup_player_ui("Blue", 1)
        self.setup_player_ui("Red", 3)

        tk.Checkbutton(self.root, text = "Record Game", variable = self.record_game).grid(row = 1, column = 3, columnspan = 3, pady = 5)

        tk.Button(self.root, text="New Game", command = self.reset_board).grid(row = 3, column = 3, columnspan = 3)

    def setup_player_ui(self, color, row):
        tk.Label(self.root, text=f"{color} Player:").grid(row = row, column = 0, padx = 5, pady = 5)
        tk.Radiobutton(self.root, text = "Human", variable = self.blue_player if color == "Blue" else self.red_player, value = 'Human').grid(row = row, column = 1)
        tk.Radiobutton(self.root, text = "Computer", variable = self.blue_player if color == "Blue" else self.red_player, value = 'Computer').grid(row = row, column = 2)
        tk.Radiobutton(self.root, text = "S", variable = self.blue_symbol if color == "Blue" else self.red_symbol, value = 'S').grid(row = row + 1, column = 1)
        tk.Radiobutton(self.root, text = "O", variable = self.blue_symbol if color == "Blue" else self.red_symbol, value = 'O').grid(row = row + 1, column = 2)

    # RESOURCES USED LISTED BELOW
    # Youtube: https://www.youtube.com/watch?v=YXPyB4XeYLA
    # Website: https://www.geeksforgeeks.org/tic-tac-toe-game-with-gui-using-tkinter-in-python/
    # Youtube: https://www.youtube.com/watch?v=xx0qmpuA-vM
    # Youtube: https://www.youtube.com/watch?v=IJ-iVnN09-8
    # Website: https://www.geeksforgeeks.org/python-tkinter-entry-widget/