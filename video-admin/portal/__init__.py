import os

from flask import Flask, redirect
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from flask.json import jsonify
from requests import Response

import portal.database.DBConnection as DBConn
from portal.app.Data.Models import *
from portal.app.Exceptions.APIException import APIException


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(os.path.abspath('./Environment.py'))
    app.config['SQLALCHEMY_DATABASE_URI'] = DBConn.connect_url
    app.config['MAX_CONTENT_LENGTH'] = 150 * 1000 * 1000
    migrate = Migrate(app, DBConn.db, render_as_batch=True)

    @migrate.configure
    def configure_alembic(config):
        # modify config object
        return config

    DBConn.db.init_app(app)
    CORS(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import video_router
    from .routes import playlist_router
    from .routes import schedule_router

    app.register_blueprint(video_router, url_prefix='/video')
    app.register_blueprint(playlist_router, url_prefix='/playlist')
    app.register_blueprint(schedule_router, url_prefix='/schedule')
    

    @app.errorhandler(APIException)
    def handle_invalid_usage(error: APIException):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return
    
    @app.route('/', methods=['GET'])
    def index() -> Response:
        return redirect('/schedule/?page=1&per_page=10&relationships=playlist&relationships=videos')

    return app
