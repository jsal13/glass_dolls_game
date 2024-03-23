set shell := ["zsh", "-cu"]

default:
  just --list

docs-serve:
  mkdocs serve

docs-build:
  mkdocs build

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
  python -m pytest --doctest-modules ./tests
