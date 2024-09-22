### Start Project
I assume you already had `venv` to create virtual env. for the project dependencies. In ubuntu / WSL2 you should install it first.
- `sudo apt install python-venv`

Then create a virtual env:

- `python -m venv my-env`

- Activate it:  `source my-env/bin/activate`

Then simply install dependencies:

- `pip install -r requirements.txt`

Then create your .env file with below variables:
```
ENV=development
PROJECT_NAME=Github Issue Tracker
DATABASE_URL=postgresql+psycopg://testuser:testpass*@localhost/issue_tracker
REDIS_URL=redis://localhost:6379/9
GITHUB_TOKEN=your_github_token_here
SECRET_KEY=bestsecret
ACCESS_TOKEN_EXPIRE_MINUTES=5
MAIL_USERNAME=""
MAIL_PASSWORD=""
MAIL_FROM=test@gmail.com
MAIL_PORT=1025
MAIL_SERVER=localhost
MAIL_TLS=False
MAIL_SSL=False
MAIL_STARTTLS=False
MAIL_SSL_TLS=False
USE_CREDENTIALS=False
VALIDATE_CERTS=False
API_V1_STR=/api/v1
POSTGRES_USER=test
POSTGRES_PASSWORD=test*
POSTGRES_DB=test
POSTGRES_PORT=5432
```

Finally, simply start the app:

- `uvicorn app.main:app --reload`


### How To
- First, register with an test or real email and use `/token/` endpoint and login with your credentials to get token which will need for other endpoints.
- Secondly, track some real repository that exists on github. You wiil need to provide a github user name and repo name.
- Finally check `https://canilgu.dev/mailhog` to see if you got an email from us for issue changes.
- Furthermore, you can play with our api using `https://canilgu.dev/issue-tracker/docs`.


### Docker for production

Initially we could build our project.

- `docker compose build`

Then simply we could start our dockerized project like below:

- `docker compose up -d`.


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

or trigger single test file:

- `pytest -s tests/test_repos.py`

