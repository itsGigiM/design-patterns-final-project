from typing import Protocol


class ICreateDatabase(Protocol):
    def drop_table(self) -> None:
        pass

    def create_table(self) -> None:
        pass
