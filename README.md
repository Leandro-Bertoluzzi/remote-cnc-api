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

# 2. Run DB migrations
$ alembic upgrade head
```

Then, and every time you want to start your app in development mode, you must run:

```bash
$ flask --app index run --debug
#or
$ python -m flask --app index run --debug
```

Open [http://localhost:5000](http://localhost:5000) with your browser to see the result.
