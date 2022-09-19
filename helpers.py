from flask import *
from functools import wraps
import sqlite3
from hashlib import sha256
from secrets import token_hex
TOKEN_LEN = 64

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("token") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def nlogin_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("token"):
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def connect(path="archive.db"):
    try:
        conn = sqlite3.connect(path)

    except sqlite3.Error as err:
        print(err)
        conn = None
    
    return conn

def Hash(text):
    return sha256(str(text).encode()).hexdigest()

def generate_token(conn):
    found_token = False
    while not found_token:
        # generatin a token
        token = token_hex(TOKEN_LEN)
        # checking if someone already has the token
        res = conn.execute("SELECT id FROM users WHERE token=?", [token]).fetchone()
        # regenerating token if token already exists
        if not res:
            found_token = True

    return token