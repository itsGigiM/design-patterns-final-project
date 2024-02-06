import uuid

import pytest

from core.user import User, UserFactory
from infra.repository.user_repository import InMemoryUserRepository


def test_user_creation() -> None:
    key = uuid.uuid4()
    user = User(api_key=key)
    assert user.api_key == key
    assert isinstance(user, User)


def test_users_unique_api_key() -> None:
    api_key1 = uuid.uuid4()
    api_key2 = uuid.uuid4()

    user_a = User(api_key=api_key1)
    user_b = User(api_key=api_key2)

    assert user_a != user_b


def test_generate_user_success() -> None:
    user_repository = InMemoryUserRepository()
    user_factory = UserFactory(user_repository)
    email = "ggg@gmail.com"

    result = user_factory.generate_user(email)

    assert isinstance(result, User)
    assert user_repository.exists_user(email)
    assert user_repository.get_wallet_number(email) == 0


def test_generate_user_already_exists() -> None:
    user_repository = InMemoryUserRepository()
    user_factory = UserFactory(user_repository)
    email = "ggg@gmail.com"

    user_factory.generate_user(email)

    with pytest.raises(Exception):
        user_factory.generate_user(email)
