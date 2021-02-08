CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE conversation (
  c_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user INTEGER NOT NULL,
  FOREIGN KEY (user) REFERENCES user(username)
);

CREATE TABLE message (
  msg_no INTEGER NOT NULL,
  c_id INTEGER NOT NULL,
  txt TEXT NOT NULL,
  sender TEXT NOT NULL,
  PRIMARY KEY (c_id, msg_no),
  FOREIGN KEY (c_id) REFERENCES conversation(c_id)
);
