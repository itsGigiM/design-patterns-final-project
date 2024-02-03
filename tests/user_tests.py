import pytest
import uuid

from core.user import User, IUser


def test_user_creation():
    key = uuid.uuid4()
    user = User(api_key=key)
    assert user.api_key == key
    assert isinstance(user, IUser)


def test_users_unique_api_key():
    api_key1 = uuid.uuid4()
    api_key2 = uuid.uuid4()

    user_a = User(api_key=api_key1)
    user_b = User(api_key=api_key2)

    assert user_a != user_b