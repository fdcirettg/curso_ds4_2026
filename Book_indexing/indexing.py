""" Indexing functions for the book database. """
import argparse
import os
from auxiliary_functions import list_directory_files, load_book, clean_list_of_words, reduce_list_of_words, count_words   

def main(args):
    book_path = args.book_path
    book_dictionary = {}
    if not os.path.exists(book_path):
        print(f"Error: The path '{book_path}' does not exist.")
        return
    if os.path.isfile(book_path):
        # If it's a single file, process it directly
        book_dictionary[book_path] = load_book(book_path)
    elif os.path.isdir(book_path):
        # If it's a directory, list all text files and process them
        files = list_directory_files(book_path)
        for file in files:
            if file.endswith('.txt'):
                book_dictionary[file] = load_book(os.path.join(book_path, file))
    else:
        print(f"Error: The path '{book_path}' is neither a file nor a directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index books.")
    parser.add_argument("book_path", type=str, help="Path to the books text files.")
    args = parser.parse_args()
    main(args)