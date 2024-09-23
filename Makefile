.PHONY: test

run:
	cd ./src && python -m presentation.cli

test:
	pytest
	
venv:
	python -m venv .venv

env:
	source .venv/bin/activate

install:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt

lint:
	ruff check

fmt:
	ruff format src