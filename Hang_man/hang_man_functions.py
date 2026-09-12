""" Functions for the Hangman game """
import os
from pathlib import Path
from random import choice
import argparse

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

if __name__ == "__main__":
    # Example usage
    word_list = load_words("word_list_prog.txt")
    game = Hangman(word_list)
    game.load_board()
    game.play()
