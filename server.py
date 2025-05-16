import datetime
from flask import Flask
from flask import render_template

from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html')

    # run the application
if __name__ == "__main__":
    app.run(debug=True)
