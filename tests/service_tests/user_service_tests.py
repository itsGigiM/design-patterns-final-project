import uuid

from core.repository_interface.user_repository_interface import IUserRepository
from core.services.user_service import UserService
from core.user import UserFactory


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
    user_data = "gigiBandia@gmail.com"

    result = user_service.register_user(user_data=user_data)

    assert isinstance(result, uuid.UUID)
