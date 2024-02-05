from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .views import router
from .services.database import sessionmanager
from .services.redis import redismanager
from .config import Settings
from .utils.exceptions import CustomException
from .utils.middlewares import session_middleware


def init_app(startup=True):
    lifespan = None

    if startup:
        sessionmanager.init(Settings.postgres_dsn)
        redismanager.init(Settings.redis_dsn)

        @asynccontextmanager
        async def lifespan(_: FastAPI):  # pylint: disable=function-redefined
            yield
            if sessionmanager._engine is not None:  # pylint: disable=protected-access
                await sessionmanager.close()
            if redismanager.pool is not None:
                await redismanager.close()

    app = FastAPI(
        title="FastAPI",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/docs/openai.json",
        redoc_url=None,
    )
    app.include_router(router)

    return app


server = init_app()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
server.middleware("http")(session_middleware)
add_pagination(server)


@server.exception_handler(CustomException)
async def custom_exception_handler(_: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status,
            "data": exc.data,
        },
    )
