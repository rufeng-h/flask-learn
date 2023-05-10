import dataclasses
import datetime
import decimal
import typing
import uuid

from flask import Flask, current_app, template_rendered, request_started, request_tearing_down, request_finished, \
    got_request_exception, jsonify
from werkzeug.exceptions import HTTPException

from common import ApiResponse, Serializable
from models import init_db


def connect_signal(app):
    @template_rendered.connect_via(app)
    def log_template_rendered(sender, template, context):
        current_app.logger.info(f'{template} rendered with {context}, the sender is {sender}')

    @request_started.connect_via(app)
    def request_start(sender):
        current_app.logger.info(f'request started, the sender is {sender}')

    @request_tearing_down.connect_via(app)
    def tear_down(sender, *, exc=None):
        current_app.logger.info(f'request tear down {exc}, the sender is {sender}')

    @request_finished.connect_via(app)
    def req_finished(sender, response):
        current_app.logger.info(f'request finished {response}, the sender is {sender}')

    @got_request_exception.connect_via(app)
    def req_exp(sender, exception):
        current_app.logger.info(f'request exception {exception.args}, the sender is {sender}')


def init_datasource(app):
    init_db(app)


def add_url_mapping(app):
    @app.route('/')
    def index():
        return jsonify(ApiResponse.success())

    from bp import user

    app.register_blueprint(user.bp)


def add_error_handler(app: Flask):
    @app.errorhandler(Exception)
    def handle_all(exp):
        current_app.logger.error(exp)
        return jsonify(ApiResponse.server_error())

    @app.errorhandler(HTTPException)
    def handle_http(exp):
        current_app.logger.error(exp)
        print(dir(exp))
        return jsonify(ApiResponse.server_error())

    pass


def config_app(app, test_config=None):
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    def default(o: typing.Any) -> typing.Any:
        if isinstance(o, Serializable):
            return dict(o)

        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, "%Y-%m-%d %H:%M:%S")

        if isinstance(o, datetime.date):
            return datetime.date.strftime(o, '%Y-%m-%d')

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if hasattr(o, "__html__"):
            return str(o.__html__())

        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

    app.json.default = default
    app.json.ensure_ascii = False
    app.json.sort_keys = False
    app.json.compact = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


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
