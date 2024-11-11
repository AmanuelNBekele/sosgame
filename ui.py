import tkinter as tk
from tkinter import messagebox

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
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is None:
                    return i, j  

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
            sequence = [(i, j)]
            
            for dx, dy in [(dx1, dy1), (dx2, dy2)]:
                x, y = i, j
                while 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    x, y = x + dx, y + dy
                    sequence.append((x, y))

            if len(sequence) == 3:  
                (x1, y1), (x2, y2), (x3, y3) = sequence
                if self.board[x1][y1] == "S" and self.board[x2][y2] == "O" and self.board[x3][y3] == "S":
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
        self.red_player = HumanPlayer("Red", "O")
        self.current_turn = "Blue"
        self.game_mode = "Simple" 
        self.game_over = False  

    def reset_game(self):
        self.board.reset()
        self.current_turn = "Blue"
        self.game_over = False

    def make_move(self, i, j):
        if self.game_over:
            return False  

        if self.current_turn == "Blue":
            player = self.blue_player
        else:
            player = self.red_player

        if self.board.place_symbol(i, j, player.get_symbol()):
            sos_sequences = self.board.check_sos(i, j, player.get_symbol(), self.game_mode)
            self.board.update_score(player.get_symbol(), sos_sequences, self.game_mode)

            if self.game_mode == "Simple" and sos_sequences:
                self.game_over = True
                return player.name 

            return True
        return False

    def switch_turn(self):
        if not self.game_over:
            self.current_turn = "Red" if self.current_turn == "Blue" else "Blue"

    def get_score(self):
        return self.board.get_score()

    def set_player_symbol(self, color, symbol):
        if color == "Blue":
            self.blue_player.set_symbol(symbol)
        else:
            self.red_player.set_symbol(symbol)

    def check_winner(self):

        if self.game_over:
            return self.current_turn
        return None

class SOS:
    def __init__(self, root):

        self.root = root
        self.root.title("SOS Game")

        self.game = SOSGame()

        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, pady=10)

        self.game_mode_label = tk.Label(self.top_frame, text="Game Mode:")
        self.game_mode_label.grid(row=0, column=0)
        self.game_mode_var = tk.StringVar(value='Simple')
        self.game_mode_dropdown = tk.OptionMenu(self.top_frame, self.game_mode_var, 'Simple', 'General', command=self.update_game_mode)
        self.game_mode_dropdown.grid(row=0, column=1)

        self.board_size_label = tk.Label(self.top_frame, text="Board Size:")
        self.board_size_label.grid(row=0, column=2)
        self.board_size_var = tk.StringVar(value='8')
        self.board_size_dropdown = tk.OptionMenu(self.top_frame, self.board_size_var, *[str(i) for i in range(3, 9)], command=self.update_board_size)
        self.board_size_dropdown.grid(row=0, column=3)

        self.turn_label = tk.Label(self.top_frame, text="Blue's Turn", font=("Arial", 14))
        self.turn_label.grid(row=0, column=4, padx=10)

        self.score_frame = tk.Frame(self.root)
        self.score_frame.grid(row=1, column=1, padx=10, pady=10)

        self.blue_score_label = tk.Label(self.score_frame, text="Blue: 0", font=("Arial", 14))
        self.blue_score_label.grid(row=0, column=0, padx=20)
        self.red_score_label = tk.Label(self.score_frame, text="Red: 0", font=("Arial", 14))
        self.red_score_label.grid(row=0, column=1, padx=20)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=2, column=1, padx=10, pady=10)

        self.setup_player_ui("Blue", 1, 0)
        self.setup_player_ui("Red", 1, 2)

        self.create_board(self.game.board.size)
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.reset_game_ui, height=2, width=15)
        self.new_game_button.grid(row=3, column=1, pady=10)

    def setup_player_ui(self, color, row, column):
        player_var = tk.StringVar(value="Human")
        symbol_var = tk.StringVar(value="S")
        tk.Label(self.root, text=f"{color} Player:").grid(row=row, column=column, padx=5, pady=5)
        tk.Radiobutton(self.root, text="Human", variable=player_var, value="Human").grid(row=row+1, column=column)
        tk.Radiobutton(self.root, text="Computer", variable=player_var, value="Computer").grid(row=row+2, column=column)
        tk.Label(self.root, text="Choose Symbol:").grid(row=row+3, column=column, padx=5, pady=5)
        tk.Radiobutton(self.root, text="S", variable=symbol_var, value="S", command=lambda: self.update_player_symbol(color, 'S')).grid(row=row+4, column=column)
        tk.Radiobutton(self.root, text="O", variable=symbol_var, value="O", command=lambda: self.update_player_symbol(color, 'O')).grid(row=row+5, column=column)

        if color == "Blue":
            self.blue_player_var = player_var
            self.blue_symbol_var = symbol_var
        else:
            self.red_player_var = player_var
            self.red_symbol_var = symbol_var

    def update_player_symbol(self, color, symbol):
        self.game.set_player_symbol(color, symbol)

    def update_game_mode(self, mode):
        self.game.game_mode = mode

    def update_board_size(self, size):
        self.game.board.size = int(size)
        self.reset_game_ui()

    def create_board(self, size):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.squares = [[tk.Label(self.board_frame, width=4, height=2, borderwidth=1, relief="solid", font=('Arial', 18)) for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                self.squares[i][j].grid(row=i, column=j)
                self.squares[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.cell_clicked(x, y))

    def reset_game_ui(self):
        self.game.reset_game()
        self.update_score()
        self.create_board(self.game.board.size)

    def update_score(self):
        blue_score, red_score = self.game.get_score()
        self.blue_score_label.config(text=f"Blue: {blue_score}")
        self.red_score_label.config(text=f"Red: {red_score}")

    def cell_clicked(self, i, j):
        if not self.game.game_over and self.game.make_move(i, j):
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