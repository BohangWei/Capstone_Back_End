import functools
from adaptor import BAAdaptor

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request,
    jsonify
)

bp = Blueprint('messaging', __name__, url_prefix='/messaging')
adaptor = BAAdaptor("test")

@bp.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'GET':
        return adaptor.send_message("hello")
    elif request.method == 'POST':
        print(request.get_json())

        #Authenticate the user

        #Save the incoming message to their convo history in DB

        #Send the incoming message on to the adaptor class

        #Get the returned value from the adaptor class and forward it back to the React app

        response = {
            'response': 'this is the response from flask to the message: {}'.format(request.get_json()['value'])
        }
        return(response)
