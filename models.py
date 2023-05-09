from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, DateTime, func

from common import Serializable

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class User(db.Model, Serializable):
    exclude_fields = ('password',)
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(32), nullable=False, server_default='')
    password = Column(String(64), nullable=False, server_default='123456')
    birth_date = Column(Date, nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
