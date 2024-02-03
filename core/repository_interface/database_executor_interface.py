from typing import Any, Optional, Protocol, Tuple


class IDatabaseExecutor(Protocol):

    def execute_query(self, q: str, p: Optional[Tuple[Any, ...]] = None) -> int:
        pass

    def search(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Any:
        pass

    def commit(self) -> None:
        pass
