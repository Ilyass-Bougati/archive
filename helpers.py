from flask import *
from functools import wraps
import sqlite3
from hashlib import sha256


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

def connect(path="archive.db"):
    try:
        conn = sqlite3.connect(path)

    except sqlite3.Error as err:
        print(err)
        conn = None
    
    return conn

def Hash(text):
    return sha256(str(text).encode()).hexdigest()