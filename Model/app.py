from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "Hello <h1> Home Page</h1>"

