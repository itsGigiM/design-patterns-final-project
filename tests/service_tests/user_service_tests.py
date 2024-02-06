import uuid
from typing import Protocol

from core.services.user_service import UserService
from core.user import UserFactory
from infra.repository.user_repository import InMemoryUserRepository


def test_register_user() -> None:
    user_repository = InMemoryUserRepository()
    user_factory = UserFactory(user_repository=user_repository)
    user_service = UserService(user_factory=user_factory)
    user_data = "gigiBandia@gmail.com"

    result = user_service.register_user(user_data=user_data)

    assert isinstance(result, uuid.UUID)
