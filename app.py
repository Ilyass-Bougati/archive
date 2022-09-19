from crypt import methods
from flask import *
from flask_session import *
from sys import argv
from helpers import *

from secrets import token_hex
TOKEN_LEN = 64

# creating the app
app = Flask(__name__)

# the sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
        # getting the request data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # checking for missing data
        if not username:
            return render_template("register.html", Error="The username is required")
        if not email:
            return render_template("register.html", Error="The email is required")
        if not password:
            return render_template("register.html", Error="The password is required")
        if not confirmation:
            return render_template("register.html", Error="The password confirmation is required")

        # checking if the password confirmation matches the password
        if password != confirmation:
            return render_template("register.html", Error="The password and confirmation doesn't match")

        # connecting to the database
        conn = connect()

        # todo change this later
        # checking if the username is unique
        res = conn.execute("SELECT id FROM users WHERE username=?", [username]).fetchone()
        if res:
            conn.close()
            return render_template("register.html", Error="Username already in use")

        found_token = False
        while not found_token:
            # generatin a token
            token = token_hex(TOKEN_LEN)
            # checking if someone already has the token
            res = conn.execute("SELECT id FROM users WHERE username=?", [username]).fetchone()
            # regenerating token if token already exists
            if not res:
                found_token = True
        

        # creating the user
        # inserting the user and giving session
        conn.execute("INSERT INTO users (username, email, password, token) VALUES(?, ?, ?, ?)", [username, email, Hash(password), token])
        session["token"] = token
        # committing the changes
        conn.commit()
        # closing the connection
        conn.close()
        return redirect("/")



if __name__ == "__main__":
    try:
        debug = argv[1] == "debug"
    except:
        debug = False

    app.run(debug=debug)