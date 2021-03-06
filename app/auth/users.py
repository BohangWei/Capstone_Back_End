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
from services import MessagingService
from services import UserService

bp = Blueprint('users', __name__, url_prefix='/user')
messaging_service = MessagingService()
user_service = UserService()

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
    user = request.json.get('username', None)
    pwd = request.json.get('password', None)

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
    user_service.add_new_user(user, pwd)

    #Initialize conversation in DB
    messaging_service.start_conversation(user)

    #Return the JWT
    access_token = create_access_token(identity = user, expires_delta = False)
    resp = jsonify({
        'access_token': access_token
    })
    return resp

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
    user = request.json.get('username', None)
    pwd = request.json.get('password', None)
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
    user_matches_result = user_matches.fetchone()
    if not user_matches_result:
        return {
            'error': 'incorrect username'
        }
    elif not check_password_hash(user_matches_result['password'], pwd):
        return {
            'error': 'incorrect password'
        }

    #Return the JWT
    access_token = create_access_token(identity = user, expires_delta = False)
    resp = jsonify({
        'access_token': access_token
    })
    return resp

@bp.route('/uname', methods = ['GET'])
@jwt_required()
def uname():
    return jsonify({
        'uname': get_jwt_identity()
    })
