from typing import Optional
from fastapi import Request, status
from pydantic import BaseModel
from async_property import async_cached_property, AwaitLoader

from src.services.redis import redismanager
from src.config import Settings
from src.utils.exceptions import CustomException


class RedisDriver:
    EXPIRE_SECONDS = int(Settings.config("EXPIRE_SECONDS"))

    _hgetall_script = None
    _hmset_script = None

    @property
    def hgetall_script(self):
        if self._hgetall_script:
            return self._hgetall_script
        lua = """
            local flat_map = redis.call("hgetall", KEYS[1])
            if next(flat_map) ~= nil then
                redis.call("expire", KEYS[1], ARGV[1])
                return flat_map
            end
            return {}
        """
        self._hgetall_script = redismanager.pool.register_script(lua)
        return self._hgetall_script

    @property
    def hmset_script(self):
        if self._hmset_script:
            return self._hmset_script
        lua = """
            local seconds = table.remove(ARGV, #ARGV)
            redis.call("hmset", KEYS[1], unpack(ARGV))
            redis.call("expire", KEYS[1], seconds)
        """
        self._hmset_script = redismanager.pool.register_script(lua)
        return self._hmset_script

    async def hmset(self, session_id, cache_value):
        flat_map = []
        for key, value in cache_value.items():
            flat_map.append(key)
            flat_map.append(value)
        flat_map.append(self.EXPIRE_SECONDS)
        await self.hmset_script(keys=[session_id], args=flat_map)

    async def hgetall(self, session_id):
        flat_map = await self.hgetall_script(
            keys=[session_id], args=[self.EXPIRE_SECONDS]
        )
        session_map = {}
        for i in range(0, len(flat_map), 2):
            session_map[flat_map[i]] = flat_map[i + 1]
        return session_map

    async def delete(self, session_id):
        await redismanager.pool.delete(session_id)


class SessionManager(AwaitLoader):
    SESSION_NAME = Settings.config("SESSION_NAME")

    def __init__(self, session_id):
        self._driver = None
        self.session_id = session_id
        self._cache_map = {}
        self._session_map = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = RedisDriver()
        return self._driver

    @async_cached_property
    async def session_map(self) -> dict:
        if self._session_map is None:
            self._session_map = await self.driver.hgetall(self.session_id)
        return self._session_map

    def __setitem__(self, key, value):
        self._cache_map[key] = value

    async def __getitem__(self, key):
        value = self._cache_map.get(key)
        if not value:
            return await self.session_map.get(key)  # pylint: disable=no-member
        return value

    async def clear(self):
        await self.driver.delete(self.session_id)

    async def set(self):
        if not self._cache_map:
            return
        await self.driver.hmset(self.session_id, self._cache_map)


class SessionData(BaseModel):
    uid: int
    username: str
    email: str
    is_admin: int


class SessionChecker:
    def __init__(
        self,
        *,
        admins_only: bool = False,
        auto_error: bool = False,
    ):
        self.admins_only = admins_only
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[SessionData]:
        _session_map = await request.session.session_map
        if not _session_map:
            if self.auto_error:
                raise CustomException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    status="INVALID_SESSION",
                )
            return

        if self.admins_only and not int(_session_map["is_admin"]):
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                status="USER_NOT_ADMIN",
            )

        return SessionData(
            uid=int(_session_map["uid"]),
            is_admin=int(_session_map["is_admin"]),
            username=_session_map["username"],
            email=_session_map["email"],
        )
