""" Functions for the Hangman game """
import os
from pathlib import Path
from random import choice
import argparse
# for textual interface
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Static

def load_words(file_path: str) -> list:
    """Load words from a file and return them as a list."""
    with open(file_path, "r", encoding="utf-8") as f:
        words = f.read().splitlines()
    return words

class Hangman:
    """Class to represent the Hangman game."""
    LIVES = 7

    def __init__(self, word_list:list):
        self.board = {}
        self.word_list = word_list
        self.reset_game()

    def reset_game(self):
        """Reset the game state with a new random word."""
        self.num_lives = self.LIVES
        self.word = choice(self.word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.list_of_guesses = []

    def current_board_index(self):
        """Return the current board stage based on failed attempts."""
        return self.LIVES - self.num_lives

    def load_board(self):
        """Load the the game board."""
        board_dir = Path(__file__).parent
        for i in range(0, self.LIVES + 1):
            file_path = os.path.join(board_dir, f"board_{i}.txt")
            with open(file_path, "r", encoding="utf-8") as f:
                self.board[i] = f.read()
                
    def display_board(self):
        """Display the current state of the game board."""
        print(self.board[self.current_board_index()])
        print(" ".join(self.word_guessed))
        print(f"Lives remaining: {self.num_lives}")
        print(f"Guessed letters: {', '.join(self.list_of_guesses)}")

    def refresh_view(self, message: str | None = None):
        """Render the current terminal state of the game."""
        self.display_board()
        if message is not None:
            print(message)

    def game_won(self):
        """Return True when the player has guessed the entire word."""
        return (self.num_letters == 0)

    def game_lost(self):
        """Return True when the player has no lives left."""
        return (self.num_lives == 0)

    def check_guess(self, guess:str):
        """Check if the guessed letter is in the word."""
        guess = guess.strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            return "Invalid input. Please enter a single alphabetical character."
        if guess in self.list_of_guesses:
            return f"You have already guessed '{guess}'. Try a different letter."
        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.word_guessed[i] = guess
            self.num_letters -= 1
            message = f"Good guess! '{guess}' is in the word."
        else:
            self.num_lives -= 1
            message = f"Sorry, '{guess}' is not in the word."
        self.list_of_guesses.append(guess)
        return message

    def submit_guess(self, guess: str):
        """Apply a terminal guess and return the resulting message."""
        message = self.check_guess(guess)
        if self.game_won():
            message += "\nCongratulations! You've guessed the word!"
        elif self.game_lost():
            message += f"\nGame over! The word was '{self.word}'."
        return message

    def restart_game(self):
        """Restart the terminal game."""
        self.reset_game()
        self.refresh_view("Game restarted! A new word has been chosen.")

    def play(self):
        """Run the hangman game loop in the terminal."""
        self.refresh_view("Try to guess the word! type a letter and press enter.")
        while True:
            guess = input("Enter a letter: ")
            message = self.submit_guess(guess)
            self.refresh_view(message)
            if not (self.game_won() or self.game_lost()):
                continue
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            if play_again == 'y':
                self.restart_game()
                continue
            break

class _Hangman(App[None], Hangman):
    """Class to represent the Hangman game with a Textual interface."""
    CSS = """
    Screen {
        align: center middle;
    }

    #board-container {
        width: 60;
        height: auto;
        padding: 1 4;
        border: round $accent;
    }

    #board-art {
        content-align: center middle;
        text-align: center;
        text-style: bold;
        color: $warning;
        height: 8;
    }

    #word-line {
        content-align: center middle;
        text-align: center;
        text-style: bold;
        padding-top: 1;
    }

    #lives-line, #guesses-line {
        content-align: center middle;
        text-align: center;
        padding-top: 1;
    }

    #message-line {
        content-align: center middle;
        text-align: center;
        padding-top: 1;
        color: $accent;
    }

    #guess-row {
        width: 100%;
        height: auto;
        padding-top: 1;
    }

    #guess-input {
        width: 1fr;
    }

    #guess-button {
        margin-left: 1;
    }
    """

    def __init__(self, word_list:list):
        App.__init__(self)
        Hangman.__init__(self, word_list)
        self.load_board()

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "restart_game", "Restart"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the UI elements for the Hangman game."""
        yield Header()
        with Vertical(id="board-container"):
            yield Static(self.board[self.current_board_index()], id="board-art")
            yield Static(" ".join(self.word_guessed), id="word-line")
            yield Static(f"Lives remaining: {self.num_lives}", id="lives-line")
            yield Static("Type a letter and press Enter.", id="message-line")
            with Horizontal(id="guess-row"):
                yield Input(placeholder="Type a letter", max_length=1, id="guess-input")
                yield Button("Guess", id="guess-button", variant="primary")
            yield Static(
                f"Guessed letters: {', '.join(self.list_of_guesses)}",
                id="guesses-line",
            )
        yield Footer()

    def on_mount(self) -> None:
        """Refresh the board once the widgets are mounted."""
        self.refresh_view("Type a letter and press Enter.")
        self.query_one("#guess-input", Input).focus()

    def refresh_view(self, message: str | None = None) -> None:
        """Refresh the Textual widgets with the current game state."""
        self.query_one("#board-art", Static).update(self.board[self.current_board_index()])
        self.query_one("#word-line", Static).update(" ".join(self.word_guessed))
        self.query_one("#lives-line", Static).update(
            f"Lives remaining: {self.num_lives}"
        )
        guessed_letters = ", ".join(self.list_of_guesses) or "None"
        self.query_one("#guesses-line", Static).update(
            f"Guessed letters: {guessed_letters}"
        )
        if message is not None:
            self.query_one("#message-line", Static).update(message)

    def submit_guess(self) -> None:
        """Read the current input, apply the guess, and refresh the board."""
        input_widget = self.query_one("#guess-input", Input)
        guess = input_widget.value
        input_widget.value = ""

        message = self.check_guess(guess)
        if self.game_won():
            message = f"You won! The word was {self.word}. Press r to play again."
            input_widget.disabled = True
            self.query_one("#guess-button", Button).disabled = True
        elif self.game_lost():
            message = f"Game over. The word was {self.word}. Press r to play again."
            input_widget.disabled = True
            self.query_one("#guess-button", Button).disabled = True

        self.refresh_view(message)
        if not input_widget.disabled:
            input_widget.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter on the input widget."""
        if event.input.id == "guess-input":
            self.submit_guess()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "guess-button":
            self.submit_guess()

    def action_restart_game(self) -> None:
        """Restart the game from the keyboard binding."""
        self.reset_game()
        input_widget = self.query_one("#guess-input", Input)
        input_widget.disabled = False
        self.query_one("#guess-button", Button).disabled = False
        self.refresh_view("Type a letter and press Enter.")
        input_widget.focus()

if __name__ == "__main__":
    # Example usage
    parser = argparse.ArgumentParser(description="Play Hangman in the terminal.")
    parser.add_argument("--word_file", "-w", type=str, default="word_list_prog.txt", help="Path to the word list file.")
    parser.add_argument(
        "--textual",
        action="store_true",
        help="Run the Hangman game with a Textual interface.",
    )
    parser.add_argument(
        "--terminal",
        action="store_true",
        help="Run the Hangman game in the terminal.",
    )
    args = parser.parse_args()
    word_list = load_words(args.word_file)
    if args.textual:
        hangman_app = _Hangman(word_list)
        hangman_app.run()
    elif args.terminal:
        hangman_game = Hangman(word_list)
        hangman_game.load_board()
        hangman_game.play()