from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return '<html><head><title>About</title></head><body><h1>About This App</h1><p>This is a simple Flask application that demonstrates the "Hello, World!" concept.</p></body><footer><a href="/">Home</a></footer></html>'

if __name__ == '__main__':
    app.run(debug=True)
