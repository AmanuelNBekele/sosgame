import unittest
from tkinter import Tk
from ui import SOS  # assuming the main class is in a file named sos_game.py

class TestSOSGame(unittest.TestCase):

    def test_update_board_size(self):
        # Initialize the Tkinter root and SOS game instance
        root = Tk()
        sos_game = SOS(root)

        # Test initial board size
        initial_size = sos_game.game.board.size
        self.assertEqual(initial_size, 8, "Initial board size should be 8.")

        # Update the board size
        sos_game.update_board_size(6)
        
        # Check if the board size is updated correctly
        updated_size = sos_game.game.board.size
        self.assertEqual(updated_size, 6, "Board size should be updated to 6.")

        # Reset the game and check if the board is reset to the new size
        sos_game.reset_game_ui()
        reset_size = sos_game.game.board.size
        self.assertEqual(reset_size, 6, "After resetting the game, the board size should remain 6.")
        
        root.quit()  # Close Tkinter window

    def test_make_move_simple_game(self):
        # Initialize the SOS game
        root = Tk()
        sos_game = SOS(root)
        
        # Make sure the game is set to simple mode
        sos_game.update_game_mode("Simple")
        
        # Make a move for the Blue player at position (0, 0)
        sos_game.cell_clicked(0, 0)
        
        # Check if the symbol was placed correctly
        symbol = sos_game.squares[0][0].cget("text")
        self.assertEqual(symbol, "S", "Blue player should have placed an 'S' symbol at (0, 0).")
        
        # Check if it's now Red's turn
        turn_label = sos_game.turn_label.cget("text")
        self.assertEqual(turn_label, "Red's Turn", "It should be Red player's turn after Blue's move.")
        
        root.quit()  # Close Tkinter window

if __name__ == '__main__':
    unittest.main()