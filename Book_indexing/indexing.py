""" Indexing functions for the book database. """
import argparse
import os
import math
import itertools

from auxiliary_functions import list_directory_files, load_book, clean_list_of_words, reduce_list_of_words, count_words   

def compute_tf(word_count, total_words):
    """ Compute the term frequency (TF) for a word in a document. """
    if total_words == 0:
        return {}
    dict_tf = {}
    for word, count in word_count.items():
        dict_tf[word] = count / total_words
    return dict_tf

def compute_idf(documents):
    '''
        Compute the Inverse Document Frequency (IDF) for each word in the documents.
        usage: idf = compute_idf(list_of_dictionaries)
    '''
    N = len(documents)
    idf_dictionary = dict.fromkeys(documents[0].keys(),0)
    print("Dictionary length:",len(idf_dictionary))
    
    dictionary_list = [list(dictionary.keys()) for dictionary in documents]
    key_list = list(itertools.chain(*dictionary_list))
    print("List length:",len(key_list))
    idf_dictionary = dict.fromkeys(key_list,0)
    print("Dictionary length:",len(idf_dictionary))
    for dictionary in documents:
        for word, valor in dictionary.items():
            if valor > 0:
                if word in idf_dictionary:
                    idf_dictionary[word] += 1
                else:
                    idf_dictionary[word] = 1
    for word, valor in idf_dictionary.items():
        idf_dictionary[word] = math.log(N/float(valor))
    return idf_dictionary

def compute_tf_idf(tf:dict, idfs:dict) -> dict:
    '''
        Computes Term-Frequency-Inverse Document Frequency (TF-IDF) for all documents.
        usage: tfidf_book = compute_tf_idf(book_tf, idfs)
        Returns a dictionary with the TF-IDF of the book.
        Computes Term-Frequency-Inverse Document Frequency
        for all documents
        usage: tfidf_book = compute_tf_idf(book_tf, idfs)
        Returns a dictionary with the TF-IDF of the book.
    '''
    tfidf = dict()
    for word, value in tf.items():
        tfidf[word] = value * idfs[word]
    return tfidf

def book_indexing(dictionary_of_books:dict) -> dict:
    """ Indexes the books and computes TF, IDF, and TF-IDF. """
    tf_dict = {}
    for book_name, words in dictionary_of_books.items():
        cleaned_words = clean_list_of_words(words)
        word_count = count_words(cleaned_words)
        total_words = len(cleaned_words)
        tf_dict[book_name] = compute_tf(word_count, total_words)

    idf_dict = compute_idf(list(tf_dict.values()))

    tfidf_dict = {}
    for book_name, tf in tf_dict.items():
        tfidf_dict[book_name] = compute_tf_idf(tf, idf_dict)

    return tfidf_dict


def main(args):
    """ Main function to index books. """
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
    print(book_dictionary.keys())
    tfidf_dict = book_indexing(book_dictionary)
    print("TF-IDF Dictionary:", tfidf_dict.keys())
    D = tfidf_dict["Dracula.txt"]
    print("TF-IDF for 'Dracula.txt':")
    if "dracula" in D:
        print(f"TF-IDF for 'dracula': {D['dracula']}")
    """
    for book_name, words in book_dictionary.items():
        cleaned_words = clean_list_of_words(words)
        word_count = count_words(cleaned_words)
        total_words = len(cleaned_words)
        tf_dict = compute_tf(word_count, total_words)
        print(f"Book: {book_name}")
        print(f"Total words: {total_words}")
        print(f"Unique words: {len(word_count)}")
        print(f"Term Frequencies:")
        for word, tf in tf_dict.items():
            if tf >=0.0001:  # Only print words with a non-zero frequency
                print(f"  {word}: {tf:.4f}")
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index books.")
    parser.add_argument("book_path", type=str, help="Path to the books text files.")
    args = parser.parse_args()
    main(args)