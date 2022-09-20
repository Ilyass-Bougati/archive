CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    token TEXT UNIQUE
);


CREATE TABLE files(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);