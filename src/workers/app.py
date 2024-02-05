from celery import Celery

from src.config import Settings


celery_app = Celery(
    "Artifacory_worker",
    broker=Settings.redis_dsn,
    include=[
        "src.workers.tasks",
    ],
)

default_queue = {"queue": "celery"}

celery_app.conf.update(
    worker_pool_restarts=True,
    broker_connection_retry_on_startup=True,
    broker_transport_options={"priority_steps": list(range(10))},
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=256,
    task_routes={
        "src.workers.tasks.*": default_queue,
    },
)
