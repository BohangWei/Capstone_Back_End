from flask import Flask
from flask_cors import CORS
import app.api as api
import app.auth as auth
from . import db
import os
from flask_jwt_extended import JWTManager

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    jwt_manager = JWTManager(app)

    #Add configuration values
    app.config.from_mapping(
        SECRET_KEY = 'dev', #Secret key, should be replaced with something random for more security
        DATABASE = os.path.join(app.instance_path, 'binder.sqlite') #Database path
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app) #Add the callbacks for db connection setup and teardown

    app.register_blueprint(api.messaging.bp) #Register the messaging endpoints blueprint
    app.register_blueprint(auth.users.bp) #Register the user endpoints blueprint

    CORS(app)
    return app
