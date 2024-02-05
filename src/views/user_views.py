import datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

from src.models.user_models import User
from src.services.database import get_db
from src.schemas.user_schema import UserSchema, UserResponseSchema
from src.schemas.base import ResponseSchemaCustom
from src.models.models_base import model2dict
from src.services.sessions import SessionChecker, SessionData

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post(
    "/login",
    response_model=ResponseSchemaCustom[UserResponseSchema],
)
async def create_user(
    request: Request,
    user: UserSchema,
    db_session: AsyncSession = Depends(get_db),
    session: SessionData | None = Depends(SessionChecker()),
):
    if session:
        _user = await User.get_by_id(db_session, session.uid)
        return ResponseSchemaCustom(data=UserResponseSchema(**model2dict(_user)))

    query = (
        update(User)
        .where(User.username == user.username, User.email == user.email)
        .values(updated_time=datetime.datetime.now())
        .returning(
            User.id,
            User.username,
            User.email,
            User.is_admin,
            User.is_active,
            User.created_time,
            User.updated_time,
        )
    )
    try:
        user_dict = (await db_session.execute(query)).mappings().one()
        await db_session.commit()
    except NoResultFound:
        _user = await User.create(db_session, user)
        user_dict = model2dict(_user)

    request.session["uid"] = user_dict["id"]
    request.session["is_admin"] = int(user_dict["is_admin"])
    request.session["email"] = user_dict["email"]
    request.session["username"] = user_dict["username"]

    return ResponseSchemaCustom(data=UserResponseSchema(**user_dict))


@user_router.get(
    "/current-user",
    response_model=ResponseSchemaCustom[UserResponseSchema],
)
async def get_current_user(
    session: SessionData = Depends(SessionChecker(auto_error=True)),
    db_session: AsyncSession = Depends(get_db),
):
    _user = await User.get_by_id(db_session, session.uid)
    return ResponseSchemaCustom(data=UserResponseSchema(**model2dict(_user)))


@user_router.post(
    "/logout",
    response_model=ResponseSchemaCustom,
)
async def clear_session(request: Request):
    if await request.session.session_map:
        await request.session.clear()
    return ResponseSchemaCustom(data=None)
