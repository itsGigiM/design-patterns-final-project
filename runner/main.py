import uvicorn
from fastapi import FastAPI

from infra.fastapi.bitcoin_wallet_api import app_router


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(app_router)
    return app


if __name__ == "__main__":
    uvicorn.run(setup(), host="0.0.0.0", port=8000)
