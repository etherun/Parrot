import asyncio

from src.workers.app import celery_app


@celery_app.task
def demo_celery(**kwargs):
    async def _run():
        print(f"Celery async task get: {kwargs}")

    asyncio.get_event_loop().run_until_complete(_run())
