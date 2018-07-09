import os

import functools

from flask import (Blueprint, Flask, send_file, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    from . import db
    db.init_app(app)

    @app.route('/return-file/')
    def return_file():
        print(request.form["sheet_id"])
        return send_file("static/Nutrition_Label_Output.docx", attachment_filename="Nutrition_Label.docx")


    from . import generator
    app.register_blueprint(generator.bp)
    app.add_url_rule('/', endpoint='index')

    return app
