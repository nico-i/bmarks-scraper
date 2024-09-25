.PHONY: test build

dev:
	cd ./src && python -m presentation.cli

build:
	pyinstaller --onefile --path src -n bkmks src/presentation/cli/__main__.py --paths .venv/lib/python3.12/site-packages

run:
	./dist/bkmks

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