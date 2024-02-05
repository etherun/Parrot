import datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

from src.config import Settings
from src.models.user_models import User
from src.services.database import get_db
from src.schemas.user_schema import UserSchema, UserResponseSchema
from src.schemas.whisper_schema import PathSchema
from src.schemas.base import ResponseSchemaCustom
from src.models.models_base import model2dict
from src.services.sessions import SessionChecker, SessionData
from parrot_grpc import parrot_pb2, parrot_pb2_grpc

whisper_router = APIRouter(prefix="/whisper", tags=["Whisper"])


@whisper_router.post(
    "/transcribe",
    response_model=ResponseSchemaCustom,
)
async def get_transcribe(
    path: PathSchema,
    # db_session: AsyncSession = Depends(get_db),
    # session: SessionData | None = Depends(SessionChecker()),
):
    whisper_stub = parrot_pb2_grpc.WhisperServiceStub(Settings.whisper_channel)
    whisper_response = whisper_stub.Transcribe(parrot_pb2.AudioPathRequest(path=path.text))
    return ResponseSchemaCustom(data=whisper_response.text.strip())
