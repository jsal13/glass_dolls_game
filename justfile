set shell := ["zsh", "-cu"]

default:
  just --list

# Requires docker to be set up.
run:
  python ./glassdolls/main_game.py

up:
  docker compose up --remove-orphans -w

down:
  docker compose down --remove-orphans --volumes

build:
  docker compose build

docs:
  quarto render docs

venv: 
  python -m venv .venv
  # Use uv package to pip install.
  # Ref: https://github.com/astral-sh/uv?tab=readme-ov-file#highlights
  export CONDA_PREFIX="" \
    && source .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install uv \
    && uv pip install -r requirements.txt \
    && uv pip install -r requirements-dev.txt
  
activate:
  source .venv/bin/activate

test:
  coverage run -m pytest --doctest-modules tests/
  coverage report && coverage html

# Requires wslu
# Requires running:
# wslview -r $(wslpath -au 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
ui:
  www-browser http://localhost:5000  # App 
  www-browser http://localhost:8001/docs/  # Backend
  www-browser http://localhost:15672  # RabbitMQ
  www-browser http://localhost:8081  # Mongo Express
  www-browser http://localhost:3000  # Loki
