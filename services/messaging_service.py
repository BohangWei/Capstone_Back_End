import functools
import sqlite3
from app.db import get_db, close_db


class MessagingService:

  pass
  
  def start_conversation(self, user_id):

    db = get_db()

    # start conversation for new user
    convo_query = 'INSERT INTO conversation (user) VALUES (?)'
    db.execute(convo_query, (user_id,))
    db.commit()

    # get c_id for new user
    get_convo_id_query = 'SELECT c_id FROM conversation WHERE (user) = (?)'
    convo_id_query_result = db.execute(get_convo_id_query, (user_id,)).fetchone()
    c_id = convo_id_query_result['c_id']

    # add initial binder message to new conversation
    message_query = 'INSERT INTO message VALUES (?, ?, ?, ?)'
    db.execute(message_query, (1, c_id, "Hello! How can I help you?", "binder"))
    db.commit()





