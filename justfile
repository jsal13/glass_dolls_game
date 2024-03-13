set shell := ["zsh", "-cu"]

default:
  just --list

docs-serve:
  mkdocs serve

docs-build:
  mkdocs build

venv: 
  python -m venv .venv
  source .venv/bin/activate \
    && pip install -r requirements.txt \
    && pip install -r requirements-dev.txt

test:
  pytest --doctest-modules
