""" Database operations for the movies app """
import os
import csv 

def load_csv_data(file_path)->dict:
    """ Load data from a CSV file and return it as a dictionary of dictionaries """
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data[row['id']] = row
    return data

def create_new_dictionary(data: dict, key_field: str) -> dict:
    """ Create a new dictionary with the specified key field """
    new_dict = {}
    for item in data.values():
        key = item[key_field]
        new_dict[key] = item
    return new_dict

if __name__ == "__main__":
    # Example usage
    stars_file_path = os.path.join(os.path.dirname(__file__), 'movie_database - stars.csv')
    connections_file_path = os.path.join(os.path.dirname(__file__), 'movie_database - connection.csv')

    stars_data = load_csv_data(stars_file_path)
    connections_data = load_csv_data(connections_file_path)

    print("Stars Data:", stars_data['1'])
    print("Connections Data:", connections_data['1'])

    stars_by_name = create_new_dictionary(stars_data, 'stage_name')
    print("Stars by Stage Name:", stars_by_name['Carrie Fisher'])