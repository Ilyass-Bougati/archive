from flask import *
from sys import argv

# creating the app
app = Flask(__name__)

# the main route
@app.route("/")
def index():
    return "Hello world"

if __name__ == "__main__":
    try:
        debug = argv[1] == "debug"
    except:
        debug = False

    app.run(debug=debug)