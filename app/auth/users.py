import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request,
    jsonify
)
from app.db import get_db
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)

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
    params = request.get_json()
    user = params['username']
    pwd = params['password']

    #Validate the input
    if not user:
        return {
            'error': 'no username given'
        }
    elif not pwd:
        return {
            'error': 'no password given'
        }

    #Store user into DB
    query_str = 'INSERT INTO user (username, password) VALUES (?, ?)'
    db = get_db()
    db.execute(query_str, (user, generate_password_hash(pwd)))
    db.commit()

    #Return the JWT
    access_token = create_access_token(identity = user)
    return {
        'access_token': access_token
    }

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
    params = request.get_json()
    user = params['username']
    pwd = params['password']
    db = get_db()
    check_user_query = 'SELECT * FROM user WHERE username = ?'

    #Validate the input
    if not user:
        return {
            'error': 'no username given'
        }
    elif not pwd:
        return {
            'error': 'no password given'
        }

    #Make sure the provided credentials match up to a user
    user_matches = db.execute(check_user_query, (user, ))
    user_query_result = user_matches.fetchone()
    if not check_password_hash(user_query_result['password'], pwd):
        return {
            'error': 'incorrect password'
        }

    #Return the JWT
    access_token = create_access_token(identity = user)
    return {
        'access_token': access_token
    }
