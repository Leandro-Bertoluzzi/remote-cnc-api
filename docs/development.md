# Starting

## Install dependencies

Before using the app for the first time you should run:

```bash
# Clone this project
$ git clone --recurse-submodules https://github.com/Leandro-Bertoluzzi/remote-cnc-api

# 1. Access the repository
$ cd remote-cnc-api

# 2. Set up your Python environment
# Option 1: If you use Conda
conda env create -f environment.yml
conda activate cnc-remote-api

# Option 2: If you use venv and pip
$ python -m venv env-dev
$ source env-dev/bin/activate
$ pip install -r requirements-dev.txt

# 3. Copy and configure the .env file
cp .env.example .env
```

### Windows

Take into account that the virtual environment activation with pip (step 2, option 2) is slightly different in Windows:

```bash
$ python -m venv env-dev
$ .\env-dev\Scripts\activate
$ pip install -r requirements-dev.txt
```

## Environment variables

To complete the environment variables, you must create a `TOKEN_SECRET`. You can run the python interpreter, run the following code and copy the result in the .env file:
```python
from secrets import token_hex
token_hex(64)
```

## Run the API

### Locally

Once installed all dependencies and created the Python environment, you can run the API locally:

```bash
# 1. Activate your Python environment
# Option 1: If you use Conda
conda activate cnc-remote-api

# Option 2: If you use venv and pip
$ source env-dev/bin/activate

# 2. Start the app with auto-reload
$ uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.

### Docker

You can also run the API in a Docker container. This will also start a containerized DB, plus an `adminer` instance.

```bash
$ docker compose up -d
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.

# Manage database

To see your database, you can either use the `adminer` container which renders an admin in `http://localhost:8080` when running the `docker-compose.yml`; or connect to it with a client like [DBeaver](https://dbeaver.io/).

You can also manage database migrations by using the following commands inside the `core` folder.

- Apply all migrations:

```bash
$ alembic upgrade head
```

- Revert all migrations:

```bash
$ alembic downgrade base
```

More info about Alembic usage [here](https://alembic.sqlalchemy.org/en/latest/tutorial.html).
