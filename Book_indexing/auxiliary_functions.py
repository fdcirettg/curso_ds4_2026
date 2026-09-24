""" Auxiliary functions for the Hangman game. """
import os


def list_directory_files(directory:str) -> list:
    """List all files in a given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def load_book(file_path:str) -> list:
    """Load a book from a text file and return a list of words."""
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().split()
    return words

def save_words_to_file(word_list:list, file_path:str) -> None:
    """Save a list of words to a text file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for word in word_list:
            file.write(word + '\n')

def clean_list_of_words(word_list:list) -> list:
    """Clean a list of words by removing punctuation and converting to lowercase."""
    cleaned_words = []
    # my code to clean the word list
    for word in word_list[0:]:
        word = word.lower().strip(".,!?;:\"'()[]{}1234567890")
        #print(word)
        cleaned_words.append(word)
    return cleaned_words

def reduce_list_of_words(word_list:list, min_length:int=3) -> list:
    """Reduce a list of words by filtering out words shorter than min_length."""
    reduced_words = [word for word in word_list if len(word) >= min_length]
    word_set = set(reduced_words)  # Remove duplicates
    reduced_words = list(word_set)
    return reduced_words

def count_words(word_list:list) -> dict:
    """Count the occurrences of each word in a list and return a dictionary."""
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

if __name__ == "__main__":
    # Example usage
    book_path = "Dracula.txt"
    words = load_book(book_path)
    print(len(words))
    print(len(words[0]))
    #print(words[0])
    #print(words[:200])
    cleaned_words = clean_list_of_words(words)
    print("Number of words in the cleaned list:", len(cleaned_words))
    reduced_words = reduce_list_of_words(cleaned_words,4)
    
    print(reduced_words)
    word_dict = count_words(cleaned_words)
    # Print the top ten most common words
    top_ten_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top ten most common words:")
    for word, count in top_ten_words:
        print(f"{word}: {count}")
    print("Number of words in the reduced list:", len(reduced_words))
    save_words_to_file(reduced_words, "dracula_words.txt")