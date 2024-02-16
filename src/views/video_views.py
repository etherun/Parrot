from datetime import datetime
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import Insert

from src.utils.videos import VideoUtils
from src.schemas.base import ResponseSchemaCustom
from src.utils.exceptions import CustomException
from src.services.database import get_db
from src.models.video_models import Video

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
    
    return ResponseSchemaCustom(data={"checksum": video_checksum})
