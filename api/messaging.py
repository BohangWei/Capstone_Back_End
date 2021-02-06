import functools
from adaptor import BAAdaptor

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

bp = Blueprint('messaging', __name__, url_prefix='/messaging')
adaptor = BAAdaptor("test")

@bp.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'GET':
        return adaptor.send_message("hello")
    elif request.method == 'POST':
        print('here')
        print(request.form)
        print(request.form.get('value'))
        return('post complete')
