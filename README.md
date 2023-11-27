<h1 align="center">Remote CNC API</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/Leandro-Bertoluzzi/remote-cnc-api?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/Leandro-Bertoluzzi/remote-cnc-api?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/Leandro-Bertoluzzi/remote-cnc-api?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/Leandro-Bertoluzzi/remote-cnc-api?color=56BEB8">
</p>

<!-- Status -->

<h4 align="center">
	🚧 Remote CNC API 🚀 Under construction...  🚧
</h4>

## Getting Started

Before running the project for the first time, you must make some configuration:

```bash
# 1. Set up an isolated Python environment with dependencies installed
# Option 1: If you use Conda
conda env create -f environment.yml
conda activate cnc-remote-api

# Option 2: If you use venv and pip
$ pip install -r requirements.txt
# Activate your environment according to your OS:
# https://docs.python.org/3/tutorial/venv.html

# 2. Copy and configure environment variables
$ cp .env.dist .env
$ cp core/.env.example core/.env

# 3. Run DB migrations
$ cd core
$ alembic upgrade head
```

To complete step 2, you must create a `TOKEN_SECRET`. You can run the python interpreter, run the following code and copy the result in the .env file:
```python
from secrets import token_hex
token_hex(64)
```

Then, and every time you want to start your app in development mode, you must run:

```bash
$ uvicorn app:app --reload
```

## :wrench: Running tests

### Code style linter

```bash
$ flake8
```

### Type check

```bash
$ mypy .
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.
