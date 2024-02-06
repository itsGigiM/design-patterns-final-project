from typing import Protocol
from uuid import UUID

from core.user import IUserFactory


class IUserService(Protocol):
    def register_user(self, user_data: str) -> UUID:
        pass


class UserService(IUserService):
    def __init__(self, user_factory: IUserFactory):
        self.user_factory = user_factory

    def register_user(self, user_data: str) -> UUID:
        return self.user_factory.generate_user(email=user_data).api_key
