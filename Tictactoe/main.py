""" Main module for the Tic Tac Toe game. """
from Gameboard import Gameboard

def get_players():
    """Prompt the user to choose the game mode and return the players."""
    while True:
        mode = input("Choose game mode: 1 for Player vs Computer, 2 for Player vs Player: ")
        mode = mode.strip()
        p = int(mode) if mode.isdigit() else None
        if p in [1,2]:
            return p
        else:
            print("Invalid input. Please enter 1 or 2.")
def main():
    """Main function to run the Tic Tac Toe game."""
    gameboard = Gameboard()
    players = get_players()
    current_player = 'X'
    continue_playing="yes"
    while continue_playing.lower() == "yes":
        gameboard.display_board()
        if players == 1 and current_player == 'O':
            message = gameboard.computer_move(current_player)
        else:
            position = input(f"Player {current_player}, enter your move (1-9): ")
            position = int(position) if position.isdigit() else None
            if position not in range(1, 10):
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            message = gameboard.player_move(current_player, position)
        print(message)
        winner = gameboard.check_winner()
        if winner:
            gameboard.display_board()
            status = {"X": "Player X wins!", "O": "Player O wins!", "-": "It's a draw!"}
            print(status[winner])
            gameboard.update_scoreboard(winner)
            print(f"Scoreboard: {gameboard.scoreboard}")
            continue_playing = input("Do you want to play again? (yes/no): ")
        
            gameboard.reset_board()  # Reset the board for a new game
            
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
