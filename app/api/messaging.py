import functools
import sqlite3
from adaptor import BAAdaptor
from flask_jwt_extended import (
    jwt_required, jwt_optional, get_jwt_identity
)
from app.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request,
    jsonify
)

bp = Blueprint('messaging', __name__, url_prefix='/messaging')
adaptor = BAAdaptor("test")

"""
This is the endpoint to which the frontend will send messages written by the user.
"""
@bp.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'GET':
        return adaptor.send_message("hello")
    elif request.method == 'POST':
        print(request.get_json())

        #Save the incoming message to their convo history in DB

        #Send the incoming message on to the adaptor class

        #Get the returned value from the adaptor class and forward it back to the React app

        response = {
            'response': 'this is the response from flask to the message: {}'.format(request.get_json()['value'])
        }
        return(response)

"""
This is the endpoint to be called when the frontend is rendering the chatbox
for a logged in user. It will return the message history for that user, which
can then be rendered into the chat box.

Parameters:
    JWT in the header, plus query string of following format: "?c_id=[conversation id]"

Returns:
    A JSON response of all the messages in the message history, in order
"""
@bp.route('/load_conversation', methods = ['GET'])
@jwt_required
def load_conversation():
    db = get_db()
    username = get_jwt_identity()
    c_id = request.args.get('c_id')

    #Query the user's conversation and get all the messages in this conversation
    query_str = "SELECT * FROM conversation, message WHERE conversation.c_id = ? AND message.c_id = conversation.c_id"
    query_result = db.execute(query_str, (c_id, )).fetchall()
    messages = [{'msg_txt': row['txt'], 'msg_sender': row['sender'], 'msg_no': row['msg_no']} for row in query_result]
    messages.sort(key = lambda x: x['msg_no']) #Sort in ascending order by message number

    return jsonify({
        'messages': messages
    })

"""
This is the endpoint through which the frontend can get all the conversation
IDs associated with a user to be used in a successive request to the /load_conversation
endpoint to actually populate that conversation to the message box
"""
@bp.route('/get_c_ids', methods = ['GET'])
@jwt_required
def get_c_ids():
    db = get_db()
    username = get_jwt_identity()

    #Query the user's conversations from the database
    query_str = "SELECT c_id FROM user, conversation WHERE user.username = ? AND user.id = conversation.user"
    query_result = db.execute(query_str, (username, )).fetchall()

    c_ids = [row['c_id'] for row in query_result]

    return(jsonify(c_ids))
