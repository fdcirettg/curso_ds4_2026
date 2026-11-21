""" Extract text from PDF files using PyMuPDF (fitz) library. """
import argparse
import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
    """
    # Initialize an empty string to hold the extracted text
    extracted_text = ""
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        print(f"=============== ******** Extracting text from: {pdf_path}")
        try:
            # Create a PDF reader object
            pdf_reader = PdfReader(pdf_file)
             # Iterate through each page in the PDF
            for page in pdf_reader.pages:
                # Extract text from the current page and append it to the extracted_text
                extracted_text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error occurred while reading the PDF: {e}")
       
    return extracted_text

def main(arguments):
    """
    Main function to extract text from PDF files.

    Args:
        arguments (list): List of command-line arguments.
    """ 
    pdf_path = arguments.pdf_folder
    pdf_list = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
    texts_list = []
    for pdf in pdf_list:
        pdf_full_path = os.path.join(pdf_path, pdf)
        
        extracted_text = extract_text_from_pdf(pdf_full_path)
        
        texts_list.append(extracted_text)

    # Print the extracted text
    for text in texts_list:
        print(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF files.")
    parser.add_argument("pdf_folder", help="Path to the PDF folder.",
                        default="pdfs")
    args = parser.parse_args()
    main(args)