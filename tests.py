import datetime
import json
from unittest import TestCase

from common import ApiResponse
from models import User


class TestSerialize(TestCase):
    def testResponse(self):
        response = ApiResponse.success(User(id=2, username='dsafd'))
        # print(getattr(response, 'sdafas'))
        # print(api_jsonify(response))

    def test_deserialize(self):
        s = '{"code": 200, "message": "\u64cd\u4f5c\u6210\u529f", "data": {"id": 2, "username": "dsafd"}}'
        print(json.loads(s))

    def test_date(self):
        self.assertTrue(isinstance(datetime.datetime.now(), datetime.date))
