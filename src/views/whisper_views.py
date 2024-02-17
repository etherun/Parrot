from fastapi import APIRouter

from src.config import Settings
from src.schemas.whisper_schema import PathSchema
from src.schemas.base import ResponseSchemaCustom
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
    # pylint: disable=no-member
    whisper_response = whisper_stub.Transcribe(
        parrot_pb2.AudioPathRequest(path=path.text)
    )
    return ResponseSchemaCustom(data=whisper_response.text.strip())
