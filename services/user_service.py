import functools
import sqlite3
from app.db import get_db, close_db
from werkzeug.security import check_password_hash, generate_password_hash

class UserService:

  pass

  def add_new_user(self, username, password, fname, lname):

    db = get_db()

    # add user info to database
    add_user_query = 'INSERT INTO user (username, password, fname, lname) VALUES (?, ?, ?, ?)'
    db.execute(add_user_query, (username, generate_password_hash(password), fname, lname))
    db.commit()

    # get user id
    get_id_query = 'SELECT id FROM user WHERE (username) = (?)'
    get_id_query_result = db.execute(get_id_query, (username,)).fetchone()
    user_id = get_id_query_result['id']

    return user_id
