import random
import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, symbol, player_type, color):
        self.symbol = symbol
        self.player_type = player_type 
        self.color = color
        self.score = 0

    def make_move(self, board):
        if self.player_type == 'Human':
            return None
        elif self.player_type == 'Computer':
            return self.best_move(board)

    def best_move(self, board):
        move = self.find_sos_move(board, self.symbol)
        if move:
            return move
        opponent_symbol = 'O' if self.symbol == 'S' else 'S'
        move = self.find_sos_move(board, opponent_symbol)
        if move:
            return move
        return self.random_move(board)

    def find_sos_move(self, board, symbol):
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] == '':
                    board.update_cell(r, c, symbol)
                    if board.check_sos() > 0:
                        board.update_cell(r, c, '')
                        return (r, c)
                    board.update_cell(r, c, '')
        return None

    def random_move(self, board):
        empty_cells = [(r, c) for r in range(board.size) for c in range(board.size) if board.grid[r][c] == '']
        return random.choice(empty_cells) if empty_cells else None

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]

    def initialize_board(self):
        self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]

    def update_cell(self, row, col, symbol):
        if self.grid[row][col] == '':
            self.grid[row][col] = symbol
            return True
        return False

    def check_sos(self):
        sos_count = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.check_sequence(r, c):
                    sos_count += 1
        return sos_count

    def check_sequence(self, r, c):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            sequence = []
            for i in range(3):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    sequence.append(self.grid[nr][nc])

            if sequence == ['S', 'O', 'S']:
                return True
        return False

    def is_full(self):
        return all(self.grid[r][c] != '' for r in range(self.size) for c in range(self.size))

    def reset_board(self):
        self.initialize_board()

class Game:
    def __init__(self, player1, player2, game_mode='Simple'):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.game_mode = game_mode
        self.board = Board(3) 
        self.turns_taken = 0 
        self.extra_turn = False  

    def start_game(self):
        self.board.initialize_board()
        self.turns_taken = 0
        self.extra_turn = False

    def play_turn(self, row, col):
        if self.board.update_cell(row, col, self.current_player.symbol):
            sos_count = self.board.check_sos()
            if sos_count > 0:
                self.current_player.score += 1
                if self.game_mode == "Simple":
                    return True
                else:
                    self.extra_turn = True
                    return True
            else:
                self.turns_taken += 1
                if not self.extra_turn:
                    self.switch_turn()
                else:
                    self.extra_turn = False
        return False

    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def check_winner(self):
        if self.game_mode == 'Simple' and self.board.check_sos() > 0:
            return f"{self.current_player.color.capitalize()} Wins!"
        if self.board.is_full():
            return "Tie"
        return None

    def reset_game(self):
        self.board.reset_board()
        self.turns_taken = 0
        self.extra_turn = False

class GameGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.buttons = {}
        self.create_widgets()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=1, column=1, padx=10, pady=10)

        self.score_label = tk.Label(self.root, text="Score: Blue - 0 | Red - 0")
        self.score_label.grid(row=0, column=1, pady=10)

        self.mode_label = tk.Label(self.root, text="Mode: Simple")
        self.mode_label.grid(row=0, column=0)

        self.turn_label = tk.Label(self.root, text="Blue's turn", font=('Arial', 12))
        self.turn_label.grid(row=0, column=2)

        self.mode_var = tk.StringVar(value="Simple")
        self.mode_dropdown = tk.OptionMenu(self.root, self.mode_var, "Simple", "General", command=self.set_game_mode)
        self.mode_dropdown.grid(row=2, column=1, padx=10)

        self.board_size_label = tk.Label(self.root, text="Board Size:")
        self.board_size_label.grid(row=3, column=0, padx=10)
        self.board_size_var = tk.IntVar(value=3)
        self.size_dropdown = tk.OptionMenu(self.root, self.board_size_var, *range(3, 9), command=self.resize_board)
        self.size_dropdown.grid(row=3, column=1, padx=10)

        self.create_grid()

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=4, column=1, pady=10)

        self.player1_label = tk.Label(self.root, text="Player 1 (Blue)")
        self.player1_label.grid(row=1, column=0)
        self.player2_label = tk.Label(self.root, text="Player 2 (Red)")
        self.player2_label.grid(row=1, column=2)

        self.player1_menu = tk.OptionMenu(self.root, tk.StringVar(value="Human"), "Human", "Computer")
        self.player1_menu.grid(row=2, column=0)

        self.player2_menu = tk.OptionMenu(self.root, tk.StringVar(value="Human"), "Human", "Computer")
        self.player2_menu.grid(row=2, column=2)

    def create_grid(self):
        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                button = tk.Button(self.grid_frame, text='', width=10, height=3, command=lambda r=r, c=c: self.cell_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button
        self.update_grid()

    def update_grid(self):
        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                symbol = self.game.board.grid[r][c]
                color = 'black' 
                if symbol == 'S':
                    color = 'blue'
                elif symbol == 'O':
                    color = 'red'
                self.buttons[(r, c)].config(text=symbol, fg=color)
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: Blue - {self.game.player1.score} | Red - {self.game.player2.score}")
        self.turn_label.config(text=f"{self.game.current_player.color.capitalize()}'s turn")

    def set_game_mode(self, mode):
        self.game.game_mode = mode
        self.mode_label.config(text=f"Mode: {mode.capitalize()}")

    def resize_board(self, size):
        self.game.board.size = size
        self.create_grid()

    def cell_click(self, r, c):
        if self.game.board.grid[r][c] == '' and self.game.check_winner() is None:
            self.game.play_turn(r, c)
            self.update_grid()
            winner = self.game.check_winner()
            if winner:
                self.show_winner(winner)

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", winner)
        self.new_game()

    def new_game(self):
        self.game.reset_game()
        self.update_grid()