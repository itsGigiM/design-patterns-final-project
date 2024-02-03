from typing import Protocol


class IUserRepository(Protocol):
    def create_user(self, email: str) -> str:
        pass

    def exists_user(self, email: str) -> bool:
        pass

    def set_wallet_number(self, email: str, wallet_num: int) -> None:
        pass

    def get_wallet_number(self, email: str) -> int:
        pass
