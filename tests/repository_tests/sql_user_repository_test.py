import pytest

from infra.repository.database_executor import DatabaseExecutor
from infra.repository.user_repository import SQLUserRepository


@pytest.fixture
def user_repo(db_executor: DatabaseExecutor) -> SQLUserRepository:
    user_repo = SQLUserRepository(db_connection=db_executor)
    user_repo.create_table()
    return user_repo


def test_create_user(db_executor: DatabaseExecutor) -> None:
    user_repo = SQLUserRepository(db_executor)
    email = "test@example.com"
    assert user_repo.create_user(email) == email


def test_create_user_duplicate_email(user_repo: SQLUserRepository) -> None:
    email = "test@example.com"
    user_repo.create_user(email)
    with pytest.raises(Exception):
        user_repo.create_user(email)


def test_exists_user(user_repo: SQLUserRepository) -> None:
    email = "mk@gmail.com"
    user_repo.create_user(email)
    assert user_repo.exists_user(email) is True


def test_exists_user_nonexistent(user_repo: SQLUserRepository) -> None:
    email = "kk@gmail.com"
    assert user_repo.exists_user(email) is False


def test_set_wallet_number(user_repo: SQLUserRepository) -> None:
    email = "kk@gmail.com"
    wallet_num = 1
    user_repo.create_user(email)
    user_repo.set_wallet_number(email, wallet_num)
    assert user_repo.get_wallet_number(email) == wallet_num


def test_set_wallet_number_nonexistent_user(user_repo: SQLUserRepository) -> None:
    email = "none@gmail.com"
    wallet_num = 12345
    with pytest.raises(Exception):
        user_repo.set_wallet_number(email, wallet_num)
