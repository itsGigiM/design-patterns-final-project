import pytest

from infra.repository.user_repository import InMemoryUserRepository


@pytest.fixture
def user_repo() -> InMemoryUserRepository:
    user_repo = InMemoryUserRepository()
    user_repo.create_table()
    return user_repo


def test_create_user() -> None:
    user_repo = InMemoryUserRepository()
    email = "test@example.com"
    assert user_repo.create_user(email) == email


def test_create_user_duplicate_email(user_repo: InMemoryUserRepository) -> None:
    email = "duplicate@example.com"
    user_repo.create_user(email)
    with pytest.raises(Exception):
        user_repo.create_user(email)


def test_exists_user(user_repo: InMemoryUserRepository) -> None:
    email = "exists@gmail.com"
    user_repo.create_user(email)
    assert user_repo.exists_user(email) is True


def test_exists_user_nonexistent(user_repo: InMemoryUserRepository) -> None:
    email = "doesnotexist@gmail.com"
    assert user_repo.exists_user(email) is False


def test_set_wallet_number(user_repo: InMemoryUserRepository) -> None:
    email = "wallets@gmail.com"
    wallet_num = 1
    user_repo.create_user(email)
    user_repo.set_wallet_number(email, wallet_num)
    assert user_repo.get_wallet_number(email) == wallet_num


def test_set_wallet_number_nonexistent_user(user_repo: InMemoryUserRepository) -> None:
    email = "none@gmail.com"
    wallet_num = 12345
    with pytest.raises(Exception):
        user_repo.set_wallet_number(email, wallet_num)
