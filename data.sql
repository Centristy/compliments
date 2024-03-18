CREATE DATABASE compliments

\c compliments


CREATE TABLE users
(
    username TEXT UNIQUE PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);
