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

# 3. Copy and configure the .env files
cp .env.example .env
cp core/.env.example core/.env
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

### Docker

if you are using `docker compose`, you can run the following command to apply database migrations:

```bash
$ docker exec remote-cnc-api bash -c "cd core && alembic upgrade head"
```

# Start the Celery worker

In order to execute tasks and scheduled tasks, you must start the CNC worker (Celery).

```bash
# 1. Move to worker folder
$ cd core/worker

# 2. Start Celery's worker server
$ celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log
```

Optionally, if you are going to make changes in the worker's code and want to see them in real time, you can start the Celery worker with auto-reload.

```bash
# 1. Move to worker folder
$ cd core/worker

# 2. Start Celery's worker server with auto-reload
$ watchmedo auto-restart --directory=./ --pattern=*.py -- celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log
```

### Windows

Due to a known problem with Celery's default pool (prefork), it is not as straightforward to start the worker in Windows. In order to do so, we have to explicitly indicate Celery to use another pool. You can read more about this issue [here](https://celery.school/celery-on-windows).

- **solo**: The solo pool is a simple, single-threaded execution pool. It simply executes incoming tasks in the same process and thread as the worker.

```bash
$ celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log --pool=solo
```

- **threads**: The threads in the threads pool type are managed directly by the operating system kernel. As long as Python's ThreadPoolExecutor supports Windows threads, this pool type will work on Windows.

```bash
$ celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log --pool=threads
```

- **gevent**: The [gevent package](http://www.gevent.org/) officially supports Windows, so it remains a suitable option for IO-bound task processing on Windows. Downside is that you have to install it first.

```bash
# 1. Install gevent
# Option 1: If you use Conda
$ conda install -c anaconda gevent

# Option 2: If you use pip
$ pip install gevent

# 2. Start Celery's worker server
$ celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log --pool=gevent
```
