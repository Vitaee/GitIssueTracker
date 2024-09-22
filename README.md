### Start Project
I assume you already had `venv` to create virtual env. In ubuntu / WSL2 you should install it first.
- `sudo apt install python-venv`

Then create a virtual env:

- `python -m venv my-env`

- Activate it:  `source my-env/bin/activate`

Then simply install dependencies:

- `pip install -r requirements.txt`

- `uvicorn app.main:app --reload`

### Celery
Start worker:

- celery -A worker.tasks worker --loglevel=info --pool=gevent --logfile=logs/celery.log

Start beat:

- celery -A worker.tasks beat --loglevel=info

### Alembic
Firstyl run below command
- alembic init alembic/

Run initial migrations:

- `alembic revision --autogenerate -m "initial migration"`

Autogenerate Migrations: To autogenerate migrations based on your models, you should run:

- `alembic upgrade head`  # To apply existing migrations
- `alembic revision` --autogenerate -m "Your migration message"
- `alembic upgrade head`  # To apply the new migration

### Tests

- `pytest -s tests/`

### Docker

Initially we could build our project.

- `docker compose build`

Then simply we could start our dockerized project like below:

- `docker compose up -d`.