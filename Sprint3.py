import tkinter as tk 
from tkinter import messagebox

# define SOS class
class SOS: 

    def __init__(self, root):

        self.root = root
        self.root.title("SOS Game")

        # initialize game mode to start as simple
        self.game_mode = tk.StringVar(value = 'simple')

        # initialize blue player to start as S and red player to start as O
        self.blue_player = tk.StringVar(value = 'S')
        self.red_player= tk.StringVar(value = 'O')

        # call setup_ui()
        self.user_interface()

        # board_frame is not intialized to anything atm but will be later in the code to 8
        self.board_frame = None

        # call create_board()
        self.create_board()
    
    def user_interface(self):

        # creating radio buttons for simple and general game and placing them on the grid
        tk.Radiobutton(root, text = "Simple Game", variable = self.game_mode, value = 'simple').grid(row = 0, column = 0)
        tk.Radiobutton(root, text = "General Game", variable = self.game_mode, value = 'general').grid(row = 0, column = 2)

        # creating labels for blue and red player and placing them on the grid 
        tk.Label(root, text = "Blue Player").grid(row = 2, column = 0)
        tk.Label(root, text = "Red Player").grid(row = 3, column = 0)

        # creating S and O radio buttons for blue player
        tk.Radiobutton(root, text = "S",variable = self.blue_player, value = 'S').grid(row = 2, column = 1)
        tk.Radiobutton(root, text = "O",variable = self.blue_player, value = 'O').grid(row = 2, column = 2)
        
        # creating S and O radio buttons for red player
        tk.Radiobutton(root, text = "S",variable = self.red_player, value = 'S').grid(row = 3, column = 1)
        tk.Radiobutton(root, text = "O",variable = self.red_player, value = 'O').grid(row = 3, column = 2)

        # creating space labels to make the game design look better
        tk.Label(root, text = "").grid(row = 0, column = 4)
        tk.Label(root, text = "").grid(row = 0, column = 5)

        # creating a label called Board Size for the input box
        tk.Label(root, text = "Board Size").grid(row = 0, column = 6)
        # creating an input box for board size using Entry and placing it on the grid
        self.board_size = tk.StringVar() # making input boxs' text be editable
        self.boardSize = tk.Entry(root, width = 3, borderwidth = 2, textvariable = self.board_size) # not able to put .grid here b/c it makes the ui look weird
        self.boardSize.grid(row = 0, column = 7) # .grid to place the entry box in row 0, column 7 
        
        # set the board size value to be 8 at the start of the game
        self.boardSize.insert(0, "8")
        # creating a space after the input box 
        tk.Label(root, text = "").grid(row = 0, column = 8) # .grid to place the space in row0, column 8

        tk.Button(root, text = "New Game", command = lambda: self.update_board()).grid(row = 2, column = 6) # create a button named newGame and give it a command

    def create_board(self, board_size = 8): #board size is defaulted to 8
        
        if self.board_frame is not None: # if a board exisits or is not null...
            self.board_frame.destroy() # destroy the board
        
        # create the board and place it on the grid
        self.board_frame = tk.Frame(root) # putting .grid here makes the board frame be all over the place 
        # spacer to make the game layout look nice
        tk.Label(root, text = "").grid(row = 6, column = 1) 
        self.board_frame.grid(row = 7, column = 1, columnspan = 3) # .grid to place the frame in row 7, column 1, and have a column span of 3
        
        # adjust the board size based on the board_size
        for x in range(board_size):
            for y in range(board_size):
                # have each square be a button with a width of 3 and a height of 1
                tk.Button(self.board_frame, text = '', width = 3, height = 1).grid(row = x, column = y)
        # create a space to make the board look nice
        tk.Label(root, text = "").grid(row = 8, column = 1) # .grid to place the space lable in row 8, column 1

    def update_board(self): 
        
        # the current value of the board size input box is the value of board_size which is 8
        current_value = int(self.board_size.get())

        # if the current value is greater than or equal to 3, then the board will update based on the current_value
        if current_value >= 3:
            self.create_board(current_value)
            print("Button was clicked", current_value) # testing button so terminal/output will show that the button was clicked by printing message
        else: # if the current value is anything other greater than or equal to 3, then the user will recieve an error message
            messagebox.showerror("Error", "Board size must be > 3") # error message header and error message 

    def player_move():
        pass

    def general_game():
        pass

    def simple_game(): 
        pass
    

if __name__ == "__main__": 
    root = tk.Tk()
    app = SOS(root)
    root.mainloop()


    # RESOURCES USED LISTED BELOW
    # Youtube: https://www.youtube.com/watch?v=YXPyB4XeYLA
    # Website: https://www.geeksforgeeks.org/tic-tac-toe-game-with-gui-using-tkinter-in-python/
    # Youtube: https://www.youtube.com/watch?v=xx0qmpuA-vM
    # Youtube: https://www.youtube.com/watch?v=IJ-iVnN09-8
    # Website: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
    # Sprint 1 & Sprint 2 