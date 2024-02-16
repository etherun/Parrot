import asyncio
import logging
from pathlib import Path
from deepface import DeepFace
from sqlalchemy import update

from src.workers.app import celery_app
from src.utils.videos import VideoUtils
from src.config import PROJECT_ROOT, Settings
from src.models.video_models import Video
from src.services.database import sessionmanager
from parrot_grpc import parrot_pb2, parrot_pb2_grpc


@celery_app.task
def sentiment_analysis(checksum):
    async def _run():
        VideoUtils.extract_audio(checksum)
        VideoUtils.extract_frame(checksum)

        emotions = []    
        video_dir = Path(f"{PROJECT_ROOT}/cache/{checksum[:2]}/{checksum[2:]}")
        for _pic in video_dir.glob("*.png"):
            try:
                emotions.append(
                    DeepFace.analyze( _pic.absolute().as_posix(), actions=["emotion"])[0]
                )
            except Exception as _error:
                logging.error(_error)
                continue
        
        whisper_stub = parrot_pb2_grpc.WhisperServiceStub(Settings.whisper_channel)
        whisper_response = whisper_stub.Transcribe(
            parrot_pb2.AudioPathRequest(
                path=Path(video_dir, "audio.wav").absolute().as_posix()
            )
        )

        query = update(Video).values(
            {
                "text": whisper_response.text.strip(),
                "emotion": emotions,
            }
        ).where(Video.checksum == checksum)
        async with sessionmanager.session() as db:
            await db.execute(query)
            await db.commit()

    asyncio.get_event_loop().run_until_complete(_run())
