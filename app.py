import os

from flask import Flask, current_app, template_rendered, request_started, request_tearing_down, request_finished, \
    got_request_exception, jsonify
from werkzeug.exceptions import HTTPException

import auth
import blog
import db
from common import ApiResponse


def connect_signal(app):
    @template_rendered.connect_via(app)
    def log_template_rendered(sender, template, context):
        current_app.logger.info(f'{template} rendered with {context}, the sender is {sender}')

    @request_started.connect_via(app)
    def request_start(sender):
        current_app.logger.info(f'request started, the sender is {sender}')

    @request_tearing_down.connect_via(app)
    def tear_down(sender, exc=None):
        current_app.logger.info(f'request tear down {exc}, the sender is {sender}')

    @request_finished.connect_via(app)
    def req_finished(sender, response):
        current_app.logger.info(f'request finished {response}, the sender is {sender}')

    @got_request_exception.connect_via(app)
    def req_exp(sender, exception):
        current_app.logger.info(f'request exception {exception.args}, the sender is {sender}')

    def exp_func():
        raise ValueError('')

    app.add_url_rule('/exp', view_func=exp_func)


def init_datasource(app):
    db.init_app(app)


def add_url_mapping(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    db.init_app(app)
    app.add_url_rule('/', endpoint='index')


def add_error_handler(app: Flask):
    @app.errorhandler(Exception)
    def handle_all(exp):
        current_app.logger.error('服务器异常', exp)
        return ApiResponse.server_error()
    jsonify

    @app.errorhandler(HTTPException)
    def handle_http(exp):
        current_app.logger.error('Http异常', exp)
        return ApiResponse.server_error()


def config_app(app, test_config=None):
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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    config_app(app, test_config)
    init_datasource(app)
    add_url_mapping(app)
    connect_signal(app)
    add_error_handler(app)
    return app


if __name__ == '__main__':
    create_app().run()
