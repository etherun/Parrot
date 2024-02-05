### Dependencies

- PostgreSQL

```
docker run --name <pgsql-local> -e POSTGRES_PASSWORD=admin123 -p 5432:5432 postgres:latest
```

- Redis

```
docker run --name <local-redis> -p 6379:6379 -d redis
```

### Build Image

```
<project_root> $ docker build -f ./config/Dockerfile --build-arg BUILD_ENV=<dev/stage/prod> -t <docker_repo>:<1.0.0> .   
```

### Launch Backend of Fastapi 

```
uvicorn src:server --reload
```
- `--env-file=config/<stage/prod>.env`, can be used to specify the config file to be start with
- `--workers=<4>`, can be used to specify the process number of workers
