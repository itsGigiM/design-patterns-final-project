from fastapi import APIRouter, Depends
from fastapi import HTTPException, Header

from core.bitcoin_wallet_service import BitcoinWalletService
from core.constants import ADMIN_API_KEY
from core.model.request.request import UserRegistrationRequest, TransactionRequest
from core.model.response.response import UserRegistrationResponse, WalletResponse, TransactionResponse, \
    StatisticsResponse

app_router = APIRouter()
service_dependency = BitcoinWalletService() # TODO add dependency services


def get_service() -> BitcoinWalletService:
    return service_dependency


@app_router.post("/users",
                 response_model=UserRegistrationResponse,
                 responses={500: {"description": "Couldn't register the user"}})
def register_user(user_data: UserRegistrationRequest,
                  s: BitcoinWalletService = Depends(get_service)) -> UserRegistrationResponse:
    try:
        return UserRegistrationResponse(s.register_user(user_data.email))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.post("/wallets",
                 response_model=WalletResponse)
def create_wallet(api_key: str = Header(...),
                  s: BitcoinWalletService = Depends(get_service)) -> WalletResponse:
    try:
        res = s.create_wallet(api_key)
        return WalletResponse(str(res.address), res.amount, res.usd_amount)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.get("/wallets/{address}")
async def get_wallet_info(address: str,
                          api_key: str = Header(...),
                          s: BitcoinWalletService = Depends(get_service)) -> WalletResponse:
    try:
        res = s.get_wallet(address, api_key)
        return WalletResponse(str(res.address), res.amount, res.usd_amount)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.post("/transactions")
async def make_transaction(
        transaction_request: TransactionRequest,
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service)) -> TransactionResponse:
    try:
        return s.make_transaction(transaction_request, api_key)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.get("/transactions")
async def get_transactions(
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service)) -> TransactionResponse:
    try:
        return s.get_transactions(api_key)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.get("/wallets/{address}/transactions")
async def get_wallet_transactions(
        address: str,
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service)) -> TransactionResponse:
    try:
        return s.get_wallet_transactions(address, api_key)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app_router.get("/statistics")
async def get_statistics(
        api_key: str = Header(...),
        s: BitcoinWalletService = Depends(get_service)) -> StatisticsResponse:
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Access denied.")
    return s.get_statistics()
