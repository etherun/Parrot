import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi import status


class DatabaseModel:
    id: int

    @classmethod
    async def get(cls, db_session: AsyncSession):
        all_repos = (await db_session.execute(select(cls))).scalars().all()
        return all_repos if all_repos else None

    @classmethod
    async def create(cls, db_session: AsyncSession, model: BaseModel):
        try:
            transaction = cls(**model.model_dump())
            db_session.add(transaction)
            await db_session.commit()
            await db_session.refresh(transaction)
            return transaction
        except IntegrityError as _error:
            # pylint: disable=import-outside-toplevel
            from src.utils.exceptions import CustomException

            logging.exception(_error)
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                status="FORBIDDEN_ERROR",
                data=f"{_error._message}",  # pylint: disable=protected-access
            ) from _error
        except SQLAlchemyError as _error:
            # pylint: disable=import-outside-toplevel
            from src.utils.exceptions import CustomException

            logging.exception(_error)
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                status="FORBIDDEN_ERROR",
                data=str(_error.__dict__["orig"]),  # pylint: disable=protected-access
            ) from _error

    @classmethod
    async def get_by_id(cls, db_session: AsyncSession, target_id: int):
        try:
            return (
                (await db_session.execute(select(cls).where(cls.id == target_id)))
                .scalars()
                .one()
            )
        except NoResultFound as error:
            # pylint: disable=import-outside-toplevel
            from src.utils.exceptions import CustomException

            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                status=f"{cls.__name__.upper()}_ID_NOTFOUND",
            ) from error


def model2dict(row):
    return row.__dict__
