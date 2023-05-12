import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, DateTime, func
from sqlalchemy.orm import Mapped

from common import Serializable

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class User(db.Model, Serializable):
    _exclude_fields = ('password',)
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str] = Column(String(32), nullable=False, server_default='')
    password: Mapped[str] = Column(String(64), nullable=False, server_default='123456')
    birth_date: Mapped[datetime.date] = Column(Date, nullable=False)
    create_time: Mapped[datetime.datetime] = Column(DateTime, nullable=False, server_default=func.now())

    def __str__(self):
        return f'{self.id}: {self.username}'

    __repr__ = __str__
