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

        self.turn_label = tk.Label(self.root, text = f"{self.current_turn}'s Turn", font = ("Arial", 12))
        self.turn_label.grid(row = 4, column = 3, columnspan = 3, pady = 10)

    def setup_player_ui(self, color, row):
        tk.Label(self.root, text=f"{color} Player:").grid(row = row, column = 0, padx = 5, pady = 5)
        tk.Radiobutton(self.root, text = "Human", variable = self.blue_player if color == "Blue" else self.red_player, value = 'Human').grid(row = row, column = 1)
        tk.Radiobutton(self.root, text = "Computer", variable = self.blue_player if color == "Blue" else self.red_player, value = 'Computer').grid(row = row, column = 2)
        tk.Radiobutton(self.root, text = "S", variable = self.blue_symbol if color == "Blue" else self.red_symbol, value = 'S').grid(row = row + 1, column = 1)
        tk.Radiobutton(self.root, text = "O", variable = self.blue_symbol if color == "Blue" else self.red_symbol, value = 'O').grid(row = row + 1, column = 2)

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

            if self.check_sos(i, j):
                if self.current_turn == "Blue":
                    self.blue_sos_count += 1
                else:
                    self.red_sos_count += 1
                self.update_score()
            self. turn_label.config(text = f"{self.current_turn}'s Turn")

    
    def check_sos(self, i, j):
        symbol = self.squares[i][j]['text']
        if symbol == "":
            return False
        
        count_sos = 0
        x, y = i, j  
        while 0 <= y + 1 < self.board_size.get() and self.squares[x][y +1 ]['text'] == symbol:
            y += 1
            count_sos += 1
        y = j
        while 0 <= y -1 < self.board_size.get() and self.squares[x][y - 1]['text'] == symbol:
            y -= 1
            count_sos += 1
        if count_sos >= 2:
            return True
        
        count_sos = 0
        x, y = i, j  
        while 0 <= x + 1 < self.board_size.get() and self.squares[x + 1][y]['text'] == symbol:
            x += 1
            count_sos += 1
        x = i
        while 0 <= x -1 < self.board_size.get() and self.squares[x - 1][y]['text'] == symbol:
            x -= 1
            count_sos += 1
        if count_sos >= 2:
            return True
        
        count_sos = 0
        x, y = i, j
        while 0 <= x + 1 < self.board_size.get() and 0<= y + 1 < self.board_size.get() and self.squares[x + 1][y + 1]['text'] == symbol:
            x += 1
            y += 1
            count_sos += 1
        while 0 <= x - 1 < self.board_size.get() and 0 <= y -1 < self.board_size.get() and self.squares[x - 1][y - 1]['text'] == symbol:
            x -= 1
            y -= 1
            count_sos += 1
        if count_sos >=2:
            return True
        
        count_sos = 0
        x, y = i, j
        while 0 <= x + 1 < self.board_size.get() and 0 <= y - 1 < self.board_size.get() and self.squares[x + 1][y - 1]['text'] == symbol:
            x += 1
            y -= 1
            count_sos += 1
        x,y = i, j
        while 0 <= x -1 < self.board_size.get() and 0 <= y + 1 < self.board_size.get() and self.squares[x - 1][y + 1]['text'] == symbol:
            x -= 1
            y += 1
            count_sos += 1
        if count_sos >= 2:
            return True
        
        return False 
    
    def update_score(self):
        score_label = tk.Label(self.root, text = f"Blue: {self.blue_sos_count} - Red: {self.red_sos_count}", font = ("Arial", 12))
        score_label.grid(row = 5, column = 3, columnspan = 3)

    def end_game(self): 
        if self.blue_sos_count > self.red_sos_count:
            winner = "Blue Player Wins!"
        elif self.red_sos_count > self.blue_sos_count:
            winner = " Red Player Wins!"
        else: 
            winner = "It's a tie!"

        messagebox.showinfo("Game Over", winner)
                                                                                                                       



















    # RESOURCES USED LISTED BELOW
    # Youtube: https://www.youtube.com/watch?v=YXPyB4XeYLA
    # Website: https://www.geeksforgeeks.org/tic-tac-toe-game-with-gui-using-tkinter-in-python/
    # Youtube: https://www.youtube.com/watch?v=xx0qmpuA-vM
    # Youtube: https://www.youtube.com/watch?v=IJ-iVnN09-8
    # Website: https://www.geeksforgeeks.org/python-tkinter-entry-widget/