import unittest
from tkinter import Tk
from ui import SOSGame

class TestSOSGame(unittest.TestCase):

    def test_computer_player_move(self):
        game = SOSGame()
        red_player = game.red_player
        move = red_player.make_move(game.board.board)
        self.assertIsInstance(move, tuple) 

if __name__ == '__main__':
    unittest.main()