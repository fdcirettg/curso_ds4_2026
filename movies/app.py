""" A simple movie database application """
from flask import Flask, render_template 
import movies_sqlite as db

app = Flask(__name__) 


@app.route('/')
def index():
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies;"
    rows = db.retrieve_data_with_query(conn, query)
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True) 
