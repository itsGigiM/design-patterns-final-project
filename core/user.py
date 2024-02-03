import uuid
from asyncio import Protocol
from dataclasses import dataclass


@dataclass
class IUser(Protocol):
    api_key: uuid.UUID


@dataclass
class User(IUser):
    api_key: uuid.UUID


# class IUserFactory(ABC):
#     users_repository: UsersRepository
#
#     @abstractmethod
#     def generate_user(self, email: str):
#         pass
#
#
# @dataclass()
# class UserFactory(IUserFactory):
#     users_repository: UsersRepository
#
#     def generate_user(self, email: str):
#         if users_repository.contains(email):
#             return USER_ALREADY_EXISTS_ERROR
#         users_repository.add_user(email)
#         return User(api_key=uuid.uuid4())
