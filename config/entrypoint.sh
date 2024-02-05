#!/bin/bash
set -e
echo "### GET ENV: ${BUILD_ENV}"

if [ $BUILD_ENV == "stage" ]; then
    env_file=./config/stage.env
elif [ $BUILD_ENV == "prod" ]; then
    env_file=./config/prod.env
else 
    env_file=./config/dev.env
fi
. $env_file

echo "Connect DB_HOST: ${DB_HOST}"
celery_broker=${REDIS_SUBPROTOCOL}://${REDIS_USERNAME}:${REDIS_USERNAME}@${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB_NUM}
echo "Connect BROKER: ${celery_broker}"

/opt/venv/bin/alembic -x dburl=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE} upgrade head
ENV=${BUILD_ENV} /opt/venv/bin/celery -A src.workers.app --broker ${celery_broker} worker -B -c 2 --loglevel=INFO &
/opt/venv/bin/celery -A src.workers.app --broker ${celery_broker} flower --url_prefix=flower &
/opt/venv/bin/uvicorn src:server --host 0.0.0.0 --port 8000 --env-file ${env_file} --reload