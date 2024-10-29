import tkinter as tk
from ui import SOS
from tkinter import messagebox

class Game:

    def create_board(self, size):
        for widget in self.board.winfo_children():
            widget.destroy()

        self.squares = [[tk.Label(self.board, width = 4, height = 2, borderwidth = 1, relief = "solid", font = ('Arial', 18)) for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                self.squares[i][j].grid(row = i, column = j)
                self.squares[i][j].bind("<Button-1>", lambda e, x = i, y = j: self.make_move(x, y))

    def reset_board(self):
        try:
            size = int(self.board_size_entry.get())
            if size >= 3:
                self.board_size.set(size)
                self.create_board(self.board_size.get())
                self.current_turn = "Blue"
                self.blue_sos_count = 0
                self.red_sos_count = 0
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Minimum board size is 3.")

    def make_move(self, i, j):
        if self.squares[i][j]['text'] == "":
            if self.current_turn == "Blue":
                self.squares[i][j].config(text=self.blue_symbol.get(), fg = "blue")
                self.current_turn = "Red"
            else:
                self.squares[i][j].config(text=self.red_symbol.get(), fg = "red") 
                self.current_turn = "Blue"

class SimpleGame:
    pass

class GeneralGame:
    pass