import functools
import sqlite3
from app.db import get_db, close_db
from werkzeug.security import check_password_hash, generate_password_hash

class UserService:

  pass

  def add_new_user(self, username, password):

    db = get_db()

    # add user info to database
    query_str = 'INSERT INTO user (username, password) VALUES (?, ?)'
    db.execute(query_str, (username, generate_password_hash(password)))
    db.commit()



  