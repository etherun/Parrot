import email.utils
import hashlib
from calendar import timegm
from datetime import datetime, timedelta
from uuid import uuid4
from starlette.requests import Request

from src.services.sessions import SessionManager
from src.config import Settings


async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get(SessionManager.SESSION_NAME)
    create_session = None
    if not session_id:
        create_session = session_id = hashlib.sha256(
            str(uuid4()).encode("utf-8")
        ).hexdigest()
        request.cookies[SessionManager.SESSION_NAME] = session_id
        request.scope["headers"].append(
            (b"cookie", f"{SessionManager.SESSION_NAME}={session_id}".encode())
        )
    session = SessionManager(session_id)
    request.scope["session"] = session
    response = await call_next(request)
    if request.url.path.endswith("/clear-session"):
        response.delete_cookie(key=SessionManager.SESSION_NAME)
    elif create_session:
        max_age = int(Settings.config("EXPIRE_SECONDS"))
        expires = email.utils.formatdate(
            timeval=timegm(
                (datetime.utcnow() + timedelta(seconds=max_age)).utctimetuple()
            ),
            usegmt=True,
        )
        response.set_cookie(
            key=SessionManager.SESSION_NAME,
            value=create_session,
            httponly=True,
            max_age=max_age,
            expires=expires,
        )
    await session.set()
    return response
