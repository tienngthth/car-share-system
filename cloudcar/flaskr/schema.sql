-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS cars;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE cars (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  make varchar NOT NULL,
  body TEXT NOT NULL,
  colour TEXT NOT NULL,
  seats INTEGER NOT NULL,
  location TEXT NOT NULL,
  cost INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
