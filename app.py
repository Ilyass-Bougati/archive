from crypt import methods
from flask import *
from flask_session import *
from sys import argv
from helpers import *
import os
from werkzeug.utils import secure_filename

# creating the app
app = Flask(__name__)

# creating the data file if it doesn't exist
try:
    os.mkdir("data")
except FileExistsError:
    print("Data file exists")

# upload folder
UPLOAD_FOLDER = os.getcwd() + "/data"
ALLOWED_EXTENSIONS = {'mp4'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# the sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# the main route
@app.route("/")
@login_required
def index():
    return render_template("index.html")


#the login route
@app.route("/login", methods=["GET", "POST"])
@nlogin_required
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":


        # getting the credentials
        username = request.form.get("username")
        password = request.form.get("password")

        # getting the user data
        # Connecting to the database
        conn = connect()
        # getting the data
        res = conn.execute("SELECT * FROM users WHERE username=?", [username]).fetchone()
        print(res)
        # checking if the user exists
        if not res:
            conn.close()
            return render_template("login.html", Error="Password or username incorrect")
        # checking if the passwords match
        if Hash(password) != res[3]:
            conn.close()
            print("password shit")
            return render_template("login.html", Error="Password or username incorrect")
        
        # generating token
        token = generate_token(conn)

        # changing the token in db
        conn.execute("UPDATE users SET token=? WHERE username=?", [token, username])
        session["token"] = token

        # redirect
        return redirect("/")


# The registering route
@app.route("/register", methods=["POST", "GET"])
@nlogin_required
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

        # generating token
        token = generate_token(conn)

        # creating the user
        # inserting the user and giving session
        conn.execute("INSERT INTO users (username, email, password, token) VALUES(?, ?, ?, ?)", [username, email, Hash(password), token])
        session["token"] = token
        # committing the changes
        conn.commit()
        # closing the connection
        conn.close()
        return redirect("/")


# logout route
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect("/")

# the main route (The files route)
@app.route("/files")
@login_required
def files():
    return render_template("files.html")


# The upload page
@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        # getting the data
        file = request.files.get("file")
        filename = request.form.get("filename") + "." + file.filename.split(".")[-1]

        # checking the data
        if not file.filename:
            return render_template("upload.html", Error="You must choose a file")
        if not filename:
            filename = file.filename

        # saving the file
        # getting the user id
        conn = connect()
        user_id = conn.execute("SELECT id FROM users WHERE token=?", [session["token"]]).fetchone()[0]
        user_directory = UPLOAD_FOLDER + f"/{user_id}" 

        # make user directory
        try:
            os.mkdir(user_directory)
        except FileExistsError:
            pass

        # adding the file to the database
        conn.execute("INSERT INTO files (user_id, name) VALUES(?,?)", [user_id, filename])
        file.save(os.path.join(user_directory, secure_filename(filename)))

        #closing connection
        conn.commit()
        conn.close()

        return redirect("/")
        


if __name__ == "__main__":
    try:
        debug = argv[1] == "debug"
    except:
        debug = False

    app.run(debug=debug)