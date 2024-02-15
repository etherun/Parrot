from fastapi import APIRouter

from src.views import user_views, whisper_views, video_views

router = APIRouter(prefix="/api/v1")

for each_router in [
    user_views.user_router,
    whisper_views.whisper_router,
    video_views.video_router,
]:
    router.include_router(each_router)
