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

# 2. Run DB migrations
$ flask db upgrade
```

Then, and every time you want to start your app in development mode, you must run:

```bash
$ flask --app app run --debugger
#or
$ python -m flask --app app run --debugger
```

Open [http://localhost:5000](http://localhost:5000) with your browser to see the result.
