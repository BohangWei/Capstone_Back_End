import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('messaging', __name__, url_prefix='/messaging')

@bp.route('/send_message')
def send_message():
    print('Message sent')
    return('Message sent')
