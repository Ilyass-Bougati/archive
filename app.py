from crypt import methods
from flask import *
from sys import argv
from helpers import login_required

# creating the app
app = Flask(__name__)



# the main route
@app.route("/")
@login_required
def index():
    return "Hello world"


#the login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        return "post"


# The registering route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")


    elif request.method == "POST":
        return "post"


if __name__ == "__main__":
    try:
        debug = argv[1] == "debug"
    except:
        debug = False

    app.run(debug=debug)