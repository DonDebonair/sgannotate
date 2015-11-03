# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from sgannotate.user.models import User
from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User('foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        user = User(email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_factory(self, db):
        user = UserFactory()
        db.session.commit()
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.active is True

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"
