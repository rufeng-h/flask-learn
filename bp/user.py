from flask import Blueprint, jsonify
from flask.views import MethodView

from common import ApiResponse
from models import db, User

bp = Blueprint('user', __name__, url_prefix='/user')


class UserView(MethodView):
    def get(self):
        scalars = db.session.scalars(db.select(User))
        return jsonify(ApiResponse.success(scalars.all()))


bp.add_url_rule('', view_func=UserView.as_view('user_view'))
