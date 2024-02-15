from fastapi import APIRouter, UploadFile
from src.utils.videos import Video
from src.schemas.base import ResponseSchemaCustom
from src.utils.exceptions import CustomException

video_router = APIRouter(prefix="/videos", tags=["Videos"])


@video_router.post("/upload")
async def upload_video(video: UploadFile):
    try:
        contents = await video.file.read()
        video_checksum = Video.save(contents)
    except Exception as _error:
        raise CustomException(data="Upload Error.")
    finally:
        await video.file.close()

    return ResponseSchemaCustom(data={"checksum": video_checksum})
