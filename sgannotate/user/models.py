# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin

from sgannotate.database import (
    Column,
    db,
    Model,
    SurrogatePK
)

class User(UserMixin, Model, SurrogatePK):

    __tablename__ = 'users'
    email = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)

    def __init__(self, email, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User %s>' % self.email
