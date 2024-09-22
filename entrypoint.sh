#!/usr/bin/env bash


# Run Alembic migrations
alembic upgrade head

# Start the FastAPI app
uvicorn "app.main:app" --host "0.0.0.0" --port 8002 & celery -A worker.tasks worker --loglevel=info --pool=gevent & celery -A worker.tasks beat --loglevel=info
