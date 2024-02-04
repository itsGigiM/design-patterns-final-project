from asyncio import Protocol


class IUserService(Protocol):
    def register_user(self, user_data: str) -> str:
        pass
