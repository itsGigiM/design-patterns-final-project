import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from core.exceptions import UserExistsError
from core.repository_interface.user_repository_interface import IUserRepository


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
    def generate_user(self, email: str) -> IUser:
        pass


@dataclass()
class UserFactory(IUserFactory):
    user_repository: IUserRepository

    def generate_user(self, email: str) -> IUser:
        if self.user_repository.exists_user(email):
            raise UserExistsError
        self.user_repository.create_user(email)
        return User(api_key=uuid.uuid4())
