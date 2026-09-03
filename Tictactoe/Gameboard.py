"""Gameboard Module for the Tic Tac Toe game board."""
import random

class Gameboard:
    """Class representing the Tic Tac Toe game board."""
    def __init__(self):
        self.board = {x:str(x) for x in range(1, 10)}  # Initialize the board with positions 1-9
    def display_board(self):
        """Display the current state of the game board."""
        b = self.board
        print("\n")
        print(f"{b[1]} | {b[2]} | {b[3]}")
        print("--+---+--")
        print(f"{b[4]} | {b[5]} | {b[6]}")
        print("--+---+--")
        print(f"{b[7]} | {b[8]} | {b[9]}")
        print("\n")
    def player_move(self, player,position):
        """Update the board with the player's move."""
        if self.board[position] not in ['X', 'O']:
            self.board[position] = player
            message = f"Player {player} placed on position {position}."
        else:
            message = "Position already taken. Invalid move."
        return message
    def computer_move(self, player):
        """Randomly select an empty position for the computer's move."""
        position = random.choice([k for k, v in self.board.items() if v not in ['X', 'O']])
        message = self.player_move(player, position)
        return message

if __name__ == "__main__":
    gameboard = Gameboard()
    gameboard.display_board()
    m = gameboard.player_move('X', 5)
    gameboard.display_board()
    print(m)
    m = gameboard.computer_move('O')
    gameboard.display_board()
    print(m)
