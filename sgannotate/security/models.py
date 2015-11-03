# -*- coding: utf-8 -*-
import datetime as dt

from sgannotate.database import (
    Column,
    db,
    Model,
)

class Annotation(Model):

    __tablename__ = 'ip_annotations'
    cidr = db.Column(db.String(80), primary_key=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    name = Column(db.String(255))

    def __init__(self, cidr, **kwargs):
        db.Model.__init__(self, cidr=cidr, **kwargs)

    def __repr__(self):
        return '<Annotation %s = %s>' % self.cidr, self.name
