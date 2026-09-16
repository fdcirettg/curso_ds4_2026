""" Auxiliary functions for the Hangman game. """

def load_book(file_path:str) -> list:
    """Load a book from a text file and return a list of words."""
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().split()
    return words

if __name__ == "__main__":
    # Example usage
    book_path = "Dracula.txt"
    words = load_book(book_path)
    print(len(words))
    print(len(words[0]))
    print(words[0])
    print(words[:200])