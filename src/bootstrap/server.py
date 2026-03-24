import asyncio
import contextlib
import typing

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from src.common.http.collections import HTTPError
from src.entrypoints import brokers
from src.entrypoints import http
from src.entrypoints.workers import workers
from src.framework.background import background
from src.infrastructure.databases.postgres import postgres


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> typing.Any:
    postgres.start()
    workers()
    background.start()
    yield
    background.shutdown()
    postgres.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(http.router)

app.include_router(brokers.rabbitmq.router)

@app.exception_handler(HTTPError)
async def error_handler(_: Request, error: HTTPError) -> JSONResponse:
    return JSONResponse(status_code=error.code, content=error.http)

async def run() -> None:
    await uvicorn.Server(
        uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_config=None,
        )
    ).serve()


if __name__ == "__main__":
    asyncio.run(run())
