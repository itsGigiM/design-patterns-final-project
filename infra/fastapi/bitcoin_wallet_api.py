from fastapi import APIRouter, Depends, Header

from core.model.request.request import TransactionRequest, UserRegistrationRequest
from core.model.response.response import (
    StatisticsResponse,
    TransactionResponse,
    UserRegistrationResponse,
    WalletResponse,
)
from core.services.bitcoin_wallet_service import BitcoinWalletService
from core.services.transaction_service import TransactionService
from core.services.user_service import UserService
from core.services.wallet_service import WalletService
from core.user import UserFactory
from core.walletToWalletUSDAdapter import WalletToUSDWalletAdapter
from infra.BTCtoUSDconverter import BTCtoUSDConverter
from infra.fee_strategy import FeeStrategy
from infra.repository.database_connection import DatabaseConnection
from infra.repository.database_executor import DatabaseExecutor
from infra.repository.transaction_repository import SQLTransactionRepository
from infra.repository.user_repository import SQLUserRepository
from infra.repository.wallet_repository import SQLWalletRepository

executor = DatabaseExecutor(DatabaseConnection())

u_repository = SQLUserRepository(executor)
w_repository = SQLWalletRepository(executor)
t_repository = SQLTransactionRepository(executor)
adapter = WalletToUSDWalletAdapter(BTCtoUSDConverter())
u_service = UserService(UserFactory(u_repository))
w_service = WalletService(w_repository, adapter)
t_service = TransactionService(t_repository, FeeStrategy(), w_repository)
service_dependency = BitcoinWalletService(u_service, w_service, t_service)

app_router = APIRouter()


def get_service() -> BitcoinWalletService:
    return service_dependency


@app_router.post(
    "/users",
    response_model=UserRegistrationResponse,
    responses={500: {"description": "Couldn't register the user"}},
)
def register_user(
        user_data: UserRegistrationRequest, s: BitcoinWalletService = Depends(get_service)
) -> UserRegistrationResponse:
    try:
        return UserRegistrationResponse(str(s.register_user(user_data.email)))
    except Exception as e:
        raise e


@app_router.post("/wallets", response_model=WalletResponse)
def create_wallet(
        api_key: str = Header(...), s: BitcoinWalletService = Depends(get_service)
) -> WalletResponse:
    try:
        res = s.create_wallet(api_key)
        return WalletResponse(str(res.address), res.amount, res.usd_amount)
    except Exception as e:
        raise e


@app_router.get("/wallets/{address}")
async def get_wallet_info(
        address: str,
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service),
) -> WalletResponse:
    try:
        res = s.get_wallet(address, api_key)
        return WalletResponse(str(res.address), res.amount, res.usd_amount)
    except Exception as e:
        raise e


@app_router.post("/transactions")
async def make_transaction(
        transaction_request: TransactionRequest,
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service),
) -> None:
    try:
        s.make_transaction(transaction_request, api_key)
    except Exception as e:
        raise e


@app_router.get("/transactions")
async def get_transactions(
        api_key: str = Header(...), s: BitcoinWalletService = Depends(get_service)
) -> TransactionResponse:
    try:
        return TransactionResponse(s.get_transactions(api_key))
    except Exception as e:
        raise e


@app_router.get("/wallets/{address}/transactions")
async def get_wallet_transactions(
        address: str,
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service),
) -> TransactionResponse:
    try:
        return TransactionResponse(s.get_wallet_transactions(address, api_key))
    except Exception as e:
        raise e


@app_router.get("/statistics")
async def get_statistics(
        api_key: str = Header(...), s: BitcoinWalletService = Depends(get_service)
) -> StatisticsResponse:
    return s.get_statistics(api_key)
