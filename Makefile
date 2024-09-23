.PHONY: test

run:
	cd ./src && python -m presentation.cli

test:
	pytest
	
env:
	python -m venv .venv

venv:
	source .venv/bin/activate

install:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt

lint:
	ruff check

fmt:
	ruff format src