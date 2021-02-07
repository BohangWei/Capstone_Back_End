import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request,
    jsonify
)
from app.db import get_db

bp = Blueprint('users', __name__, url_prefix='/user')

"""
This is the POST request handler for registering a new user in the database.

Parameters (expected in JSON format in request body):
    {
        username: [string],
        password: [string]
    }

Returns:
    JWT if success, if error:
        {
        error: [reason in string format]
        }
"""
@bp.route('/register', methods = ['POST'])
def register():
    pass

"""
This is the POST request for logging a user in and obtaining the JWT.

Parameters (expected in JSON format in request body):
    {
        username: [string],
        password: [string]
    }

Returns:
    JWT if success, if error:
        {
        error: [reason in string format]
        }
"""
@bp.route('/login', methods = ['POST'])
def login():
    pass
