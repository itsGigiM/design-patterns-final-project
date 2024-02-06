import uuid
from core.constants import BTC_STARTING_BALANCE, SAME_OWNERS_TRANSACTION_FEE
from infra.fee_strategy import FeeStrategy


def test_strategy_same_owner() -> None:
    owner = str(uuid.uuid4())
    amount = BTC_STARTING_BALANCE
    strategy = FeeStrategy()
    fee = strategy.calculate_transaction_fee(amount, owner, owner)
    assert fee == SAME_OWNERS_TRANSACTION_FEE


def test_strategy_different_owners() -> None:
    from_wallet = str(uuid.uuid4())
    to_wallet = str(uuid.uuid4())
    amount = BTC_STARTING_BALANCE
    strategy = FeeStrategy()
    fee = strategy.calculate_transaction_fee(amount, from_wallet, to_wallet)
    assert fee == 0.015


def test_fee_should_be_rounded_up() -> None:
    from_wallet = str(uuid.uuid4())
    to_wallet = str(uuid.uuid4())
    amount = BTC_STARTING_BALANCE * 0.00000001
    strategy = FeeStrategy()
    fee = strategy.calculate_transaction_fee(amount, from_wallet, to_wallet)
    assert fee == 0.00000001
