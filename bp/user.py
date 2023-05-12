from flask import Blueprint, jsonify, request
from flask.views import MethodView

from common import ApiResponse
from models import db, User

bp = Blueprint('user', __name__, url_prefix='/user')


class UserView(MethodView):
    def get(self):
        scalars = db.session.scalars(db.select(User))
        return jsonify(ApiResponse.success(scalars.all()))

    def post(self):
        """
        手动反序列化，且不支持嵌套
        """
        user = User(**request.json)
        print(user)
        print(type(user.username))
        return jsonify(ApiResponse.success())


bp.add_url_rule('', view_func=UserView.as_view('user_view'))
