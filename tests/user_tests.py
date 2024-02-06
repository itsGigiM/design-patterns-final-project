import uuid

import pytest

from core.repository_interface.user_repository_interface import IUserRepository
from core.services.user_service_interface import UserService
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


class StubUserRepository(IUserRepository):
    def create_user(self, email: str) -> str:
        pass

    def exists_user(self, email: str) -> bool:
        pass

    def set_wallet_number(self, email: str, wallet_num: int) -> None:
        pass

    def get_wallet_number(self, email: str) -> int:
        pass


def test_register_user() -> None:
    user_repository = StubUserRepository()
    user_factory = UserFactory(user_repository=user_repository)
    user_service = UserService(user_factory=user_factory)
    user_data = "gg@gmail.com"

    result = user_service.register_user(user_data=user_data)

    assert isinstance(result, uuid.UUID)
