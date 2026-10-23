""" Database operations for the movies app with SQLite 
"""
import sqlite3
import os
import csv
import pandas as pd

def load_csv_data(file_path)->dict:
    """ Load data from a CSV file and return it as a dictionary of dictionaries """
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data[row['id']] = row
    return data

def create_database(db_path: str):
    """ Create a new SQLite database and return the connection """
    conn = sqlite3.connect(db_path)
    return conn

def open_database(db_path: str):
    """ Open an existing SQLite database and return the connection """
    conn = sqlite3.connect(db_path)
    return conn

def create_table(conn, create_table_sql: str):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_insert_statement(table_name: str, data: dict) -> str:
    """ Create an SQL INSERT statement for the given table and data """
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return sql

def insert_data(conn, table_name: str, data: dict):
    """ Insert data into the specified table """
    sql = create_insert_statement(table_name, data)
    cur = conn.cursor()
    cur.execute(sql, tuple(data.values()))
    conn.commit()

def load_csv_to_database(conn, table_name: str, csv_file_path: str):
    """ Load data from a CSV file and insert it into the specified table in the database """
    data = load_csv_data(csv_file_path)
    for item in data.values():
        insert_data(conn, table_name, item)
    print(f"Data from {csv_file_path} loaded into {table_name} table.")

def retrieve_data(conn, table_name: str) -> list:
    """ Retrieve all data from the specified table """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    return rows

def retrieve_data_with_query(conn, query: str) -> list:
    """ Retrieve data from the database using a custom SQL query """
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def show_rows(rows: list):
    """ Print the rows retrieved from the database as a table """
    df = pd.DataFrame(rows)
    print(df)

def close_database(conn):
    """ Close the database connection """
    conn.close()

def main():
    # Example usage
    db_path = os.path.join(os.path.dirname(__file__), 'movies.db')
    conn = create_database(db_path)

    # Create tables (example SQL statements)
    create_table_sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    create_table(conn, create_table_sql_users)

    create_table_sql_stars = """
    CREATE TABLE IF NOT EXISTS stars (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        stage_name TEXT NOT NULL,
        real_name TEXT,
        date_of_birth TEXT,
        place_of_birth TEXT,
        image_url TEXT,
        username TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """
    create_table(conn, create_table_sql_stars)

    create_table_sql_connections = """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        movie_id INTEGER NOT NULL,
        star_id INTEGER NOT NULL,
        role TEXT,
        FOREIGN KEY (star_id) REFERENCES stars (id),
        FOREIGN KEY (movie_id) REFERENCES movies (id)
    );
    """
    create_table(conn, create_table_sql_connections)
    create_table_sql_movies = """
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        movie_title TEXT NOT NULL,
        release_date TEXT,
        poster_url TEXT,
        username TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """
    create_table(conn, create_table_sql_movies)

    # show the tables in the database
    tables = retrieve_data_with_query(conn, "SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables in the database:")
    show_rows(tables)
    # Load data from CSV files into the database
    tables_dictionary = {
        'users': 'movie_database - users.csv',
        'movies': 'movie_database - movies.csv',
        'stars': 'movie_database - stars.csv',
        'connections': 'movie_database - connection.csv'
    }
    for table_name, csv_file in tables_dictionary.items():
        csv_file_path = os.path.join(os.path.dirname(__file__), csv_file)
        rows = retrieve_data(conn, table_name)
        if not rows:  # Only load data if the table is empty
            load_csv_to_database(conn, table_name, csv_file_path)




    # Retrieve and show data
    users_rows = retrieve_data(conn, 'users')
    print("Users Data:")
    show_rows(users_rows)

    movies_rows = retrieve_data(conn, 'movies')
    print("Movies Data:")
    show_rows(movies_rows)

    stars_rows = retrieve_data(conn, 'stars')
    print("Stars Data:")
    show_rows(stars_rows)

    connections_rows = retrieve_data(conn, 'connections')
    print("Connections Data:")
    show_rows(connections_rows)

    stars_rows = retrieve_data_with_query(conn, "SELECT real_name, date_of_birth FROM stars WHERE stage_name = 'Carrie Fisher';")
    print("Carrie Fisher Data:")
    show_rows(stars_rows)

    movies_rows = retrieve_data_with_query(conn, "SELECT movie_title, release_date FROM movies WHERE movie_title LIKE '%alice%';")
    print("Movies with 'alice' in the title:")
    show_rows(movies_rows)
    close_database(conn)


if __name__ == "__main__":
    main()
