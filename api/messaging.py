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

        response = {
            'response': 'this is the response from flask to the message: {}'.format(request.get_json()['value'])
        }
        return(jsonify(response))
