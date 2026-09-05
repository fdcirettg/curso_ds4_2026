"""Gameboard Module for the Tic Tac Toe game board."""
import random

class Gameboard:
    """Class representing the Tic Tac Toe game board."""
    winning_combinations = [ [1,2,3], [4,5,6], [7,8,9],
                            [1,4,7], [2,5,8], [3,6,9],
                            [1,5,9], [3,5,7] ]
    scoreboard = {"X": 0, "O": 0, "-": 0}  # Initialize the scoreboard
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
    def check_winner(self):
        """Check if there's a winner or if the game is a draw."""
        board = self.board
        for combo in self.winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]]:
                return f"{board[combo[0]]}"
        if all(v in ['X', 'O'] for v in self.board.values()):
            return "-"  # Draw
        return None
    def update_scoreboard(self, player):
        """Update the scoreboard based on the winner."""
        # This method can be implemented to update a scoreboard if needed.
        if player is not None:
            self.scoreboard[player] += 1
    def reset_board(self):
        """Reset the game board for a new game."""
        self.board = {x:str(x) for x in range(1, 10)}

if __name__ == "__main__":
    gameboard = Gameboard()
    gameboard.display_board()
    m = gameboard.player_move('X', 5)
    gameboard.display_board()
    print(m)
    m = gameboard.computer_move('O')
    gameboard.display_board()
    print(m)
    status = {"X": "Player X wins!", "O": "Player O wins!", "-": "It's a draw!", None: "Game continues."}
    result = gameboard.check_winner()
    print(status[result])
