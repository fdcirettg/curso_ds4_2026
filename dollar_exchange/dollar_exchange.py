"""
Dollar Exchange page scrapper
"""
import os
import requests
import argparse

def scrap_web_page(url:str) -> str:
    """Scrap the content of a web page and return the text."""
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve the web page. Status code: {response.status_code}")

def main(args):
    """Main function to scrap the web page and save the content to a file."""
    url = args.url
    output_file = args.output_file
    try:
        content = scrap_web_page(url)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Web page content saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap a web page and save its content to a file.")
    parser.add_argument("url", type=str, help="The URL of the web page to scrap.")
    parser.add_argument("output_file", type=str, help="The output file to save the content.")
    args = parser.parse_args()
    main(args)
