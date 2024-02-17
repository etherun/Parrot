from datetime import datetime
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate

from src.utils.videos import VideoUtils
from src.utils.pagination import Page
from src.schemas.base import ResponseSchemaCustom
from src.services.database import get_db
from src.models.video_models import Video
from src.workers.tasks import sentiment_analysis
from src.schemas.video_schema import VideoSchema

video_router = APIRouter(prefix="/videos", tags=["Videos"])


@video_router.post("/upload")
async def upload_video(
    video: UploadFile,
    db_session: AsyncSession = Depends(get_db),
):
    contents = await video.read()
    video_checksum = VideoUtils.save(contents)
    await video.close()
    await db_session.execute(
        Insert(Video)
        .values(
            {
                "checksum": video_checksum,
            }
        )
        .on_conflict_do_update(
            index_elements=[Video.checksum],
            set_={"updated_time": datetime.utcnow()},
        )
    )
    await db_session.commit()

    sentiment_analysis.delay(video_checksum)
    return ResponseSchemaCustom(data={"checksum": video_checksum})


@video_router.get("", response_model=Page[VideoSchema])
async def get_videos(
    db_session: AsyncSession = Depends(get_db),
):
    query = select(Video).order_by(Video.created_time.desc())
    return await paginate(db_session, query)
