import os
import grpc
import parrot_grpc
from enum import Enum
from functools import lru_cache
from starlette.config import Config
from starlette.datastructures import Secret
from sqlalchemy import URL


class Envs(Enum):
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


class ConfigFile(Enum):
    DEV = "config/dev.env"
    STAGE = "config/stage.env"
    PROD = "config/prod.env"


class Settings:
    @staticmethod
    def get_config():
        match os.getenv("ENV", "").lower():
            case Envs.DEV.value:
                return ConfigFile.DEV.value
            case Envs.STAGE.value:
                return ConfigFile.STAGE.value
            case Envs.PROD.value:
                return ConfigFile.PROD.value
            case _:
                return ConfigFile.DEV.value

    config = Config(env_file=get_config())
    postgres_dsn = URL.create(
        drivername=config("DB_DRIVER", cast=str, default=""),
        host=config("DB_HOST", cast=str, default=""),
        port=config("DB_PORT", cast=int, default=5432),
        username=config("DB_USER", cast=str, default=""),
        password=config("DB_PASSWORD", cast=Secret, default=""),
        database=config("DB_DATABASE", cast=str, default=""),
    )
    redis_dsn = (
        f"{config('REDIS_SUBPROTOCOL', cast=str, default='redis')}://"
        f"{config('REDIS_USERNAME', cast=str, default='')}:"
        f"{config('REDIS_PASSWORD', cast=str, default='')}@"
        f"{config('REDIS_HOST', cast=str, default='127.0.0.1')}:"
        f"{config('REDIS_PORT', cast=str, default='6379')}/"
        f"{config('REDIS_DB_NUM', cast=str, default=0)}"
    )
    whisper_channel = grpc.insecure_channel(config("WHISPER_CHANNEL", cast=str, default="localhost:50051"))


    @lru_cache()
    @staticmethod
    def get_settings():
        return Settings.config
