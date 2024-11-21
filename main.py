import tkinter as tk
from ui import Player
from ui import Game
from ui import GameGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SOS Game")

    player1 = Player(symbol = 'S', player_type = 'Human', color ='blue')
    player2 = Player(symbol = 'O', player_type = 'Human', color = 'red')

    game = Game(player1, player2)

    gui = GameGUI(root, game)
    root.mainloop()