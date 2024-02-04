import uuid
from abc import ABC, abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from core.repository_interface.user_repository_interface import IUserRepository
from core.constants import USER_ALREADY_EXISTS_ERROR


@dataclass
class IUser(Protocol):
    api_key: uuid.UUID


@dataclass
class User(IUser):
    api_key: uuid.UUID


@dataclass
class IUserFactory(ABC):
    user_repository: IUserRepository

    @abstractmethod
    def generate_user(self, email: str) -> User:
        pass


@dataclass()
class UserFactory(IUserFactory):
    user_repository: IUserRepository

    def generate_user(self, email: str) -> User:
        if self.user_repository.exists_user(email):
            raise Exception("User already exists")
        self.user_repository.create_user(email)
        return User(api_key=uuid.uuid4())
