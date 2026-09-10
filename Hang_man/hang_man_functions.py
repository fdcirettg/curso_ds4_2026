""" Functions for the Hangman game """
from random import choice 

class Hangman:
    """Class to represent the Hangman game."""
    LIVES = 7
    def __init__(self, word_list:list):
        self.board = {}
        self.word_list = word_list
        self.num_lives = self.LIVES
        self.word = choice(self.word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.list_of_guesses = []
    def load_board(self):
        """Load the the game board."""
        for i in range(0, self.LIVES + 1):
            with open(f"board_{i}.txt", "r", encoding="utf-8") as f:
                self.board[i] = f.read()
    def display_board(self):
        """Display the current state of the game board."""
        print(self.board[self.LIVES - self.num_lives])
        print(" ".join(self.word_guessed))
        print(f"Lives remaining: {self.num_lives}")
        print(f"Guessed letters: {', '.join(self.list_of_guesses)}")
    def check_guess(self, guess:str):
        """Check if the guessed letter is in the word."""
        guess = guess.lower() # We make sure the guess is in lowercase to match the word's case
        if guess in self.word:
            print(f"Good guess! {guess} is in the word.")
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.word_guessed[i] = guess
            self.num_letters -= 1
        else:
            print(f"Sorry, {guess} is not in the word.")
            self.num_lives -= 1
        self.list_of_guesses.append(guess)
if __name__ == "__main__":
    list_word = ["python", "java", "javascript", "hangman", "programming"]
    hangman_game = Hangman(list_word)
    hangman_game.load_board()
    hangman_game.check_guess("p")
    hangman_game.display_board()