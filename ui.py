import tkinter as tk
from tkinter import messagebox
import random
import time

class Player:
    def __init__(self, name, symbol="S"):
        self.name = name
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, name, symbol="S"):
        super().__init__(name, symbol)

    def make_move(self, board):
        pass 

class ComputerPlayer(Player):
    def __init__(self, name, symbol="S"):
        super().__init__(name, symbol)

    def make_move(self, board):
        empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] is None]
        return random.choice(empty_cells) if empty_cells else None

class Board:
    def __init__(self, size=8):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.blue_sos_count = 0
        self.red_sos_count = 0

    def reset(self):
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.blue_sos_count = 0
        self.red_sos_count = 0

    def place_symbol(self, i, j, symbol):
        if self.board[i][j] is None:
            self.board[i][j] = symbol
            return True
        return False

    def check_sos(self, i, j, symbol, game_mode):
        sos_found = []

        directions = [
            ((0, -1), (0, 1)),  
            ((-1, 0), (1, 0)),  
            ((-1, -1), (1, 1)),  
            ((-1, 1), (1, -1)), 
        ]

        for (dx1, dy1), (dx2, dy2) in directions:
            sequence = []
            for dx, dy in [(dx1, dy1), (dx2, dy2)]:
                x, y = i, j
                while 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    x, y = x + dx, y + dy
                    sequence.append((x, y))

            if len(sequence) == 2: 
                (x1, y1), (x2, y2) = sequence
                if self.board[x1][y1] == "S" and self.board[x2][y2] == "S":
                    sos_found.append(sequence)

        return sos_found

    def update_score(self, symbol, sos_sequences, game_mode):
        for sequence in sos_sequences:
            if game_mode == "Simple":
                if symbol == "S":
                    self.blue_sos_count += 1
                elif symbol == "O":
                    self.red_sos_count += 1
            elif game_mode == "General":
                if "S" in [self.board[x][y] for x, y in sequence]:
                    self.blue_sos_count += 1
                if "O" in [self.board[x][y] for x, y in sequence]:
                    self.red_sos_count += 1

    def get_score(self):
        return self.blue_sos_count, self.red_sos_count

    def is_full(self):
        for row in self.board:
            if None in row:
                return False
        return True

class SOSGame:
    def __init__(self):
        self.board = Board(8)
        self.blue_player = HumanPlayer("Blue", "S")  
        self.red_player = ComputerPlayer("Red", "O")  
        self.current_turn = "Blue"
        self.game_mode = "Simple"
        self.extra_turn = False 

    def reset_game(self):
        self.board.reset()
        self.current_turn = "Blue"
        self.extra_turn = False

    def make_move(self, i, j):
        if self.current_turn == "Blue":
            player = self.blue_player
        else:
            player = self.red_player

        if self.board.place_symbol(i, j, player.get_symbol()):
            sos_sequences = self.board.check_sos(i, j, player.get_symbol(), self.game_mode)
            self.board.update_score(player.get_symbol(), sos_sequences, self.game_mode)

            if self.game_mode == "Simple" and sos_sequences:
                return "SOS"

            if self.game_mode == "General" and sos_sequences:
                self.extra_turn = True
                return True  
            else:
                self.extra_turn = False
                return True 
        return False

    def switch_turn(self):
        if not self.extra_turn:
            self.current_turn = "Red" if self.current_turn == "Blue" else "Blue"

    def get_score(self):
        return self.board.get_score()

    def set_player_symbol(self, color, symbol):
        if color == "Blue":
            self.blue_player.set_symbol(symbol)
        else:
            self.red_player.set_symbol(symbol)

    def set_player_type(self, color, player_type):
        if color == "Blue":
            if player_type == "Human":
                self.blue_player = HumanPlayer("Blue", self.blue_player.symbol)
            else:
                self.blue_player = ComputerPlayer("Blue", self.blue_player.symbol)
        else:
            if player_type == "Human":
                self.red_player = HumanPlayer("Red", self.red_player.symbol)
            else:
                self.red_player = ComputerPlayer("Red", self.red_player.symbol)

    def check_winner(self):
        blue_score, red_score = self.board.get_score()

        if blue_score >= 3: 
            return "Blue"
        elif red_score >= 3:  
            return "Red"
        elif self.board.is_full(): 
            return "Tie"
        return None

class SOSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")

        self.game = SOSGame()

        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, pady=10)

        self.game_mode_label = tk.Label(self.top_frame, text="Game Mode:")
        self.game_mode_label.grid(row=0, column=0)
        self.game_mode_var = tk.StringVar(value="Simple")
        self.simple_button = tk.Radiobutton(self.top_frame, text="Simple", variable=self.game_mode_var, value="Simple", command=lambda: self.update_game_mode("Simple"))
        self.general_button = tk.Radiobutton(self.top_frame, text="General", variable=self.game_mode_var, value="General", command=lambda: self.update_game_mode("General"))
        self.simple_button.grid(row=0, column=1)
        self.general_button.grid(row=0, column=2)

        self.board_size_label = tk.Label(self.top_frame, text="Board Size:")
        self.board_size_label.grid(row=1, column=0)
        self.board_size_var = tk.StringVar(value="8")
        board_size_dropdown = tk.OptionMenu(self.top_frame, self.board_size_var, "3", "4", "5", "6", "7", "8", command=self.update_board_size)
        board_size_dropdown.grid(row=1, column=1)

        self.player_frame = tk.Frame(self.root)
        self.player_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.create_player_ui("Blue", self.player_frame)
        self.create_player_ui("Red", self.player_frame)

        self.start_game_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_game_button.grid(row=2, column=2)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=3, column=0, columnspan=3)

        self.score_label = tk.Label(self.root, text="Blue: 0 - Red: 0", font=('Arial', 14))
        self.score_label.grid(row=4, column=0, columnspan=3)

        self.turn_label = tk.Label(self.root, text="Blue's Turn", font=('Arial', 14))
        self.turn_label.grid(row=5, column=0, columnspan=3)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.reset_game_ui)
        self.new_game_button.grid(row=6, column=2)

    def create_player_ui(self, color, parent):
        player_var = tk.StringVar(value="Human")
        symbol_var = tk.StringVar(value="S" if color == "Blue" else "O")

        row = 0 if color == "Blue" else 1
        column = 0 if color == "Blue" else 2

        tk.Label(parent, text=f"{color} Player:").grid(row=row, column=column)
        tk.Label(parent, text="Player Type:").grid(row=row + 1, column=column)
        player_dropdown = tk.OptionMenu(parent, player_var, "Human", "Computer", command=lambda value: self.update_player_type(color, value))
        player_dropdown.grid(row=row + 2, column=column)
        tk.Label(parent, text="Select Symbol:").grid(row=row + 3, column=column)
        symbol_dropdown = tk.OptionMenu(parent, symbol_var, "S", "O", command=lambda value: self.update_player_symbol(color, value))
        symbol_dropdown.grid(row=row + 4, column=column)

        if color == "Blue":
            self.blue_player_var = player_var
            self.blue_symbol_var = symbol_var
        else:
            self.red_player_var = player_var
            self.red_symbol_var = symbol_var

    def update_player_symbol(self, color, symbol):
        self.game.set_player_symbol(color, symbol)

    def update_player_type(self, color, player_type):
        self.game.set_player_type(color, player_type)

    def update_game_mode(self, mode):
        self.game.game_mode = mode

    def update_board_size(self, size):
        self.game.board.size = int(size)
        self.reset_game_ui() 

    def reset_game_ui(self):
        self.game.reset_game()
        self.update_score()
        self.create_board(self.game.board.size)

    def create_board(self, size):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.squares = [[tk.Label(self.board_frame, width=4, height=2, borderwidth=1, relief="solid", font=('Arial', 18)) for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                self.squares[i][j].grid(row=i, column=j)
                self.squares[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.cell_clicked(x, y))

    def update_score(self):
        blue_score, red_score = self.game.get_score()
        self.score_label.config(text=f"Blue: {blue_score} - Red: {red_score}")

    def cell_clicked(self, i, j):
        if self.game.make_move(i, j) == "SOS":
            result = self.game.check_winner()
            if result:
                if result == "Tie":
                    messagebox.showinfo("Game Over", "It's a Tie!")
                else:
                    messagebox.showinfo("Game Over", f"{result} Wins!")
                self.reset_game_ui() 
                return
        else:
            symbol = self.game.blue_player.get_symbol() if self.game.current_turn == "Blue" else self.game.red_player.get_symbol()
            color = "blue" if self.game.current_turn == "Blue" else "red"
            self.squares[i][j].config(text=symbol, fg=color)
            self.update_score()

            result = self.game.check_winner()
            if result:
                if result == "Tie":
                    messagebox.showinfo("Game Over", "It's a Tie!")
                else:
                    messagebox.showinfo("Game Over", f"{result} Wins!")
                self.reset_game_ui()
                return

            self.turn_label.config(text=f"{self.game.current_turn}'s Turn")
            self.game.switch_turn()

            if self.game.current_turn == "Red" and isinstance(self.game.red_player, ComputerPlayer):
                self.computer_move()
            elif self.game.current_turn == "Blue" and isinstance(self.game.blue_player, ComputerPlayer):
                self.computer_move()

    def computer_move(self):
        if isinstance(self.game.blue_player, ComputerPlayer) and self.game.current_turn == "Blue":
            move = self.game.blue_player.make_move(self.game.board.board)
        elif isinstance(self.game.red_player, ComputerPlayer) and self.game.current_turn == "Red":
            move = self.game.red_player.make_move(self.game.board.board)
        else:
            return

        if move is None:
            print("No valid moves available.")
            return

        i, j = move  
        time.sleep(1) 
        self.cell_clicked(i, j)

    def start_game(self):
        self.game.reset_game()
        self.reset_game_ui()

        if isinstance(self.game.blue_player, ComputerPlayer):
            self.computer_move()
        elif isinstance(self.game.red_player, ComputerPlayer):
            self.computer_move()