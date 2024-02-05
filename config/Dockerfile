FROM python:3.10.12-slim-bullseye

ARG BUILD_ENV
ENV BUILD_ENV $BUILD_ENV
RUN python3 -m venv /opt/venv

COPY . /web/
WORKDIR /web
RUN chmod -R 777 /web

RUN . /opt/venv/bin/activate && \
    pip install pip -U && \
    pip install -r ./config/requirements.txt && \
    chmod +x ./config/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./config/entrypoint.sh"]