# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall
from factory.alchemy import SQLAlchemyModelFactory

from sgannotate.user.models import User
from sgannotate.database import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    active = True

    class Meta:
        model = User
